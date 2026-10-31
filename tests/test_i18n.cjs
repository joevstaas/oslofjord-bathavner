const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.resolve(__dirname,'../site/labs/oslofjord-bathavner');
const code = fs.readFileSync(path.join(root,'i18n.js'),'utf8');
function harness(storage = new Map()) {
  const changes = [];
  const context = {Event, localStorage:{getItem:key=>storage.get(key),setItem:(key,value)=>storage.set(key,value)}, dispatchEvent:event=>changes.push(event.type)};
  vm.runInNewContext(code,context);
  return {api:context.I18n,changes,storage};
}
test('Norwegian is default regardless of browser preference; English is remembered',()=>{
  const h = harness();
  assert.equal(h.api.language,'nb');
  assert.equal(h.api.t('harbours'),'havner');
  h.api.setLanguage('en');
  assert.equal(h.api.t('harbours'),'harbours');
  assert.equal(h.api.text('Spylevann'),'Wash water');
  assert.equal(harness(h.storage).api.language,'en');
  h.api.setLanguage('nb');
  assert.equal(harness(h.storage).api.language,'nb');
  assert.deepEqual(h.changes,['site-language-change','site-language-change']);
});
test('storage denial and invalid saved values do not break language switching',()=>{
  const context = {Event,localStorage:{getItem(){throw Error('blocked')},setItem(){throw Error('blocked')}}};
  vm.runInNewContext(code,context);
  assert.equal(context.I18n.language,'nb');
  context.I18n.setLanguage('en');
  assert.equal(context.I18n.language,'en');
  context.I18n.setLanguage('invalid');
  assert.equal(context.I18n.language,'en');
  assert.equal(harness(new Map([['oslofjord-language','unknown']])).api.language,'nb');
});
test('all messages have both languages and the same interpolation parameters',()=>{
  const {api} = harness();
  const params=text=>[...text.matchAll(/\{(\w+)\}/g)].map(m=>m[1]).sort();
  for (const [key,entry] of Object.entries(api.messages)) {
    assert.ok(entry.nb && entry.en,key);
    assert.deepEqual(params(entry.nb),params(entry.en),key);
  }
  const html = fs.readFileSync(path.join(root,'index.html'),'utf8');
  for (const match of html.matchAll(/data-i18n(?:-(?:aria-label|title|placeholder|content))?="([^"]+)"/g)) assert.ok(api.messages[match[1]],match[1]);
  assert.match(html,/<html lang="nb">/);
});
test('environmental summaries and evidence have explicit English translations',()=>{
  const {api} = harness();api.setLanguage('en');
  const data=JSON.parse(fs.readFileSync(path.join(root,'data/environment-cards.json')));
  for (const f of data.features) {
    const p=f.properties;
    const texts=[...p.presentation.rows.flat(),p.presentation.next_question,p.map_link.note,
      ...p.observations.flatMap(o=>[o.topic,o.claim,o.scope,o.missing_evidence,o.next_action])];
    for (const original of texts) assert.notEqual(api.text(original),original,`${p.id}: ${original}`);
  }
  assert.equal(api.t('stop',{current:2,total:23}),'Stop 2 of 23');
  api.setLanguage('nb');assert.equal(api.t('stop',{current:2,total:23}),'Stopp 2 av 23');
});
