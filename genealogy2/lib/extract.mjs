import {sha} from './archive.mjs';
export const EXTRACTOR='markdown-verbatim/1';

// No rendered Markdown: retain escapes, links, comments and all exact spans.
export function cells(line) {
  const out=[]; let cell='', escaped=false, code=0;
  for(let i=1;i<line.length;i++) {
    const c=line[i];
    if(c==='`'&&!escaped) {
      let n=1; while(line[i+n]==='`')n++;
      if(!code)code=n; else if(code===n)code=0;
      cell+='`'.repeat(n); i+=n-1; escaped=false; continue;
    }
    if(c==='|'&&!escaped&&!code) {out.push(cell.trim());cell='';} else cell+=c;
    if(c==='\\')escaped=!escaped;else escaped=false;
  }
  if(cell.trim())out.push(cell.trim());
  return out;
}

export function extract(file,text) {
  const bytes=Buffer.from(text);
  const entityMatch=file.path.match(/^genealogy\/(people|sources|citations|research-profiles)\/([PSC]-\d{4})(?:[-.]|$)/);
  const kinds={people:'person',sources:'source',citations:'citation','research-profiles':'profile'};
  const entity=entityMatch ? {id:entityMatch[2],kind:kinds[entityMatch[1]],title:text.match(/^# (.+)$/m)?.[1]??entityMatch[2]} : null;
  const owner=entity?.id??null;
  const lines=[]; let byte=0;
  for(const raw of text.match(/[^\n]*\n|[^\n]+$/g)??[]) {
    lines.push({raw,line:raw.replace(/\r?\n$/,''),start:byte}); byte+=Buffer.byteLength(raw);
  }
  const units=[]; let section='', fence=null; const headings=[];
  function add(kind,start,end,legacyId=null,parsed={},historic=false,title=section) {
    const begin=lines[start].start, finish=end<lines.length?lines[end].start:byte;
    const raw=bytes.subarray(begin,finish).toString('utf8');
    units.push({id:sha(`${file.path}\0${file.sha256}\0${kind}\0${begin}`),document_path:file.path,kind,legacy_id:legacyId,owner_id:owner,section:title,start_byte:begin,end_byte:finish,start_line:start+1,end_line:end,raw,parsed_json:JSON.stringify(parsed),historical:historic?1:0});
  }
  for(let i=0;i<lines.length;i++) {
    const s=lines[i].line;
    const fm=s.match(/^\s*(`{3,}|~{3,})/);
    if(fm) {if(!fence)fence=fm[1];else if(fm[1][0]===fence[0]&&fm[1].length>=fence.length)fence=null; continue;}
    if(fence)continue;
    const heading=s.match(/^(#{1,6})\s+(.+)/);
    if(heading) {
      headings.push({i,level:heading[1].length,title:heading[2]});
      if(heading[1].length===2)section=heading[2];
    }
    if(s.startsWith('|')) {
      const c=cells(s);
      if(!c.length||c.every(x=>/^:?-+:?$/.test(x)))continue;
      const historical=/historik|rättelser/i.test(section);
      const aid=/^A-\d{4}$/.test(c[0])?c[0]:null;
      const kind=aid?'assertion':section==='Relationer'?'relation_row':'table_row';
      add(kind,i,i+1,aid,{cells:c},historical);
    }
  }
  for(let n=0;n<headings.length;n++) {
    const h=headings[n];
    if(h.level===1)continue; // The full document is already preserved separately.
    const next=headings.slice(n+1).find(x=>x.level<=h.level)?.i??lines.length;
    let kind='section',legacyId=null;
    const q=h.title.match(/^(Q-\d+|KP-\d+)(?::|\s)/);
    if(entity?.kind==='profile'&&q) {kind=q[1].startsWith('Q-')?'question':'source_path';legacyId=owner+'/'+q[1];}
    const fields={};
    for(let i=h.i+1;i<next;i++) {
      const m=lines[i].line.match(/^- ([^:]+):\s*(.*)$/); if(m)fields[m[1]]=m[2];
    }
    add(kind,h.i,next,legacyId,{heading:h.title,level:h.level,fields},/historik|rättelser/i.test(h.title),h.title);
  }
  return {entity,units};
}
