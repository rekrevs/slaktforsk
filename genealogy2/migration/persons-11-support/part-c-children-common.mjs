export * from './part-c-common.mjs';
import {core,fact,relation,units,section,reuse,whole,subjectFact} from './part-c-common.mjs';
export function childBase(p,bookNames,extra={}){
 const os=whole(p);
 core(p,[section(p,'Identitet')],'Individuellt avgränsad barnidentitet i samma namngivna familj. Egna uppgifter följer en beroende husförhörskedja; broderns födelsepost styrker familjen men ger ingen oberoende egen rad för detta barn. TRANSCRIBED skiljs från accepterad identitet och profilgranskning. Inget separat explicit könsfält har utvunnits; son-/dotterrollerna bevaras utan att fylla sex.',null);
 const house=fact(p,'household_membership','Buberget',{parents:['P-0082','P-0519'],place:'Buberget',parish:'Degerfors',books:bookNames,book_periods_not_own_birth_arrival_or_lifespan:true,no_continuous_physical_presence:true,no_birth_village_inferred:true,servants_not_siblings:true,children_of_Anders_lower_household_not_own_siblings:true,...extra},os);
 const limits=fact(p,'research_limits','own-life',{own_birth_baptism_original_unread:true,own_spouse_children_godparents_unknown:true,own_occupation_education_property_personal_sources_unproved:true,fathers_titles_not_own:true,no_modern_school_level_from_signs:true,smallpox_v_not_disease_or_vaccination_date:true,blank_fields_not_person_negative:true,mother_death1867_not_own_life_point:true,own_death_burial_unknown:p.person!=='P-0527',no_general_military_or_legal_negative:true},os);
 const siblingIds=['P-0065','P-0520','P-0521','P-0522','P-0523','P-0524','P-0525','P-0526','P-0527'].filter(x=>x!==p.person);
 const family=fact(p,'family_context','known-siblings',{siblings:siblingIds,known_sibling_count:8,no_lifetime_total:true,parents:['P-0082','P-0519'],all_relations_from_household_order:true,Anders_own_birth_entry_not_independent_birth_evidence_for_siblings:true},os);
 const targets={};
 for(const u of units(p.person,'person').filter(u=>u.kind==='relation_row'&&!u.historical)){
  const cells=JSON.parse(u.parsed_json).cells;const other=cells[0].match(/P-\d{4}/)?.[0];if(!other)continue;
  if(![...siblingIds,'P-0082','P-0519'].includes(other))throw Error(`Ej individuellt prövad släktkant ${p.person}/${other}`);
  const parent=['P-0082','P-0519'].includes(other),edge=relation(p,parent?other:p.person,parent?p.person:other,parent?'parent':'sibling',[u.id],parent?'recorded_parent':'recorded_sibling');
  const context=subjectFact(p,edge,'source_context',p.person.replace('-',''),{person_row:p.person,reported_relation:cells[1],reported_time_place:cells[2],book_period_not_own_lifespan:true,household_relation_not_unspecified_biological_claim:true},[u.id]);
  targets[other]=[edge,context,house,family,limits];
  if(other==='P-0521')targets[other].push(reuse(p,'F-P-0521-name_form-Eva-rejected',[u.id],'Aktuell Lisa-rättelse gäller även äldre Eva-benämningar i andra syskons relationsrader.'));
  p.relations.push({unit:u.id,state:'mapped_complete',targets:targets[other],rationale:'Egen granskad relationsrad: riktning/art återbrukas, tids-/ortprosans bokgräns kvalificeras utan livslängdsinferens.',question:''});
 }
 reuse(p,`F-P-0065-family_context-sibling-${p.person}`,os);
 reuse(p,`F-P-0082-family_source_assessment-${p.person}`,os);
 reuse(p,'F-P-0519-family_context-nine-known-children',os);
 return{os,house,limits,family,targets};
}
