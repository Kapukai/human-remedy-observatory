/* Pure descriptive helpers. No inference or causal estimates. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.RemedyAnalysis = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  function sectorOf(c, alternative = false) { return alternative && c.alternative_sector ? c.alternative_sector : c.sector; }
  function filterCases(cases, selection = {}) {
    const s = {country:'US', sector:'all', technology:'all', search:'', habeas:false, alternative:false, comparator:false, ...selection};
    const search = s.search.toLocaleLowerCase().trim();
    return cases.filter(c => (s.comparator || (c.included_by_default !== false && c.plaintiff !== 'Organization comparator')) &&
      (s.country === 'all' || c.country === s.country) && (s.sector === 'all' || sectorOf(c,s.alternative) === s.sector) &&
      (s.technology === 'all' || c.technology === s.technology) && (!s.habeas || !!c.habeas_vehicle) &&
      (!search || [c.name,c.short,c.summary,c.limit,...(c.tags || [])].join(' ').toLocaleLowerCase().includes(search)));
  }
  function counts(rows, key) {
    const result = {};
    for (const row of rows) { const v = typeof key === 'function' ? key(row) : row[key]; const label = v == null || v === '' ? 'Not recorded' : String(v); result[label] = (result[label] || 0) + 1; }
    return result;
  }
  function jaccard(a, b) {
    const aa = new Set(Array.isArray(a) ? a : (a.tags || []));
    const bb = new Set(Array.isArray(b) ? b : (b.tags || []));
    const union = new Set([...aa, ...bb]);
    if (!union.size) return null;
    return [...aa].filter(x => bb.has(x)).length / union.size;
  }
  function nearestCases(selected, rows) {
    return rows.filter(c=>c.id!==selected.id).map(c=>({case:c,similarity:jaccard(selected,c)}))
      .filter(c=>c.similarity!==null).sort((a,b)=>b.similarity-a.similarity || a.case.name.localeCompare(b.case.name));
  }
  function cramerV(rows, keyA, keyB) {
    const value = (r,k) => typeof k === 'function' ? k(r) : r[k];
    const clean=rows.filter(r=>value(r,keyA)!=null && value(r,keyB)!=null && value(r,keyA)!=='' && value(r,keyB)!=='');
    const a=[...new Set(clean.map(r=>value(r,keyA)))],b=[...new Set(clean.map(r=>value(r,keyB)))],n=clean.length;
    if(!n || a.length<2 || b.length<2) return null;
    const ac=counts(clean,r=>value(r,keyA)),bc=counts(clean,r=>value(r,keyB));
    let chi=0;
    for(const x of a) for(const y of b) { const observed=clean.filter(r=>value(r,keyA)===x && value(r,keyB)===y).length; const expected=ac[x]*bc[y]/n; chi+=(observed-expected)**2/expected; }
    return Math.sqrt(chi/(n*Math.min(a.length-1,b.length-1)));
  }
  function parseCSV(text) {
    const rows=[];let row=[],field='',quoted=false;
    for(let i=0;i<text.length;i++) {
      const c=text[i];
      if(quoted) { if(c==='"' && text[i+1]==='"'){field+='"';i++;}else if(c==='"'){quoted=false;}else field+=c; }
      else if(c==='"') quoted=true;
      else if(c===','){row.push(field);field='';}
      else if(c==='\n'){row.push(field.replace(/\r$/,''));if(row.some(v=>v!==''))rows.push(row);row=[];field='';}
      else field+=c;
    }
    if(quoted) throw new Error('CSV ends within a quoted field');
    if(field!=='' || row.length){row.push(field.replace(/\r$/,''));rows.push(row);}
    if(!rows.length)return [];
    const headers=rows.shift().map((v,i)=>i===0?v.replace(/^\uFEFF/,''):v);
    return rows.map(values=>Object.fromEntries(headers.map((h,i)=>[h,values[i]??''])));
  }
  function toCSV(rows, fields) {
    const quote = value => { let v = value == null ? '' : typeof value === 'object' ? JSON.stringify(value) : String(value); const trimmed=v.trimStart(); if(/^[=+\-@]/.test(trimmed) || /^[\t\r]/.test(v))v="'"+v; return '"'+v.replace(/"/g,'""')+'"'; };
    return [fields.map(quote).join(','),...rows.map(row=>fields.map(f=>quote(row[f])).join(','))].join('\r\n')+'\r\n';
  }
  function parseViewState(query, cases) {
    const params = query instanceof URLSearchParams ? query : new URLSearchParams(query);
    const enumValue = (key,allowed,fallback) => allowed.includes(params.get(key)) ? params.get(key) : fallback;
    const selection = {
      country:enumValue('country',['all','US',...new Set(cases.map(c=>c.country))],'US'),
      sector:enumValue('sector',['all','Public','Private','Mixed'],'all'),
      technology:enumValue('technology',['all','Physical','Administrative','Computerized'],'all'),
      search:(params.get('q') || '').replace(/[\u0000-\u001F\u007F]/g,'').slice(0,500),
      habeas:params.get('habeas')==='1',
      alternative:params.get('alternative')==='1',
      comparator:params.get('comparator')==='1'
    };
    const selected=cases.some(c=>c.id===params.get('case')) ? params.get('case') : cases.some(c=>c.id==='miller_pate') ? 'miller_pate' : cases[0]?.id || '';
    return {view:enumValue('view',['atlas','relationships','corpus','research'],'atlas'),selection,selected};
  }
  function buildViewParams(viewState) {
    const s=viewState.selection;
    const params=new URLSearchParams({view:viewState.view,country:s.country,sector:s.sector,technology:s.technology});
    if(s.search)params.set('q',s.search);
    for(const key of ['habeas','alternative','comparator'])if(s[key])params.set(key,'1');
    if(viewState.selected)params.set('case',viewState.selected);
    return params;
  }
  return {sectorOf,filterCases,counts,jaccard,nearestCases,cramerV,parseCSV,toCSV,parseViewState,buildViewParams};
});
