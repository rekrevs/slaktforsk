import json
def rows(q,args=()):return [dict(r) for r in connection.execute(q,args)]
def existing(oid,version):
 rev=rows('select * from current_revision where object_id=?',(oid,))[0];assert rev['version']==version
 kind=rev['kind'];data=rows('select * from '+kind+' where revision_id=?',(rev['id'],))[0];data.pop('revision_id')
 for k,v in data.items():
  if k.endswith('_json') and v is not None:data[k]=json.loads(v)
 return {'id':oid,'kind':kind,'expectedVersion':version,'data':data,'origins':[{'unit':r['unit_id'],'coverage':r['coverage'],'note':r['note']} for r in rows('select * from origin where revision_id=?',(rev['id'],))],'evidence':[{'object':r['basis_revision_id'].rsplit('@',1)[0],'version':int(r['basis_revision_id'].rsplit('@',1)[1]),'role':r['role'],'note':r['note']} for r in rows('select * from dependency where revision_id=?',(rev['id'],))],'disposition':rev['disposition'],'evidenceStatus':rev['evidence_status'],'rationale':rev['rationale'],'caveat':rev['caveat']}
