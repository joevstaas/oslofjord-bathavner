const { test } = require('node:test');
const assert = require('node:assert/strict');
require('../site/labs/oslofjord-bathavner/capacity-filter.js');
const { matches } = globalThis.CapacityFilter;
test('published boundary inclusive and takes precedence over estimates', () => {
  assert.equal(matches({capacity: {count:199}, capacity_estimate:{category:'likely_ge_200',high:600}}, 'possible'), false);
  assert.equal(matches({capacity:{count:200}}), true);
  assert.equal(matches({}), false);
});
test('estimates require opt in and uncertain intervals stay distinct', () => {
  const likely = {capacity_estimate:{category:'likely_ge_200',high:600}};
  const uncertain = {capacity_estimate:{category:'uncertain',high:200}};
  assert.equal(matches(likely), false);
  assert.equal(matches(likely,'likely'), true);
  assert.equal(matches(uncertain,'likely'), false);
  assert.equal(matches(uncertain,'possible'), true);
  assert.equal(matches({capacity_estimate:{category:'uncertain',high:199}},'possible'), false);
});
