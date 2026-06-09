// Minimal zero-dependency static file server for Railway / Nixpacks.
// Serves the files in this folder. Railway sets PORT; falls back to 8080 locally.
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
  ".ico": "image/x-icon",
  ".json": "application/json",
  ".webmanifest": "application/manifest+json",
  ".txt": "text/plain; charset=utf-8",
};

http
  .createServer((req, res) => {
    // strip query string, prevent directory traversal
    let urlPath = decodeURIComponent((req.url || "/").split("?")[0]);
    if (urlPath === "/") urlPath = "/index.html";
    const safePath = path
      .normalize(urlPath)
      .replace(/^(\.\.[/\\])+/, "");
    let filePath = path.join(ROOT, safePath);

    fs.stat(filePath, (err, stat) => {
      // pretty URLs: /menu -> /menu.html
      if (err || stat.isDirectory()) {
        const withHtml = filePath.replace(/\/$/, "") + ".html";
        if (fs.existsSync(withHtml)) {
          filePath = withHtml;
        } else {
          res.writeHead(404, { "Content-Type": "text/html; charset=utf-8" });
          res.end("<h1>404 — Not Found</h1>");
          return;
        }
      }
      const ext = path.extname(filePath).toLowerCase();
      const type = TYPES[ext] || "application/octet-stream";
      res.writeHead(200, {
        "Content-Type": type,
        "Cache-Control": ext === ".html" ? "no-cache" : "public, max-age=86400",
      });
      fs.createReadStream(filePath).pipe(res);
    });
  })
  .listen(PORT, () => console.log(`Winchester Grill site live on :${PORT}`));
