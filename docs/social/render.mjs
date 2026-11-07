// Render a poster HTML to PNG with the toolbox Chromium and run its in-page validator.
// usage: node render.mjs poster1.html poster1.png
import pw from 'playwright-core';
const { chromium } = pw;
import { writeFileSync } from 'node:fs';
const [,, html, png] = process.argv;
const browser = await chromium.launch({ headless: true, chromiumSandbox: false, args: ['--no-sandbox', '--disable-gpu', '--font-render-hinting=none'] });
const page = await browser.newPage({ viewport: { width: 1200, height: 1500 }, deviceScaleFactor: 2 });
await page.goto('file://' + process.cwd() + '/' + html);
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(300);
const report = await page.evaluate(() => window.__validate());
await page.screenshot({ path: png, fullPage: false });
writeFileSync(png.replace(/\.png$/, '.validation.json'), JSON.stringify(report, null, 2));
const bad = report.textOverlaps.length + report.edgeCrossings.length + report.edgeHitsBox.length + report.textOutside.length + report.overflow.length;
console.log(JSON.stringify({ png, counts: report.counts, textOverlaps: report.textOverlaps.length, edgeCrossings: report.edgeCrossings.length, edgeHitsBox: report.edgeHitsBox.length, textOutside: report.textOutside.length, overflow: report.overflow.length, verdict: bad ? 'FAIL' : 'PASS' }));
if (bad) console.log(JSON.stringify(report, null, 1).slice(0, 3000));
await browser.close();
