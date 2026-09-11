'use strict';
const assert = require('node:assert/strict');
const test = require('node:test');
const fs = require('node:fs');
const path = require('node:path');
const A = require('../web/analysis.js');
const cases = JSON.parse(fs.readFileSync(path.join(__dirname, '../data/curated/cases.json'), 'utf8'));

test('default and expanded filters retain documented denominators', () => {
  assert.equal(A.filterCases(cases).length, 57);
  assert.equal(A.filterCases(cases, {country:'all'}).length, 62);
  assert.equal(A.filterCases(cases, {country:'all',comparator:true}).length, 63);
  assert.equal(A.filterCases(cases, {habeas:true}).length, 19);
  assert.equal(A.filterCases(cases, {habeas:true,sector:'Private'}).length, 0);
  assert.equal(A.filterCases(cases, {search:'NONEXISTENT-RESEARCH-CASE-9379'}).length, 0);
});

test('Jaccard similarity uses topics, not outcome or sector', () => {
  assert.equal(A.jaccard([], []), null);
  assert.equal(A.jaccard(['a','b'], ['b','c']), 1/3);
  const first = {id:'a',name:'A',tags:['Evidence'],direction:'Favorable',sector:'Public'};
  const second = {id:'b',name:'B',tags:['Evidence'],direction:'Adverse',sector:'Private'};
  assert.equal(A.nearestCases(first,[first,second])[0].similarity, 1);
  assert.equal(A.jaccard(first,{...second,direction:'Favorable',sector:'Public'}),1);
});

test('descriptive association reproduces frozen atlas and respects missing margins', () => {
  const included = A.filterCases(cases,{country:'all'});
  for(const [field,expected] of Object.entries({stage:0.5283980937272063,technology:0.4279106419365117,direction:0.19843463286694782})) {
    assert.ok(Math.abs(A.cramerV(included,'sector',field)-expected)<1e-12, field);
  }
  assert.equal(A.cramerV([], 'sector','direction'),null);
  assert.equal(A.cramerV(included.filter(c=>c.sector==='Private'),'sector','direction'),null);
});

test('CSV preserves quoted evidence and neutralizes formula cells', () => {
  const rows = [{name:'A, B',note:'A "quoted"\npassage',value:'=1+1'}];
  const parsed=A.parseCSV(A.toCSV(rows,['name','note','value']));
  assert.equal(parsed[0].name,rows[0].name);
  assert.equal(parsed[0].note,rows[0].note);
  assert.equal(parsed[0].value,"'=1+1");
  assert.throws(()=>A.parseCSV('name,note\nA,"unfinished'));
  assert.equal(A.parseCSV(A.toCSV([{value:'  =1+1'}],['value']))[0].value,"'  =1+1");
});

test('saved views round-trip filters and reject unknown values', () => {
  const viewState={view:'relationships',selected:cases[0].id,selection:{country:'all',sector:'Mixed',technology:'all',search:'evidence & remedy',habeas:true,alternative:true,comparator:false}};
  assert.deepEqual(A.parseViewState(A.buildViewParams(viewState),cases),viewState);
  const bad=A.parseViewState('?view=unknown&country=unknown&sector=unknown&technology=unknown&case=missing&habeas=true&q='+('x'.repeat(700)),cases);
  assert.equal(bad.view,'atlas');
  assert.equal(bad.selection.country,'US');
  assert.equal(bad.selection.sector,'all');
  assert.equal(bad.selection.technology,'all');
  assert.equal(bad.selection.habeas,false);
  assert.equal(bad.selection.search.length,500);
  assert.ok(cases.some(c=>c.id===bad.selected));
});
