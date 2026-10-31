const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const site = path.resolve(__dirname, '../site');
const html = fs.readFileSync(path.join(site, 'labs/oslofjord-bathavner/index.html'), 'utf8');
const overlay = fs.readFileSync(path.join(site, 'labs/oslofjord-bathavner/environment-cards.js'), 'utf8');
const overlayData = [...overlay.matchAll(/fetch\('([^']+)'\)/g)].map(match => match[1]);
const assets = [...html.matchAll(/(?:src|href)="([^"]+\.(?:js|json))"/g)]
  .map(match => match[1]).filter(url => !/^https?:/.test(url));
for (const route of ['/labs/oslofjord-bathavner', '/labs/oslofjord-bathavner/', '/labs/oslofjord-bathavner/index.html']) {
  test(`local scripts and model links resolve from ${route}`, () => {
    assert.ok(assets.some(asset => asset.endsWith('capacity-filter.js')));
    assert.ok(assets.some(asset => asset.endsWith('environment-cards.js')));
    for (const asset of [...assets, ...overlayData]) {
      const url = new URL(asset, `https://example.org${route}`);
      assert.ok(fs.existsSync(path.join(site, url.pathname)), `Missing deployed asset: ${url.pathname}`);
    }
  });
}
