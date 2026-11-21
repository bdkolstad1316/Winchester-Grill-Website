// Minimal zero-dependency static file server for Railway / Nixpacks.
// Serves the files in this folder. Railway sets PORT; falls back to 8080 locally.
// build marker: 2026-07-18 (retrigger after transient Railway orchestrator failure)
const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = process.env.PORT || 8080;
const ROOT = __dirname;

const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".ico": "image/x-icon",
  ".json": "application/json",
  ".webmanifest": "application/manifest+json",
  ".txt": "text/plain; charset=utf-8",
  ".xml": "application/xml; charset=utf-8",
};

// Security headers applied to every response (static brochure site, no user input).
const SECURITY = {
  "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
  "X-Content-Type-Options": "nosniff",
  "X-Frame-Options": "SAMEORIGIN",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Permissions-Policy": "geolocation=(), microphone=(), camera=(), payment=()",
  "Content-Security-Policy":
    "default-src 'self'; " +
    // plausible.io  -> privacy-friendly traffic analytics (script + event POSTs)
    // cloudflareinsights.com -> Cloudflare RUM beacon, auto-injected at the edge,
    //   gives real-user Core Web Vitals (LCP/INP/CLS) that Plausible doesn't cover.
    "script-src 'self' 'unsafe-inline' https://plausible.io https://static.cloudflareinsights.com; " +
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; " +
    "font-src 'self' https://fonts.gstatic.com; " +
    "img-src 'self' data:; " +
    "connect-src 'self' https://plausible.io https://cloudflareinsights.com; " +
    "frame-ancestors 'self'; base-uri 'self'; form-action 'self'",
};

// Never serve infrastructure / source files, or any dotfile (blocks .git, .env, etc.).
// Belt and braces: anything whose extension isn't in TYPES is also refused below,
// so .md / .py / extensionless strays can't leak even if this list goes stale.
// Names are compared lower-cased, so /Server.js or /OPS/ can't slip past on a
// case-insensitive filesystem (macOS dev machines; Railway's Linux is case-sensitive).
const BLOCKED = new Set(["server.js", "package.json", "package-lock.json", ".gitignore", "claude.md", "404.html"]);
// Top-level folders that are never site content: ops/ holds the menu generators, client/
// holds client material (gitignored, so it isn't deployed — blocked here as a second lock).
const BLOCKED_DIRS = new Set(["ops", "client"]);

// The branded "page not found" screen, read once at startup. 404.html is in BLOCKED so that
// asking for it directly also answers 404. If the file is missing, fall back to a bare heading.
let NOT_FOUND_BODY = Buffer.from("<h1>404 — Not Found</h1>");
try {
  NOT_FOUND_BODY = fs.readFileSync(path.join(ROOT, "404.html"));
} catch {}

function notFound(res) {
  res.writeHead(404, {
    "Content-Type": "text/html; charset=utf-8",
    "Content-Length": String(NOT_FOUND_BODY.length),
    "Cache-Control": "no-cache",
    ...SECURITY,
  });
  res.end(NOT_FOUND_BODY);
}

function methodNotAllowed(res) {
  res.writeHead(405, { "Content-Type": "text/html; charset=utf-8", Allow: "GET, HEAD", ...SECURITY });
  res.end("<h1>405 — Method Not Allowed</h1>");
}

// Last line of defence: nothing a visitor sends may take the process down.
// Any unexpected throw becomes a 404 (or a dropped connection if the reply had begun).
function guard(res, fn) {
  try {
    fn();
  } catch {
    if (res.headersSent) res.destroy();
    else notFound(res);
  }
}

http
  .createServer((req, res) => guard(res, () => {
    // A static site only ever needs to be read.
    if (req.method !== "GET" && req.method !== "HEAD") return methodNotAllowed(res);

    // strip query string, prevent directory traversal
    let urlPath;
    try {
      urlPath = decodeURIComponent((req.url || "/").split("?")[0]);
    } catch {
      return notFound(res); // malformed %-escape: a thrown URIError here would kill the process
    }
    // A NUL byte (%00) makes every fs call throw synchronously — refuse it up front.
    if (urlPath.includes("\0")) return notFound(res);
    if (urlPath === "/") urlPath = "/index.html";
    const safePath = path.normalize(urlPath).replace(/^(\.\.[/\\])+/, "");

    // Block dotfiles (.git, .env, .gitignore …) and named infra files.
    const segments = safePath.split(/[/\\]/).filter(Boolean);
    const lower = segments.map((s) => s.toLowerCase());
    if (
      lower.some((s) => s.startsWith(".")) ||
      BLOCKED_DIRS.has(lower[0]) ||
      BLOCKED.has(lower[lower.length - 1])
    ) {
      return notFound(res);
    }

    let filePath = path.join(ROOT, safePath);
    // Whatever the path tricks, the resolved file must sit inside this folder.
    if (!filePath.startsWith(ROOT + path.sep)) return notFound(res);

    fs.stat(filePath, (err, stat) => guard(res, () => {
      // pretty URLs: /menu -> /menu.html
      if (err || stat.isDirectory()) {
        const withHtml = filePath.replace(/\/$/, "") + ".html";
        try {
          stat = fs.statSync(withHtml);
          filePath = withHtml;
        } catch {
          return notFound(res);
        }
        if (stat.isDirectory()) return notFound(res);
      }
      const ext = path.extname(filePath).toLowerCase();
      const type = TYPES[ext];
      if (!type) return notFound(res); // unknown/no extension: not site content

      // Weak ETag from size + mtime: browsers and Cloudflare revalidate for free,
      // so photos can be swapped under the same filename and still refresh within a day.
      const etag = `W/"${stat.size.toString(36)}-${Math.floor(stat.mtimeMs).toString(36)}"`;
      const cacheControl =
        ext === ".html"
          ? "no-cache" // pages: always revalidate (menu/price changes show up immediately)
          : segments[0] === "assets"
            ? "public, max-age=86400, stale-while-revalidate=604800" // photos: 1 day, then refresh in background
            : "public, max-age=300";
      const headers = {
        "Content-Type": type,
        ETag: etag,
        "Last-Modified": stat.mtime.toUTCString(),
        "Cache-Control": cacheControl,
        ...SECURITY,
      };
      if (req.headers["if-none-match"] === etag) {
        res.writeHead(304, headers);
        return res.end();
      }
      // Content-Length is required by strict crawlers (Apple/iMessage link previews)
      // to render social cards; a chunked/no-length response degrades to a plain card.
      res.writeHead(200, { ...headers, "Content-Length": String(stat.size) });
      if (req.method === "HEAD") return res.end();
      // A file that vanishes mid-read must not become an unhandled stream error.
      fs.createReadStream(filePath).on("error", () => res.destroy()).pipe(res);
    }));
  }))
  .listen(PORT, () => console.log(`Winchester Grill site live on :${PORT}`));
