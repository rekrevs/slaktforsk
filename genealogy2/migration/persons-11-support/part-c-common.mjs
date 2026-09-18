export * from './genealogy2-persons11-combined.mjs';
import {units,origins,src,event,exact,fact,add} from './genealogy2-persons11-combined.mjs';
export const whole=p=>[origins(p.person,'person',1,Math.max(...units(p.person,'person').map(u=>u.end_line)))];
export const books={
 AI3:{c:'C-1072',r:'R-dcab035cc525fa01b6631828',page:262,period:'1825–1835'},
 AI4:{c:'C-0872',r:'R-ee9afd95459534c05d5e3e8d',page:310,period:'1836–1842'},
 AI5:{c:'C-0872',r:'R-8e70b63bdefd0550e21eba3c',page:16,period:'1843–1847'},
 AI6:{c:'C-0869',r:'R-efca6e283ff6a0bd4048e02e',page:474,period:'1848–1857'},
 AI7:{c:'C-1055',r:'R-b0e359298b9139018c7eff63',page:400,period:'1858–1860'},
 AI8:{c:'C-0869',r:'R-ac67b2b327159ad11e766cc6',page:536,period:'1861–1865'},
 AI9:{c:'C-0064',r:'R-6be04582ec19e700c612f06c',page:85,period:'1866–1876'}
};
export const own=(p,b,name,role,data,os,caveat='')=>src(p,books[b].c,'',b+'-own',name,role,data,os,caveat+' Endast denna persons avgränsade rad. Bokperioden är inte ett eget närvaro-/flyttintervall.','accepted',books[b].r);
export function communion(p,dates,os,caveat){return dates.flatMap(d=>{const id=`E-church-P${p.person.slice(2)}-${d}`;const es=event(p,'other',exact(d),os,'Bokförd egen nattvardsnotering. '+caveat,null,'TRANSCRIBED',id);const f=fact(p,'church_activity',d,{activity:'communion',event:id,date:d},os);return[...es,f];});}
export function subjectFact(p,subject,property,key,value,os,status='TRANSCRIBED',caveat=''){return add(p,`F-${subject}-${property}-${key}`,'fact',{subject_id:subject,property,value_type:'structured',value_json:value},os,[],caveat,status);}
