import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {openDB} from '../../lib/store.mjs';
// Read-only canonical DB. Only this verification report is written; no apply,
// native mutation, source rereading, Wotan status or archive writes.
const dir=path.dirname(new URL(import.meta.url).pathname);
const root=path.resolve(dir,'../../..');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const scope=read(path.join(dir,'scope.json'));
const starts=read(path.join(dir,'start-records.json'));
const backlog=read(path.join(root,'wotan/backlog.json'));
const db=openDB(path.join(root,'genealogy2/data/research.sqlite'),{readOnly:true});
const all=(s,...a)=>db.prepare(s).all(...a),one=(s,...a)=>db.prepare(s).get(...a);
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const errors=[],warnings=[];
const journal=all('select sequence,operation_id,request_json from operation_payload where sequence>=119 order by sequence').filter(x=>x.operation_id.startsWith('T-0675/'));
const ops=new Map(journal.map(x=>[x.operation_id,x.sequence]));
const cur=id=>one('select * from revision where object_id=? order by version desc limit 1',id);
const latestSQL='r.version=(select max(version) from revision where object_id=r.object_id)';
const aud=all(`select a.*,r.object_id,r.version,r.operation_id,r.caveat,r.disposition from assessment a join revision r on r.id=a.revision_id where ${latestSQL} and a.criteria in ('original_revision/1','original_verification/1')`).filter(x=>ops.has(x.operation_id));
const trs=all(`select t.*,r.object_id,r.version,r.operation_id,r.caveat from transcription t join revision r on r.id=t.revision_id where ${latestSQL}`).filter(x=>ops.has(x.operation_id));
const locks=fs.readdirSync(dir).filter(n=>/initial.*\.json$/.test(n)).map(name=>{
 const bytes=fs.readFileSync(path.join(dir,name));const sha=hash(bytes);
 const candidates=[name+'.sha256',name.replace(/\.json$/,'.sha256')].filter(n=>fs.existsSync(path.join(dir,n)));
 const stored=candidates.map(n=>({file:n,text:fs.readFileSync(path.join(dir,n),'utf8')}));
 const match=stored.length?stored.some(x=>x.text.includes(sha)):null;
 if(match===false)errors.push('LOCK_HASH_MISMATCH '+name);
 return {file:name,sha256:sha,hashSidecars:stored.map(x=>x.file),hashMatches:match,recordIdentifiers:scope.members.records.filter(id=>bytes.toString('utf8').includes(id))};
});
// Explicit packet mapping for locks whose raw payload intentionally omits model record ids.
const explicitLocks={21:['root-degerfors1064-first-initial.json','degerfors1064-second-initial.json'],30:['kalmar-census-first-initial.json','kalmar-census-second-initial.json'],49:['root-dn-first-initial.json','dn-second-initial.json']};
const checked=new Map();
function fileCheck(p,expected,bytes){
 if(checked.has(p))return checked.get(p);
 const full=path.resolve(root,p);let r={path:p,expected_sha256:expected};
 if(!fs.existsSync(full)){r.exists=false;errors.push('MISSING_ASSET '+p);}else{const b=fs.readFileSync(full);r={...r,exists:true,sha256:hash(b),bytes:b.length,hashMatches:expected?hash(b)===expected:null,sizeMatches:bytes==null?null:b.length===bytes};if(r.hashMatches===false||r.sizeMatches===false)errors.push('ASSET_INTEGRITY '+p);}
 checked.set(p,r);return r;
}
function evidence(rev){return all('select basis_revision_id,role,note from dependency where revision_id=?',rev);}
const rows=scope.records.map(s=>{
 const r=cur(s.record);const rec=one('select * from record where revision_id=?',r.id);
 const assets=all('select a.*,ra.region from record_asset ra join asset a on a.path=ra.asset_path where ra.revision_id=?',r.id);
 const media=all('select a.*,rm.region from record_media rm join native_asset a on a.id=rm.asset_id where rm.revision_id=?',r.id);
 const baseline=starts.find(x=>x.object===s.record);const prior=baseline.revisions.at(-1);
 const lostAssets=(prior.assets??[]).filter(a=>!assets.some(b=>b.path===a.path&&b.region===a.region));
 const lostMedia=(prior.nativeAssets??[]).filter(a=>!media.some(b=>b.id===a.id&&b.region===a.region));
 if(lostAssets.length||lostMedia.length)errors.push('LOST_START_ASSETS '+s.record);
 const aa=aud.filter(x=>x.subject_id===s.record),tt=trs.filter(x=>x.record_id===s.record);
 const hasReview=aa.length>0&&tt.length>0;
 if(!hasReview)errors.push('NO_APPLIED_FULL_REVIEW scope'+s.number+' '+s.record);
 const details=aa.map(a=>({id:a.object_id,version:a.version,outcome:a.outcome,disposition:a.disposition,journal:ops.get(a.operation_id),operation:a.operation_id,body:a.body,caveat:a.caveat,evidence:evidence(a.revision_id)}));
 const transcriptions=tt.map(t=>({id:t.object_id,version:t.version,journal:ops.get(t.operation_id),operation:t.operation_id,reading_note:t.reading_note,sha256:hash(t.text),evidence:evidence(t.revision_id)}));
 const connectedText=[...aa.map(x=>x.body+' '+x.caveat),...tt.map(x=>x.text+' '+x.reading_note)].join('\n');
 const lockLinks=locks.filter(l=>connectedText.includes(l.sha256)||connectedText.includes(l.file)||l.recordIdentifiers.includes(s.record)||(explicitLocks[s.number]??[]).includes(l.file)).map(l=>l.file);
 if(hasReview&&!lockLinks.length)warnings.push('LOCK_REFERENCE_NOT_MACHINE_LINKED scope'+s.number);
 for(const t of transcriptions){const e=t.evidence.find(e=>e.basis_revision_id.startsWith(s.record+'@'));if(!e)errors.push('TR_NO_RECORD_DEPENDENCY '+t.id);else if(e.basis_revision_id!==r.id)warnings.push('TR_HISTORICAL_RECORD_VERSION '+t.id+' '+e.basis_revision_id+' current '+r.id);}
 const citations=[...new Set(s.origins.map(o=>o.document_path.match(/C-\d+/)?.[0]).filter(Boolean))];
 return {number:s.number,record:s.record,startVersion:s.version,currentVersion:r.version,recordDisposition:r.disposition,recordType:rec.record_type,locator:rec.locator,source:rec.source_id,citations,disposition:hasReview?'applied_bounded_review':'awaiting_applied_review',audits:details,transcriptions,lockedReadingReferences:lockLinks,lockedReadingLinkMethod:explicitLocks[s.number]?'explicit bounded packet mapping':'native hash/file reference or record-id in locked payload',assets:assets.map(a=>({...fileCheck(a.path,a.sha256,a.bytes),region:a.region})),nativeMedia:media.map(a=>({id:a.id,...fileCheck(a.storage_path,a.sha256,a.bytes),region:a.region,provenance:a.provenance})),startAssetsPreserved:!lostAssets.length&&!lostMedia.length,lostAssets,lostMedia};
});
const imported=scope.members.imported_assets.map(p=>{
 const a=one('select * from asset where path=?',p);if(!a){errors.push('UNREGISTERED_FIXED_ASSET '+p);return{path:p,registered:false};}
 const links=rows.filter(r=>r.assets.some(a=>a.path===p)).map(r=>r.number);
 if(!links.length)warnings.push('FIXED_ASSET_NO_TARGET_RECORD_LINK '+p);
 return {...fileCheck(p,a.sha256,a.bytes),scopeRecords:links};
});
const taskFor=cohort=>backlog.tasks.filter(t=>(t.summary??'').includes(cohort+':')).map(t=>({task:t.id,status:t.status}));
const cross=scope.cross_references.map(x=>({...x,owners:taskFor(x.cohort),coverageClaim:'Cross-reference only; no full citation/source/other-record completion inferred from target-row audit.'}));
for(const x of cross)if(!x.owners.length)warnings.push('CROSS_REFERENCE_NO_WOTAN_OWNER '+x.cohort+' '+x.entity);
const citationCoverage=scope.members.citations.map(c=>({citation:c,recordNumbers:rows.filter(r=>r.citations.includes(c)).map(r=>r.number),limit:'Only scoped records and their relevant own fields; citation-wide claims excluded unless expressly within fixed scope.'}));
const fullPageOwnership=imported.map(a=>({asset:a.path,targetRecordNumbers:a.scopeRecords,otherCurrentRecords:all(`select ra.revision_id,ra.region from record_asset ra join revision r on r.id=ra.revision_id where ra.asset_path=? and ${latestSQL}`,a.path).filter(x=>!scope.members.records.includes(x.revision_id.split('@')[0])).map(x=>({...x,explicitCrossReference:cross.find(c=>c.entity===x.revision_id.split('@')[0])??null})),limit:'Full image retained; rows of unrelated persons are not automatically extracted or approved.'}));
const pending=all('select q.* from review_request q where not exists(select 1 from review_resolution r where r.request_id=q.id)').filter(q=>ops.has(q.operation_id));
if(pending.length)warnings.push('PENDING_T0675_REVIEWS '+pending.length);
if(rows.length!==50||citationCoverage.length!==24||imported.length!==35)errors.push('FIXED_SCOPE_COUNT_MISMATCH');
const applied=rows.filter(r=>r.disposition==='applied_bounded_review').length;
const report={task:'T-0675',cohort:'G023',generatedAt:new Date().toISOString(),databaseAccess:'readOnly',baseline:'scope.json + start-records.json',journalFrom:119,journalThrough:one('select max(sequence) as n from operation_payload').n,scopeCounts:{records:rows.length,citations:citationCoverage.length,importedAssets:imported.length},appliedRecords:applied,awaitingRecords:rows.filter(r=>r.disposition!=='applied_bounded_review').map(r=>r.number),status:errors.length?'GAPS_FOUND':'STRUCTURAL_COVERAGE_COMPLETE',notASubstantiveApproval:'Audit outcomes/reservations are reproduced, not promoted. This script proves bounded structural coverage and preservation, not correctness of glyphs, person contracts, ancestry, exhaustion or full-page ownership.',errors,warnings,records:rows,citations:citationCoverage,importedAssets:imported,crossReferences:cross,fullPageOwnership,lockedReadings:locks,journal:journal.map(x=>({sequence:x.sequence,operation:x.operation_id,changes:JSON.parse(x.request_json).changes?.length??0})),pendingReviews:pending};
fs.writeFileSync(path.join(dir,'coverage.json'),JSON.stringify(report,null,2)+'\n');db.close();
console.log(JSON.stringify({status:report.status,journalThrough:report.journalThrough,appliedRecords:applied,awaitingRecords:report.awaitingRecords,counts:report.scopeCounts,errors,warnings}));
process.exitCode=errors.length?1:0;
