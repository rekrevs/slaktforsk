import fs from 'node:fs';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {DatabaseSync} from 'node:sqlite';
import {exportData} from '../../genealogy2/lib/store.mjs';
import {canonical} from '../../genealogy2/lib/archive.mjs';
const p='evaluations/T-0826';
const [stagePath,expectedHead,...operationPaths]=process.argv.slice(2);
assert.ok(stagePath && expectedHead && operationPaths.length,'stagePath expectedHead operations required');
const ids=operationPaths.map(n=>JSON.parse(fs.readFileSync(n)).id);
assert.equal(new Set(ids).size,ids.length);
const live=new DatabaseSync('genealogy2/data/research.sqlite',{readOnly:true});
const stage=new DatabaseSync(stagePath,{readOnly:true});
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const a=exportData(live),b=exportData(stage);
for(const x of [a,b]) {
 const seen=[];
 for(const row of x.tables.operation) if(ids.includes(row.id)){seen.push(row.id);row.recorded_at='EXACT_REVIEWED_OPERATION_TIMESTAMPS_ONLY';}
 assert.deepEqual(seen.sort(),[...ids].sort());
}
assert.equal(a.format,b.format);assert.equal(a.schemaHash,b.schemaHash);
assert.equal(sha(canonical(a)),sha(canonical(b)),'Full table export differs beyond reviewed operation recorded_at fields');
assert.equal(live.prepare('select count(*) n from pending_review').get().n,0);
assert.equal(live.prepare('select max(sequence) n from operation_payload').get().n,Number(expectedHead));
const result={task:'T-0826',verified_at:new Date().toISOString(),journal_head:Number(expectedHead),pending:0,all_exported_tables_equal:true,table_count:Object.keys(a.tables).length,native_json_array_order_preserved:true,normalized_fields_only:ids.map(id=>({table:'operation',id,field:'recorded_at'})),normalized_export_sha256:sha(canonical(a)),live_file_sha256:sha(fs.readFileSync('genealogy2/data/research.sqlite')),stage_file_sha256:sha(fs.readFileSync(stagePath))};
fs.writeFileSync(`${p}/root-actual-stage-equality-v1.json`,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result));live.close();stage.close();
