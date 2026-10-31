/* Optional, source-attributed overlay; independent of approved harbour geometry. */
window.EnvironmentCards = (() => {
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const tx = value => window.I18n?.text(value) ?? value;
  const tr = value => esc(tx(value));
  const labels = {opplyst_etablert:'Opplyst etablert',rutine_publisert:'Rutine publisert',ukjent:'Ukjent i gjennomgåtte kilder',påstand_uten_målerapport:'Påstand uten målerapport',kildeavvik:'Kildeavvik',under_etablering_opplyst:'Under etablering, ifølge operatør',opplyst_tilgang:'Tilgang opplyst'};
  let features = [], openCard = () => {}, state = 'loading', menuElement = null, activeId = null, mapInstance = null, optionsInstance = null;
  function source(s) {
    try { const url = new URL(s.url); if (url.protocol !== 'https:') return esc(s.title);
      return `<a href="${esc(url.href)}" target="_blank" rel="noopener">${esc(s.publisher)}: ${esc(s.title)} ↗</a>`;
    } catch { return esc(s.title); }
  }
  function render(p) {
    const refs = ids => ids.map(id => `<a href="#${esc(p.id)}-${esc(id)}">[${esc(id)}]</a>`).join(' ');
    const summary = p.presentation;
    return `<div class="top"><h3 tabindex="-1" id="environment-title">${esc(p.name)}</h3><button class="x" aria-label="${tr('Lukk miljøkort')}" onclick="window.__closeCard()">×</button></div>
      <section class="enrichment" lang="${window.I18n?.language || 'nb'}"><h4>${tr('Miljøkort')}</h4><p>${tr('Kildeopplysninger · kontrollert')} ${esc(p.reviewed_utc.slice(0,10))}</p>
      <dl class="environment-summary">${summary.rows.map(([label, text]) => `<dt>${tr(label)}</dt><dd>${tr(text)}</dd>`).join('')}</dl>
      <p class="environment-next"><b>${tr('Neste avklaring')}</b><br>${tr(summary.next_question)}</p>
      <details class="environment-evidence"><summary>${tr('Kilder og grunnlag')}</summary>
      <p>${tr('Ingen befaring eller direkte operatørbekreftelse. Ukjent betyr ikke at tiltak mangler. Ingen målt økologisk effekt er dokumentert.')}</p>
      <h4>${tr('Regelverk')}</h4><p>${tr('Forskriftsforslag under revisjon. Om anlegget omfattes, og om krav oppfylles, er ikke vurdert.')}</p>
      ${(p.regulatory_context?.sources || []).map(source).join('<br>')}
      <p>${tr('Kildetitler, avsnittsnavn og opprinnelige kartleggingsnotater beholdes på originalspråket.')}</p>
      <h4>${tr('Plassering og omfang')}</h4><p>${tr(p.map_link.note)} ${refs(p.map_link.source_ids)}</p>
      ${p.observations.map(o => `<details class="fact"><summary>${tr(o.topic)} — ${tr(labels[o.status] || o.status)}</summary><p>${tr(o.claim)} ${refs(o.source_ids)}</p><p>${tr('Omfang:')} ${tr(o.scope)}</p><p><b>${tr('Dokumentasjonshull:')}</b> ${tr(o.missing_evidence)}</p><p><b>${tr('Neste steg:')}</b> ${tr(o.next_action)}</p><small>${tr('Finn avsnitt:')} ${esc(o.source_locator)}</small></details>`).join('')}
      ${p.relations.length ? `<h4>${tr('Delte tjenester')}</h4>${p.relations.map(r => `<p>${tr(r.target)} — ${tr(r.status.replaceAll('_',' '))}. ${tr(r.note || '')} ${refs(r.source_ids)}</p>`).join('')}` : ''}
      <h4>${tr('Kilder')}</h4>${p.sources.map(s => `<div class="fact" id="${esc(p.id)}-${esc(s.id)}"><b>[${esc(s.id)}]</b> ${source(s)}<small>${tr(s.source_type)} · ${tr('Dokumentdato:')} ${esc(s.published_or_updated || tx('unknown'))} · ${tr('Hentet:')} ${esc(s.retrieved_utc.slice(0,10))}</small></div>`).join('')}
      <p>${tr('Ingen henvendelse er sendt.')}</p></details></section>`;
  }
  function links(hid) {
    return features.filter(f => f.properties.map_link.harbour_ids.includes(hid)).map(f => `<section class="enrichment"><button type="button" data-environment-id="${esc(f.properties.id)}">${tr('Miljøkort')}: ${esc(f.properties.name)}</button><p>${tr('Gjelder et bestemt anlegg eller en tjeneste i området; se kortets omfang.')}</p></section>`).join('');
  }
  async function init(map, options) {
    mapInstance = map; optionsInstance = options;
    openCard = id => { activeId = id; const f = features.find(x => x.properties.id === id); if (f) options.open(f, render(f.properties)); };
    const menu = document.createElement('details'); menuElement = menu; menu.id = 'environment-menu'; menu.className = 'glass'; renderMenu(); document.body.append(menu);
    document.addEventListener('click', e => { const button = e.target.closest('[data-environment-id]'); if (!button) return; menu.open = false; openCard(button.dataset.environmentId); });
    try {
      const response = await fetch('/labs/oslofjord-bathavner/data/environment-cards.json'); if (!response.ok) throw new Error('Unavailable');
      const data = await response.json();
      if (data.schema_version !== 1 || data.type !== 'FeatureCollection' || !Array.isArray(data.features) || !data.features.length || !data.features.every(f => f.geometry?.type === 'Point' && f.geometry.coordinates.length === 2 && f.geometry.coordinates.every(Number.isFinite) && f.properties?.map_link && Array.isArray(f.properties.map_link.harbour_ids) && Array.isArray(f.properties.observations) && Array.isArray(f.properties.sources) && Array.isArray(f.properties.relations) && Array.isArray(f.properties.presentation?.rows) && typeof f.properties.presentation.next_question === 'string')) throw new Error('Invalid overlay');
      features = data.features; state = 'ready';
      renderMenu();
      // Keep nested card properties out of MapLibre's flattened feature properties.
      map.addSource('environment', {type:'geojson',data:{type:'FeatureCollection',features:features.map(f => ({type:'Feature',geometry:f.geometry,properties:{id:f.properties.id,name:f.properties.name}}))}});
      map.addLayer({id:'environment-points',type:'circle',source:'environment',minzoom:9,paint:{'circle-radius':8,'circle-color':'#b8cbea','circle-stroke-color':'#172a40','circle-stroke-width':2}});
      map.addLayer({id:'environment-labels',type:'symbol',source:'environment',minzoom:13,layout:{'text-field':tx('Miljøkort'),'text-size':11,'text-offset':[0,1.6]},paint:{'text-color':'#fff','text-halo-color':'#172a40','text-halo-width':2}});
      map.on('click','environment-points',e => { e.originalEvent?.stopPropagation(); openCard(e.features[0].properties.id); });
      map.on('mouseenter','environment-points',() => { map.getCanvas().style.cursor='pointer'; });
      map.on('mouseleave','environment-points',() => { map.getCanvas().style.cursor=''; });
      options.ready?.();
    } catch { state = 'unavailable'; features = []; renderMenu(); }
  }
  function renderMenu() {
    if (!menuElement) return;
    const summary = `<summary>${window.I18n?.t('environment.menu') || 'Miljøkort'}${state === 'ready' ? ` · ${features.length}` : ''}</summary>`;
    menuElement.innerHTML = summary + (state === 'ready'
      ? `<p>${tr('Stedspunkter, ikke miljøvurdering av hele havnen.')}</p>${features.map(f => `<button type="button" data-environment-id="${esc(f.properties.id)}">${esc(f.properties.name)}</button>`).join('')}`
      : `<p>${tr(state === 'loading' ? 'Laster miljøkort…' : 'Miljøkortene kunne ikke lastes. Last siden på nytt for å prøve igjen. Havnekartet kan fortsatt brukes.')}</p>`);
  }
  function refreshLanguage() {
    renderMenu();
    if (state === 'ready') mapInstance?.setLayoutProperty?.('environment-labels','text-field',tx('Miljøkort'));
    if (document.getElementById?.('environment-title') && activeId) {
      const feature = features.find(f => f.properties.id === activeId);
      if (feature) optionsInstance?.update?.(render(feature.properties));
    }
  }
  return {init, links, refreshLanguage, get state() {return state;}};
})();
