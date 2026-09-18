import assert from 'node:assert/strict';
import {readCurrent, personView} from '../lib/domain.mjs';

// Independently chosen cases from complete dossiers and cited textual records.
// These expected dates, limits and roles are not generated from the review packet.
export function checkPersons09PartARisks(db) {
  const r = id => {const x = readCurrent(db,id); assert.ok(x,id); return x;};
  const v = id => JSON.parse(r(id).value_json);
  const d = id => JSON.parse(r(id).date_json);
  const participants = id => db.prepare('SELECT p.* FROM current_revision c JOIN participation p ON p.revision_id=c.id WHERE p.event_id=?').all(id);
  const parents = id => db.prepare("SELECT x.* FROM current_revision c JOIN relation x ON x.revision_id=c.id WHERE x.relation_type='parent' AND x.to_person=? AND c.disposition='accepted'").all(id);
  let groups=0;

  // These three identities have one own source post each, despite repeated readings.
  for(const id of ['P-0404','P-0405','P-0406']) {
    assert.equal(r(id).evidence_status,'TRANSCRIBED');
    assert.equal(r(id).disposition,'accepted');
  }
  groups++;

  // C0492 leaves Anna Adelia's own birthplace cell blank; the 1910 census says här.
  assert.equal(d('E-birth-P-0401').value,'1902-06-19');
  const adelia=v('F-P-0401-birth_assessment-date-versus-place');
  assert.equal(adelia.household_birth_place_cell,''); assert.equal(adelia.census_place_literal,'här');
  assert.equal(v('F-P-0401-source_assessment-own-life-limits').given_names_count,2);
  assert.equal(v('F-P-0401-source_assessment-own-life-limits').own_presence1916_proven,false);
  for(const id of ['P-0401','P-0402']) {
    assert.equal(r(id).disposition,'accepted');
    const qs=personView(db,id).research.questions;
    assert.ok(qs.length>0); assert.ok(qs.every(q=>q.active===false));
  }
  groups++;

  // C0506 has two adults and three child rows. A separate 1824 birth adds no fourth row.
  const brita=v('F-P-0402-source_assessment-own-life-limits');
  assert.equal(brita.household_children,3); assert.equal(brita.household_rows,5);
  assert.equal(brita.birth_place_cell_unresolved,true);
  assert.equal(brita.parents_communion_oct1824_not_own_life_anchor,true);
  assert.equal(brita.crossing_proves_move_or_death,false);
  assert.equal(r('F-P-0402-kinship_hypothesis-P0058').disposition,'candidate');
  assert.equal(readCurrent(db,'REL-sibling-P-0058-P-0402'),null);
  const britaWitnesses=participants('E-baptism-P-0402').filter(x=>x.role==='witness');
  assert.equal(britaWitnesses.length,8); assert.ok(britaWitnesses.every(x=>x.person_id===null));
  assert.equal(r('M-P-0402-C0506-witness-wife-olof').name_literal,'');
  groups++;

  // C0853's Nils, born 2 August to Jon Nilsson, is not Nils Pehrsson born 19 July.
  assert.equal(d('E-birth-P-0403').value,'1802-07-19');
  assert.equal(v('O-P-0403-C0853-other').birth,'1802-08-02');
  assert.equal(r('ID-P-0403-C0853-other').decision,'rejected');
  assert.equal(r('ID-P-0403-C0853-other').disposition,'rejected');
  const nilsSearch=r('SEARCH-P-0403-C0853-1802');
  assert.equal(nilsSearch.outcome,'negative');
  assert.deepEqual(JSON.parse(nilsSearch.scope_json).bounds.images,['C0033076_00169','C0033076_00173']);
  assert.equal(parents('P-0403').length,0); groups++;

  // C0509 has no h.-prefix before the mother; h/2 in C0510 belongs to a different woman.
  assert.equal(r('M-P-0404-C0509-mother').role_literal,'');
  assert.equal(v('O-P-0404-C0509-mother').age,25);
  assert.equal(d('E-birth-P-0404').precision,'unknown');
  assert.equal(v('F-P-0404-source_assessment-own-life-limits').approximate_birth_year,1811);
  assert.equal(v('F-P-0404-source_assessment-own-life-limits').death_before1844_or1855_proven,false);
  assert.equal(readCurrent(db,'REL-spouse-P-0403-P-0404'),null);
  assert.equal(r('REL-step-P-0405-P-0315').nature,'recorded_step_parent');
  assert.ok(parents('P-0315').every(x=>x.from_person!=='P-0405'));
  assert.equal(r('M-P-0405-C0510-own').name_literal,'Lisa Stina Jonsd:r');
  assert.equal(v('F-P-0405-marriage_assessment-raw-year').known_marriage_year,null);
  assert.equal(v('F-P-0405-source_assessment-own-fields').age_at_last_anchor,53);
  groups++;

  // The forty-day interval is from a registered banns date, not a proven wedding day.
  const lisa=v('F-P-0406-source_assessment-own-life-limits');
  assert.equal(lisa.registered_interval_days,40); assert.equal(lisa.actual_parent_wedding_day_unknown,true);
  assert.equal(lisa.own_lifespan_four_weeks_proven,false); assert.equal(lisa.year1858_destination_unresolved,true);
  assert.equal(lisa.own_Sattna1862_presence_proven,false);
  assert.equal(d('E-registered_departure-P-0406').precision,'year'); groups++;

  // C0512 contains four child rows; their unextracted cells are not blank cells.
  for(const id of ['P-0407','P-0408','P-0409','P-0410']) {
    const x=v(`F-${id}-source_assessment-household-limits`);
    assert.equal(x.children_in_core_transcription,4); assert.equal(x.unextracted_means_blank,false);
    assert.equal(x.crossing_proves_death_or_move,false); assert.equal(x.uncrossed_proves_residence_to1900,false);
    assert.equal(x.extracts_independent_of_church_series,false);
    assert.deepEqual(x.GB131_search_pages,[129,138]); assert.equal(x.GB131_negative_whole_volume,false);
  }
  assert.deepEqual(v('F-P-0410-source_assessment-household-limits').dated_census_years,[1890,1900]);
  assert.equal(readCurrent(db,'ID-P-0410-C0388-own'),null); r('O-P-0410-C0388-absence');
  assert.equal(r('M-P-0409-C0388-own').name_literal,'Katharina Petronella');
  assert.equal(r('M-P-0409-C0389-own').name_literal,'Kattar. Petronella'); groups++;

  // C0521 source father is in conflict with the mother's documented April 1849 marriage.
  assert.equal(d('E-birth-P-0411').value,'1849-07-05');
  assert.equal(d('E-baptism-P-0411').value,'1849-07-08');
  const alleged=r('REL-parent-P-0453-P-0411');
  assert.equal(alleged.disposition,'candidate'); assert.equal(alleged.evidence_status,'CONFLICT');
  assert.deepEqual(parents('P-0411').map(x=>x.from_person),['P-0413']);
  const conflict=v('F-P-0411-parentage_assessment-Olo-Fredric');
  assert.equal(conflict.mother_marriage,'1849-04-15'); assert.equal(conflict.biological_father,null);
  assert.equal(conflict.two_Anna_women_hypothesis_not_excluded,true);
  assert.equal(conflict.Olaus_parents_not_inferred,true);
  assert.ok(parents('P-0336').every(x=>!['P-0413','P-0453','P-0466'].includes(x.from_person)));
  groups++;

  // C0322 says five own children and places Johannes in family 2 as a nephew.
  const children=v('F-P-0411-family_context-five-children');
  assert.deepEqual(children.children.map(x=>x.name),['Augusta Fredrika','Hugo','Karl','Esther','Gertrud Elisabet']);
  assert.equal(children.nephew1900_family_number,2); assert.equal(children.full_or_half_brother_unresolved,true);
  assert.equal(v('F-P-0411-source_assessment-coverage-and-corrections').C0322_derived_from_C0323,true);
  assert.equal(v('F-P-0411-residence-bounded-anchors').own_arrival1895_12_31_proven,false); groups++;

  // C0645's 75 26/9 and C0323's 20 September must survive even in previously migrated P0396.
  assert.equal(v('O-P-0411-C0645-Augusta').birth_literal,'75 26/9');
  assert.equal(v('O-P-0411-C0323-Augusta').birth,'1875-09-20');
  const oldFamily=r('F-P-0396-family_context-Hudiksvall'); assert.equal(oldFamily.version,2);
  const cousins=JSON.parse(oldFamily.value_json).cousins;
  assert.deepEqual(cousins[0].reported_birth,{C0323:'1875-09-20',C0645:'1875-09-26',chosen:null});
  assert.equal(Object.hasOwn(cousins[0],'birth'),false); assert.equal(cousins[0].birth_parish,'Alnö');
  assert.deepEqual(cousins.slice(1).map(x=>x.name),['Hugo','Karl','Esther','Gertrud Elisabet']);
  assert.ok(oldFamily.origins.some(x=>x.document_path.includes('C-0645'))); groups++;

  // The archived Andris reading is not a person, an alias, a father or an active research programme.
  assert.equal(readCurrent(db,'P-0412'),null);
  assert.equal(r('IMPORT-P-0412').version,1);
  const archive=personView(db,'P-0412');
  assert.equal(archive.person,null); assert.equal(archive.relations.length,0); assert.equal(archive.events.length,0);
  assert.equal(archive.identities.length,0); assert.ok(archive.research.questions.length>0);
  assert.ok(archive.research.questions.every(q=>q.active===false)); groups++;

  // C0688's later addition leaves afl.53 unresolved, with distinct book/year negatives.
  const afl=v('F-P-0413-residence-afl53');
  assert.deepEqual(afl.meaning_unresolved,['afflyttad','afliden']);
  assert.equal(afl.confirmed_departure1853,false); assert.equal(afl.confirmed_death1853,false);
  assert.equal(d('E-marriage-P-0413-P-0466-1849').value,'1849-04-15');
  assert.equal(r('REL-spouse-P-0413-P-0453').disposition,'candidate');
  assert.equal(r('ID-P-0413-C0797-Anna').decision,'rejected');
  assert.equal(r('M-C0797-Anna').name_literal,'Anna Britta Svensdotter');
  assert.equal(JSON.parse(r('SEARCH-P-0336-death1853').scope_json).bounds.year,1853);
  assert.equal(r('SEARCH-P-0336-Anna-marriage-api').outcome,'inconclusive'); groups++;

  // C0600 gives Anna Lovisa a piga title and birth year only. Johannes is her husband's nephew.
  assert.equal(r('M-P-0414-C0600-bride').role_literal,'piga');
  const wedding=v('O-P-0414-C0600-bride'); assert.equal(wedding.birth_year,1845);
  assert.equal(Object.hasOwn(wedding,'birth_place'),false); assert.equal(Object.hasOwn(wedding,'birth'),false);
  assert.equal(d('E-marriage-P-0411-P-0414-1874').value,'1874-12-12');
  assert.equal(v('F-P-0414-relationship_assessment-Johannes').Johannes_is_husbands_nephew,true);
  assert.equal(v('F-P-0414-relationship_assessment-Johannes').legacy_correction_svager_incorrect,true);
  assert.equal(v('F-P-0414-source_assessment-personal-limits').four_independent_exact_birth_sources,false); groups++;

  // C0531/1019 correct a row shift: Stephan is Jones's father; Pehr belongs to Marta.
  assert.equal(r('M-P-0415-C0531-child').name_literal,'Jones');
  assert.equal(d('E-baptism-P-0415').value,'1816-10-13');
  assert.equal(v('O-P-0415-C0531-next-Marta').child,'Marta');
  assert.equal(v('O-P-0415-C0531-next-Marta').father,'Pehr Simonsson');
  assert.equal(v('F-P-0415-parentage_assessment-corrected-row').raw30_35_not_two_individual_ages,true);
  assert.equal(parents('P-0415').length,0);
  assert.equal(participants('E-baptism-P-0415').filter(x=>x.role==='witness').length,6); groups++;

  // C1030's title proves prior service, not name origin, regiment, completed age 26 or registered assets.
  const career=v('F-P-0415-occupation-military-and-work');
  assert.equal(career['1842'],'f.d. Lifgardisten'); assert.equal(career.Nordlund_military_name_origin_unproven,true);
  assert.equal(career.age_M26_not_completed_age25,true); assert.equal(career.agreement_registration_contents_survival_unproven,true);
  assert.equal(r('E-migration-P-0415').event_type,'registered_arrival'); assert.equal(d('E-migration-P-0415').value,'1858');
  assert.deepEqual(v('F-P-0415-source_assessment-preservation-limits').C1042_existing_images,[82,83]); groups++;

  // The December 1844 child remains distinct from P0251 despite accepted parent participants.
  assert.equal(r('ID-P-0251-C1042-candidate').decision,'candidate');
  const december=participants('E-baptism-C1042-candidate');
  assert.ok(december.some(x=>x.person_id==='P-0415'&&x.role==='father'));
  assert.ok(december.some(x=>x.person_id==='P-0416'&&x.role==='mother'));
  assert.ok(december.every(x=>x.person_id!=='P-0251'));
  assert.equal(december.filter(x=>x.role==='witness').length,6);
  assert.equal(v('F-P-0415-family_context-four-recorded-children').Jonas1850.later,'29/3');
  assert.equal(v('F-P-0415-family_context-four-recorded-children').Ingrid1853.later,'1/8'); groups++;

  // C0532's later independent reading corrects baptism to 2 February but cannot resolve raw birth 2?.
  assert.equal(d('E-baptism-P-0416').value,'1812-02-02'); assert.equal(d('E-birth-P-0416').value,'1812-01-23');
  assert.equal(v('O-P-0416-C0532-child').birth_day_literal,'2[?]');
  assert.equal(v('O-P-0416-C0857-child').birth_literal,'23/1 1812');
  assert.equal(v('O-P-0416-C0530-own').birthplace_cell,'blank');
  assert.equal(v('O-P-0416-C0530-own').from_cell,'blank');
  assert.equal(v('F-P-0416-residence-personal-household-boundaries').from1858_written_on_husband,true);
  assert.equal(participants('E-baptism-P-0416').filter(x=>x.role==='witness').length,4);
  assert.equal(r('M-P-0416-C0532-witness-Inertha').name_literal,'Inertha[?] Olsdotter');
  assert.deepEqual(v('F-P-0416-family_context-earlier-siblings').siblings.map(x=>x.raw_name),['Brita Olofsd[otter]','Jöns Olsson']); groups++;

  // C0857's preceding Stephan and younger Stefan remain source rows, not accepted ancestors or brothers.
  assert.equal(d('E-birth-P-0417').value,'1772-04-09'); assert.equal(r('E-birth-P-0417').place_id,null);
  assert.equal(v('O-P-0417-C0857-own').birthplace_blank,true);
  assert.equal(r('M-P-0417-C0857-own').name_literal,'Olof Stephansson');
  assert.equal(v('O-P-0417-C0857-predecessor').birth_literal,'25/8 1737');
  assert.equal(r('F-P-0417-family_hypothesis-father-and-brother').disposition,'candidate');
  assert.equal(parents('P-0417').length,0);
  assert.equal(v('F-P-0417-life_scope-personal-limits').first_dated_household_year,1805);
  assert.equal(v('F-P-0417-network_assessment-patronymic-limit').no_same_patronymic_does_not_exclude_kinship,true); groups++;

  // Shared 1806 marriage and Cajsa Brita baptism carry only their extracted date precision.
  assert.equal(d('E-marriage-P-0417-P-0418-1806').precision,'year');
  assert.equal(d('E-marriage-P-0417-P-0418-1806').value,'1806');
  for(const id of ['P-0417','P-0418']) assert.ok(participants('E-marriage-P-0417-P-0418-1806').some(x=>x.person_id===id&&x.role==='spouse'));
  const cajsa=participants('E-baptism-C0532-Cajsa-Brita');
  assert.equal(d('E-baptism-C0532-Cajsa-Brita').precision,'year');
  for(const id of ['P-0417','P-0418']) assert.ok(cajsa.some(x=>x.person_id===id&&x.role==='witness'&&x.mention_id));
  assert.ok(cajsa.some(x=>x.person_id===null&&x.role==='child'));
  assert.equal(r('M-P-0417-C0532-witness').name_literal,'Olof Stefansson'); groups++;
  return {ok:true,groups};
}
