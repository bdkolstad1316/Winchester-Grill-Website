// Minimal zero-dependency static file server for Railway / Nixpacks.
// Serves the files in this folder. Railway sets PORT; falls back to 8080 locally.
// build marker: 2026-07-18 (retrigger after transient Railway orchestrator failure)
const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = process.env.PORT || 8080;
const ROOT = __dirname;

// ── THE TOGGLE ──────────────────────────────────────────────────────────────
// true  = visitors to winchestergrill.com see the "coming soon" holding page
// false = visitors see the full site (index.html)
// Override without editing code by setting a COMING_SOON env var in Railway.
const COMING_SOON = process.env.COMING_SOON
  ? process.env.COMING_SOON === "true"
  : true;
// ─────────────────────────────────────────────────────────────────────────────

const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
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
    // plausible.io is allowlisted for privacy-friendly analytics (script + event POSTs).
    "script-src 'self' 'unsafe-inline' https://plausible.io; " +
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; " +
    "font-src 'self' https://fonts.gstatic.com; " +
    "img-src 'self' data:; " +
    "connect-src 'self' https://plausible.io; frame-ancestors 'self'; base-uri 'self'; form-action 'self'",
};

// Never serve infrastructure / source files, or any dotfile (blocks .git, .env, etc.).
const BLOCKED = new Set(["server.js", "package.json", "package-lock.json", ".gitignore"]);

function notFound(res) {
  res.writeHead(404, { "Content-Type": "text/html; charset=utf-8", ...SECURITY });
  res.end("<h1>404 — Not Found</h1>");
}

http
  .createServer((req, res) => {
    // strip query string, prevent directory traversal
    let urlPath = decodeURIComponent((req.url || "/").split("?")[0]);
    // Root path: serve the holding page when COMING_SOON is on, else the real site.
    // (index.html and every other page stay directly reachable for previewing.)
    if (urlPath === "/") urlPath = COMING_SOON ? "/coming-soon.html" : "/index.html";
    const safePath = path.normalize(urlPath).replace(/^(\.\.[/\\])+/, "");

    // Block dotfiles (.git, .env, .gitignore …) and named infra files.
    const segments = safePath.split(/[/\\]/).filter(Boolean);
    if (segments.some((s) => s.startsWith(".")) || BLOCKED.has(path.basename(safePath))) {
      return notFound(res);
    }

    let filePath = path.join(ROOT, safePath);

    fs.stat(filePath, (err, stat) => {
      // pretty URLs: /menu -> /menu.html
      if (err || stat.isDirectory()) {
        const withHtml = filePath.replace(/\/$/, "") + ".html";
        if (fs.existsSync(withHtml)) {
          filePath = withHtml;
        } else {
          return notFound(res);
        }
      }
      const ext = path.extname(filePath).toLowerCase();
      const type = TYPES[ext] || "application/octet-stream";
      // Content-Length is required by strict crawlers (Apple/iMessage link previews)
      // to render social cards; a chunked/no-length response degrades to a plain card.
      let size;
      try {
        size = fs.statSync(filePath).size;
      } catch {
        return notFound(res);
      }
      res.writeHead(200, {
        "Content-Type": type,
        "Content-Length": String(size),
        // Short asset cache while we're actively swapping photos; raise before launch.
        "Cache-Control": ext === ".html" ? "no-cache" : "public, max-age=300",
        ...SECURITY,
      });
      fs.createReadStream(filePath).pipe(res);
    });
  })
  .listen(PORT, () => console.log(`Winchester Grill site live on :${PORT}`));
