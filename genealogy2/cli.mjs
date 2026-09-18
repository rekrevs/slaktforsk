#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {snapshot,verifySource} from './lib/archive.mjs';
import {openDB,importBaseline,coverage,verifyDB,search,showLegacy,exportData,restore,backupDB,SCHEMA_VERSION} from './lib/store.mjs';
import {domainStatus,personView,inspect} from './lib/domain.mjs';
import {migrationReport} from './lib/migration.mjs';
import {renderPerson} from './lib/render.mjs';
import {writeOperation,stageMedia,syncJournal,replayJournal,verifyAssets,backupBundle,restoreBundle} from './lib/recovery.mjs';
import {pedigree} from './lib/pedigree.mjs';
import {contextList,contextDocument,renderContextDocument} from './lib/context.mjs';
import {identityGate} from './lib/review.mjs';
import {researchInventory} from './lib/inventory.mjs';
import {renderPersonOverview} from './lib/overview.mjs';
import {findParticipations} from './lib/vocabulary.mjs';

const root=path.resolve(fileURLToPath(new URL('..',import.meta.url)));
const argv=process.argv.slice(2);
function option(name,fallback,resolve=true) {
  const n=argv.indexOf(name);if(n<0)return fallback;
  if(!argv[n+1]||argv[n+1].startsWith('--'))throw Error(`Värde saknas: ${name}`);
  const value=argv[n+1];argv.splice(n,2);return resolve?path.resolve(value):value;
}
try {
  const dbPath=option('--db',path.join(root,'genealogy2/data/research.sqlite'));
  const baseline=option('--baseline',path.join(root,'genealogy2/import/baseline'));
  const source=option('--source',root);
  const requestedFormat=option('--format',null,false);
  const journal=option('--journal',path.join(source,'genealogy2/journal'));
  const provenance=option('--provenance',null,false);
  const group=option('--group',null,false),query=option('--query',null,false);
  const mode=option('--mode','verified',false),role=option('--role',null,false),eventType=option('--event',null,false),personId=option('--person',null,false);
  const fullIndex=argv.indexOf('--full'),full=fullIndex>=0;if(full)argv.splice(fullIndex,1);
  const [command,...args]=argv;
  const format=requestedFormat??(command==='person'?'markdown':'json');
  if(format!=='json'&&!(format==='markdown'&&['person','context'].includes(command)))throw Error('Format ska vara json, eller markdown för person/context');
  let result,db,gate;
  try {
    if(command==='snapshot')result=await snapshot(source,baseline);
    else if(command==='verify-source')result=await verifySource(source,baseline);
    else if(command==='restore')result=restore(JSON.parse(fs.readFileSync(args[0],'utf8')),dbPath);
    else if(command==='restore-bundle')result=await restoreBundle(args[0],args[1]);
    else if(command==='stage-media')result=await stageMedia(source,args[0],provenance);
    else if(['import','migrate','apply','apply-legacy','person','pedigree','inventory','participations','inspect','coverage','status','verify','verify-assets','search','show','context','export','backup','backup-bundle','journal','replay'].includes(command)) {
      db=openDB(dbPath,{create:command==='import',migrate:command==='migrate',readOnly:!['import','migrate','apply','apply-legacy','replay'].includes(command)});
      if(command==='import')result=importBaseline(db,baseline);
      if(command==='migrate')result={schema:SCHEMA_VERSION};
      if(['apply','apply-legacy'].includes(command))result=await writeOperation(db,JSON.parse(fs.readFileSync(args[0],'utf8')),{root:source,journal,legacy:command==='apply-legacy'});
      if(command==='journal')result=syncJournal(db,journal);
      if(command==='replay')result=await replayJournal(db,args[0]??journal,{root:source});
      if(command==='pedigree')result=pedigree(db,args[0],{mode});
      if(command==='person'){
        result=personView(db,args[0]);
        if(!result.person&&!result.legacy.length&&!result.identityMappings.length)throw Error(`Personen eller arkivreferensen saknas: ${args[0]}`);
        if(format==='markdown'&&!full)gate=identityGate(db,args[0]);
      }
      if(command==='inventory'){
        const inventory=researchInventory(db);
        result=full?inventory:{format:inventory.format,note:inventory.note,active:inventory.active,all:inventory.all,detail:'inventory --full visar personer och använda bedömningsrevisioner.'};
      }
      if(command==='participations')result=findParticipations(db,{role,eventType,personId});
      if(command==='inspect')result=inspect(db,args[0]);
      if(command==='coverage') {
        const report=migrationReport(db);
        if(args[0])fs.writeFileSync(args[0],JSON.stringify(report)+'\n',{flag:'wx'});
        result={...report.summary,reportHash:report.reportHash,detail:args[0]??'Ange ny.json för alla enheter och grupper.'};
      }
      if(command==='status')result={legacy:coverage(db),domain:domainStatus(db)};
      if(command==='verify')result=verifyDB(db);
      if(command==='verify-assets')result=await verifyAssets(db,source);
      if(command==='search')result=search(db,args.join(' '));
      if(command==='show')result=showLegacy(db,args[0]);
      if(command==='context'){
        if(format==='markdown'&&!args[0])throw Error('Markdown kräver en exakt dokumentsökväg');
        result=args[0]?contextDocument(db,args[0]):contextList(db,{group,query});
        if(result===null)throw Error(`Dokumentet saknas i importbasen: ${args[0]}`);
      }
      if(command==='export') {
        if(!args[0])throw Error('Ange en ny exportfil');
        fs.writeFileSync(args[0],JSON.stringify(exportData(db))+'\n',{flag:'wx'});result={file:args[0]};
      }
      if(command==='backup') {if(!args[0])throw Error('Ange en ny backupfil');result=await backupDB(db,args[0]);}
      if(command==='backup-bundle') {if(!args[0])throw Error('Ange en ny backupkatalog');result=await backupBundle(db,args[0],{root:source,baseline});}
    }else throw Error('Kommandon: snapshot | import | migrate | apply <operation.json> | apply-legacy <äldre importpaket> | stage-media <fil> --provenance <text> | person <P-id> [--full --format markdown|json] | pedigree <P-id> [--mode verified|typed] | inventory [--full] | participations [--role witness --event baptism --person P-id] | inspect <objekt/A-id> | status | verify | verify-assets | verify-source | search <text> | show <P/S/C-id> | context [importsökväg] [--group grupp --query text --format markdown] | export <ny.json> | restore <export.json> | backup <ny.sqlite> | backup-bundle <ny katalog> | restore-bundle <backup> <ny rot> | journal | replay <journal>. Val: --db --baseline --source --journal.');
    if(format==='markdown'&&command==='person')console.log(full?renderPerson(result):renderPersonOverview(result,{gate}));
    else if(format==='markdown'&&command==='context')process.stdout.write(renderContextDocument(result));
    else if(format==='json')console.log(JSON.stringify(result,null,2));
    else throw Error('Format ska vara json, eller markdown för person/context');
    if(result?.ok===false)process.exitCode=1;
  }finally{db?.close();}
}catch(e){console.error(e.message);process.exitCode=1;}
