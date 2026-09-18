// Recreate the one historical operation that predates the durable journal.
// Uses only committed inputs; never edits the production database or receipts.
import fs from 'node:fs';
import path from 'node:path';
import {openDB,importBaseline,exportData,restore} from './store.mjs';
import {applyOperation} from './domain.mjs';
import {canonical,sha} from './archive.mjs';

export const PILOT_HISTORY=Object.freeze({
  id:'T-0641/pilot-v1',
  requestHash:'dc68b9b81c178b2b7d123c6a6a5ee3e95b4bfe6fc5a8e2b833e8ed11256d2908',
  recordedAt:'2026-09-16T12:59:35.193Z',
});

export function bootstrapFromFiles(root,destination) {
  if(fs.existsSync(destination)||fs.existsSync(destination+'.restoring'))throw Error('Bootstrap kräver ett nytt mål');
  const request=JSON.parse(fs.readFileSync(path.join(root,'genealogy2/operations/T-0641-pilot-v1.json'),'utf8'));
  if(request.id!==PILOT_HISTORY.id||sha(canonical(request))!==PILOT_HISTORY.requestHash)throw Error('Pilotpaketet matchar inte den bevarade historiken');
  const db=openDB(':memory:',{create:true});
  try {
    importBaseline(db,path.join(root,'genealogy2/import/baseline'));
    applyOperation(db,request,{legacy:true,recordedAt:PILOT_HISTORY.recordedAt});
    const data=exportData(db);
    if(data.tables.operation.length!==1||data.tables.operation_payload.length!==1)throw Error('Oväntad bootstrapbas');
    // The accepted historical database has no receipt for this operation.
    // Adapt an in-memory recovery export, not any immutable live table.
    // Subsequent journal sequence 1 must still be available.
    data.tables.operation_payload=[];
    return restore(data,destination);
  }finally{db.close();}
}
