import fs from 'node:fs';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {DatabaseSync} from 'node:sqlite';
import {exportData} from '../../genealogy2/lib/store.mjs';
import {canonical} from '../../genealogy2/lib/archive.mjs';
const p='evaluations/T-0228', names=['operation-v1','retain-resolutions-v2'];
const ids=names.map(n=>JSON.parse(fs.readFileSync(`${p}/${n}.json`)).id);
const live=new DatabaseSync('genealogy2/data/research.sqlite',{readOnly:true});
const stage=new DatabaseSync('evaluations/T-0228/clone/final-stage.sqlite',{readOnly:true});
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const a=exportData(live),b=exportData(stage);
for(const x of [a,b]) {
 const seen=[];
 for(const row of x.tables.operation) if(ids.includes(row.id)){seen.push(row.id);row.recorded_at='EXACT_TWO_OPERATION_TIMESTAMPS_ONLY';}
 assert.deepEqual(seen.sort(),[...ids].sort());
}
assert.equal(a.format,b.format);assert.equal(a.schemaHash,b.schemaHash);
assert.equal(sha(canonical(a)),sha(canonical(b)),'Full table export differs beyond two recorded_at fields');
assert.equal(live.prepare('select count(*) n from pending_review').get().n,0);
assert.equal(live.prepare('select max(sequence) n from operation_payload').get().n,497);
const result={task:'T-0228',verified_at:new Date().toISOString(),journal_head:497,pending:0,all_exported_tables_equal:true,table_count:Object.keys(a.tables).length,native_json_array_order_preserved:true,normalized_fields_only:ids.map(id=>({table:'operation',id,field:'recorded_at'})),normalized_export_sha256:sha(canonical(a)),live_file_sha256:sha(fs.readFileSync('genealogy2/data/research.sqlite')),stage_file_sha256:sha(fs.readFileSync('evaluations/T-0228/clone/final-stage.sqlite'))};
fs.writeFileSync(`${p}/root-actual-stage-equality-v1.json`,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result));live.close();stage.close();
