import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {openDB,exportData,restore} from '../lib/store.mjs';
import {applyOperation,head,personView} from '../lib/domain.mjs';
import {renderPerson} from '../lib/render.mjs';
import {canonical} from '../lib/archive.mjs';

function change(id,kind,data,extra={}) {
  return {id,kind,data,expectedVersion:null,disposition:'recorded',rationale:'Syntetiskt testunderlag',...extra};
}
const basis=object=>({object,version:1,role:'supports'});
test('en gemensam händelses preciseringar visas oförändrade för alla deltagare',t=> {
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-event-detail-'));t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
  const db=openDB(path.join(dir,'db.sqlite'),{create:true});t.after(()=>db.close());
  applyOperation(db,{id:'event-detail',actor:'test',reason:'Två personer delar samma registreringsuppgift',changes:[
    change('S','source',{title:'Test',description:'Syntetiskt testunderlag'}),
    ...['P1','P2'].map(id=>change(id,'person',{display_name:id},{evidence:[basis('S')]})),
    change('E','event',{event_type:'registered_departure',date_json:{precision:'year',value:'1856',literal:'1856'},place_role:'registered_departure_place'},{evidence:[basis('S')]}),
    ...['P1','P2'].map(id=>change('EP-'+id,'participation',{event_id:'E',person_id:id,role:'departing'},{evidence:[basis('S')]})),
    change('F','fact',{subject_id:'E',property:'registration',value_type:'structured',value_json:{outgoing:7,incoming:6}},{evidence:[basis('S')],caveat:'Postnumren avser två skilda registreringar.'})
  ]});
  const a=personView(db,'P1'),b=personView(db,'P2');
  assert.equal(a.events[0].qualifications?.[0]?.object_id,'F');
  assert.deepEqual(a.events[0].qualifications,b.events[0].qualifications);
  assert.match(renderPerson(b),/Postnumren avser två skilda registreringar/);
});
test('läsvyn bevarar skilda förbehåll, bedömningar, ursprung och väntande omprövning',t=> {
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-view-'));t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
  const db=openDB(path.join(dir,'db.sqlite'),{create:true});t.after(()=>db.close());
  const source=change('S','source',{title:'Test',description:'Äldre läsning'});
  applyOperation(db,{id:'view',actor:'test',reason:'Syntetiskt',changes:[source,
    change('P','person',{display_name:'Exempel'},{evidence:[basis('S')],disposition:'accepted'}),
    change('E','event',{event_type:'birth',date_json:{precision:'year',value:'1877',literal:'1877'},place_role:'registered_parish'},
      {disposition:'accepted',evidenceStatus:'TRANSCRIBED',caveat:'Hemvist är inte förlossningsplats.',rationale:'Händelsens motivering',evidence:[basis('S')]}),
    change('EP','participation',{event_id:'E',person_id:'P',role:'child'},
      {disposition:'candidate',caveat:'Deltagaridentiteten är osäker.',rationale:'Deltagarens motivering',evidence:[basis('S')]}),
    change('Q','question',{subject_id:'P',title:'Vilken plats?',outcome:'ÖPPEN.',body:'Behöver prövas.'},
      {caveat:'Frågeförbehåll',evidence:[basis('S')]})]});
  applyOperation(db,{id:'source-correction',actor:'test',reason:'Ny läsning',changes:[{...source,expectedVersion:1,data:{...source.data,description:'Ny läsning'}}]});
  applyOperation(db,{id:'question-rewording',actor:'test',reason:'Ny formulering stänger inte en omprövning',changes:[
    change('Q','question',{subject_id:'P',title:'Vilken födelseplats?',outcome:'ÖPPEN.',body:'Behöver fortfarande prövas.'},
      {expectedVersion:1,caveat:'Frågeförbehåll',evidence:[{...basis('S'),version:2}]})]});
  const view=personView(db,'P'),event=view.events[0];
  assert.equal(event.caveat,'Hemvist är inte förlossningsplats.');
  assert.equal(event.participation.caveat,'Deltagaridentiteten är osäker.');
  assert.equal(event.disposition,'accepted');assert.equal(event.participation.disposition,'candidate');
  assert.equal(event.evidence_status,'TRANSCRIBED');
  for(const o of [view.person,event,event.participation,view.questions[0]]) {
    assert.ok(o.rationale);assert.equal(o.pending_reviews.length,1);assert.ok(o.evidence.length);assert.ok(Array.isArray(o.origins));
  }
  const text=renderPerson(view);
  for(const phrase of ['Hemvist är inte förlossningsplats.','Deltagaridentiteten är osäker.','Händelsens motivering','Deltagarens motivering','Frågeförbehåll','Omprövning väntar','S@1','candidate','TRANSCRIBED'])assert.ok(text.includes(phrase),phrase);
});
test('transaktioner, versionskonflikt, oföränderlig evidens, beroenden och återställning',t=> {
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-domain-'));t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
  const db=openDB(path.join(dir,'db.sqlite'),{create:true});t.after(()=>db.close());
  const source=change('S','source',{title:'Test',archive_reference:null,source_class:null,description:'Syntetisk källa'});
  const record=change('R','record',{source_id:'S',record_type:'test',locator:'post 1',dependence_note:''});
  const person=change('P','person',{display_name:'Exempel',sex:null,legacy_state:null},{evidence:[basis('R')]});
  const obs=change('O','observation',{record_id:'R',mention_id:null,property:'age',value_literal:'27/28',value_json:{selected:null,alternatives:[27,28]}},{evidence:[basis('R')]});
  const fact=change('F','fact',{subject_id:'P',property:'age',value_type:'number',value_json:27},{evidence:[basis('O')],disposition:'candidate'});
  const question=change('Q','question',{subject_id:'P',title:'Hur gammal?',outcome:'ÖPPEN',body:'Åldern är osäker.'},{evidence:[basis('F')]});
  const initial={id:'create',actor:'test',reason:'Syntetiskt',changes:[source,record,person,obs,fact,question]};
  assert.equal(applyOperation(db,initial).changes,6);
  assert.equal(applyOperation(db,initial).unchanged,true);
  assert.throws(()=>applyOperation(db,{...initial,reason:'Annat'}),/annat innehåll/);
  assert.throws(()=>db.exec("UPDATE observation SET value_literal='28'"),/oföränderlig/);
  assert.throws(()=>db.exec("DELETE FROM revision WHERE object_id='O'"),/oföränderlig/);
  const correction={id:'correct',actor:'test',reason:'Ny läsning',changes:[{...obs,expectedVersion:1,data:{...obs.data,value_literal:'28',value_json:{selected:28}}}]};
  applyOperation(db,correction);
  assert.equal(head(db,'O').version,2);
  assert.equal(db.prepare("SELECT value_literal FROM observation WHERE revision_id='O@1'").get().value_literal,'27/28');
  assert.deepEqual(db.prepare('SELECT affected_revision_id FROM pending_review ORDER BY affected_revision_id').all().map(r=>r.affected_revision_id),['F@1','Q@1']);
  assert.equal(head(db,'F').disposition,'candidate');
  assert.throws(()=>applyOperation(db,{...correction,id:'stale'}),/Versionskonflikt/);
  const before=canonical(exportData(db));
  assert.throws(()=>applyOperation(db,{id:'fail-last',actor:'test',reason:'Test rollback',changes:[change('S2','source',source.data),change('bad','record',{...record.data,source_id:'missing'})]}),/Fel referens/);
  assert.equal(canonical(exportData(db)),before);
  assert.throws(()=>applyOperation(db,{id:'type-error',actor:'test',reason:'Fel datatyp',changes:[change('bad','record',{...record.data,source_id:'P'})]}),/Fel referens/);
  assert.throws(()=>applyOperation(db,{id:'bad-date',actor:'test',reason:'Ogiltig dag',changes:[change('E','event',{event_type:'birth',date_json:{precision:'exact',value:'1900-02-30',literal:'30/2'},place_id:null,place_role:''},{evidence:[basis('R')]})]}),/datum/);
  assert.throws(()=>applyOperation(db,{id:'unbounded',actor:'test',reason:'Fel noll',changes:[change('N','search',{source_id:'S',question_id:null,scope_json:{description:'hela boken',query:'namn'},outcome:'negative',body:''},{evidence:[basis('R')]})]}),/sökgränser/);
  const requests=db.prepare('SELECT id FROM pending_review').all();
  applyOperation(db,{id:'review',actor:'test',reason:'Prövning redovisad',changes:[],resolve:requests.map(r=>({request:r.id,rationale:'Syntetiskt test: tidigare kandidat kvarstår tills mer underlag finns.'}))});
  assert.equal(db.prepare('SELECT count(*) n FROM pending_review').get().n,0);
  const data=exportData(db),dest=path.join(dir,'restored.sqlite');restore(data,dest);
  const restored=openDB(dest);assert.equal(canonical(exportData(restored)),canonical(data));restored.close();
});

test('kandidater/avvisanden är skilda från accepterad identitet; ägarkunskap nedgraderas inte',t=> {
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-identity-'));t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
  const db=openDB(path.join(dir,'db.sqlite'),{create:true});t.after(()=>db.close());
  const apply=(id,changes)=>applyOperation(db,{id,actor:'test',reason:'Syntetiskt',changes});
  apply('setup',[
    change('S','source',{title:'Test',archive_reference:null,source_class:null,description:''}),
    change('R','record',{source_id:'S',record_type:'test',locator:'1',dependence_note:''}),
    ...['P1','P2'].map(id=>change(id,'person',{display_name:id,sex:null,legacy_state:null},{evidence:[basis('R')]})),
    change('M','mention',{record_id:'R',name_literal:'Johan',role_literal:'barn'},{evidence:[basis('R')]}),
    change('I1','identity',{mention_id:'M',person_id:'P1',decision:'accepted'},{disposition:'accepted',evidence:[basis('M')]}),
    change('I2','identity',{mention_id:'M',person_id:'P2',decision:'rejected'},{disposition:'rejected',evidence:[basis('M')]}),
    change('OWNER','fact',{subject_id:'P1',property:'birth_date',value_type:'date',value_json:{precision:'exact',value:'1963-11-27',literal:'ägaren'}},{evidenceStatus:'OWNER_CONFIRMED',evidence:[basis('R')]})
  ]);
  assert.throws(()=>apply('two-accepted',[change('I2','identity',{mention_id:'M',person_id:'P2',decision:'accepted'},{expectedVersion:1,disposition:'accepted',evidence:[basis('M')]})]),/två accepterade/);
  assert.equal(head(db,'I2').disposition,'rejected');
  assert.throws(()=>apply('downgrade',[change('OWNER','fact',{subject_id:'P1',property:'birth_date',value_type:'date',value_json:{precision:'unknown',literal:'?' }},{expectedVersion:1,evidenceStatus:'LEAD',evidence:[basis('R')]})]),/Ägarkunskap/);
});
