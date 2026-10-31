const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const code=fs.readFileSync(path.join(root,'site/labs/oslofjord-bathavner/environment-cards.js'),'utf8');
const data=JSON.parse(fs.readFileSync(path.join(root,'site/labs/oslofjord-bathavner/data/environment-cards.json')));
function harness(response, language) {
 const menu={innerHTML:'',open:false},handlers={},added=[];
 const context={window:{},URL,document:{createElement:()=>menu,body:{append(){}},addEventListener:(type,handler)=>handlers[type]=handler},fetch:async()=>response};
 if (language) { context.Event=Event; vm.runInNewContext(fs.readFileSync(path.join(root,'site/labs/oslofjord-bathavner/i18n.js'),'utf8'),context); context.window.I18n.setLanguage(language); }
 vm.runInNewContext(code,context);
 const map={addSource:(...args)=>added.push(['source',...args]),addLayer:(...args)=>added.push(['layer',...args]),on(){},getCanvas:()=>({style:{}})};
 return {api:context.window.EnvironmentCards,map,menu,handlers,added};
}
test('six independent markers, contextual links, and attributed rendered cards',async()=>{
 const h=harness({ok:true,json:async()=>data});let rendered='';
 await h.api.init(h.map,{open:(f,html)=>rendered=html});
 assert.equal(h.api.state,'ready');assert.equal(h.added.filter(x=>x[0]==='source').length,1);
 assert.equal(h.added[0][2].data.features.length,6);
 assert.match(h.api.links('0301-H13'),/Lille Herbern/);assert.equal(h.api.links('unknown'),'');
 h.handlers.click({target:{closest:()=>({dataset:{environmentId:'MK-02'}})}});
 assert.match(rendered,/Kildeavvik/);assert.match(rendered,/Dokumentasjonshull/);assert.match(rendered,/rel="noopener"/);
});
for(const response of [{ok:false},{ok:true,json:async()=>({schema_version:999})}]){
 test('missing or malformed overlay leaves base map untouched',async()=>{
  const h=harness(response);await h.api.init(h.map,{open(){}});
  assert.equal(h.api.state,'unavailable');assert.equal(h.added.length,0);
  assert.match(h.menu.innerHTML,/Havnekartet kan fortsatt brukes/);assert.equal(h.api.links('0301-H13'),'');
 });
}

test('English environmental cards render translated summaries and evidence',async()=>{
 const h=harness({ok:true,json:async()=>data},'en');let rendered='';
 await h.api.init(h.map,{open:(f,html)=>rendered=html});
 assert.match(h.menu.innerHTML,/Environmental cards/);
 h.handlers.click({target:{closest:()=>({dataset:{environmentId:'MK-01'}})}});
 assert.match(rendered,/Wash water/);assert.match(rendered,/No site visit or direct operator confirmation/);
 assert.match(rendered,/The association describes collection through a sediment trap/);
 assert.match(rendered,/id="MK-01-S01"/);assert.match(rendered,/lang="en"/);
 assert.doesNotMatch(rendered,/undefined/);
});
