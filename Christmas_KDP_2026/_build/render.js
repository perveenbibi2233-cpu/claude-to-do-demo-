// Usage: node render.js <svg_dir> <png_dir> [name ...]
// Renders each SVG at its native pixel size with Chromium (Playwright).
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
(async () => {
  const [src, out, ...only] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const files = fs.readdirSync(src).filter(f => f.endsWith('.svg') && (!only.length || only.includes(f.replace('.svg',''))));
  const browser = await chromium.launch();
  for (const f of files) {
    const svg = fs.readFileSync(path.join(src, f), 'utf8');
    const W = +svg.match(/width="(\d+)"/)[1], H = +svg.match(/height="(\d+)"/)[1];
    const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
    await page.setContent(`<html><body style="margin:0;background:#fff">${svg}</body></html>`);
    await page.screenshot({ path: path.join(out, f.replace('.svg', '.png')), clip: { x: 0, y: 0, width: W, height: H } });
    await page.close();
    console.log('rendered', f, W + 'x' + H);
  }
  await browser.close();
})();
