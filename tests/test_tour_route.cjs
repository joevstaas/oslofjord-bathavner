const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.resolve(__dirname, '../site/labs/oslofjord-bathavner');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const municipalities = JSON.parse(fs.readFileSync(path.join(root, 'data/municipalities.geojson')));
const harbours = JSON.parse(fs.readFileSync(path.join(root, 'data/harbours.geojson')));
const routeCode = html.slice(html.indexOf('const ROUTE ='), html.indexOf('const $ ='));
const buildCode = html.slice(html.indexOf('function buildTour()'), html.indexOf('function caption(s)'));
function harness(largeOnly = false) {
  const grouped = {};
  for (const feature of harbours.features) {
    const p = feature.properties;
    const h = grouped[p.hid] ||= {mun:p.mun, name:p.name, area:0, best:feature};
    h.area += p.area;
    if (p.area > h.best.properties.area) h.best = feature;
  }
  const context = {M:municipalities, H:harbours, harbours:grouped, stops:[], largeOnly, isMobile:false,
    hasLargeCapacity:h => (h.best.properties.capacity?.count ?? 0) >= 200,
    bearingTo:() => 0, updateProg:() => {},
    maplibregl:{LngLat:{convert:coordinates => ({distanceTo:other => Math.hypot(coordinates[0]-other.coordinates[0],coordinates[1]-other.coordinates[1])*100000, coordinates})}}};
  vm.createContext(context);
  vm.runInContext(routeCode + buildCode, context);
  return context;
}
test('unfiltered tour visits all 23 mapped municipalities exactly once, plus return', () => {
  const c = harness();
  c.buildTour();
  const names = c.stops.filter(s => !s.home).map(s => s.name);
  assert.equal(names.length, 23);
  assert.equal(new Set(names).size, 23);
  assert.deepEqual(names.slice().sort(), municipalities.features.map(f => f.properties.name).sort());
  assert.equal(c.stops.filter(s => s.home).length, 1);
  assert.equal(c.stops.at(-1).home, true);
  assert.equal(c.tourProgress(c.stops, -1).total, 23);
  assert.equal(c.tourProgress(c.stops, 23).current, 23);
});
test('new municipalities are included without editing route order', () => {
  const c = harness();
  const names = c.tourMunicipalities([...municipalities.features.map(f => f.properties), {name:'Ny kommune'}]);
  assert.equal(names.length, 24);
  assert.equal(names.at(-1), 'Ny kommune');
});
test('capacity-filtered tour counts only municipalities with matching harbours', () => {
  const c = harness(true);
  c.buildTour();
  const expected = new Set(Object.values(c.harbours).filter(c.hasLargeCapacity).map(h => h.mun));
  assert.deepEqual(c.stops.filter(s => !s.home).map(s => s.name).sort(), [...expected].sort());
  assert.equal(c.tourProgress(c.stops, c.stops.length-1).current, expected.size);
  assert.equal(c.tourProgress(c.stops, 0).total, expected.size);
});
