import {readCurrent,researchOutcome} from './domain.mjs';

// Query vocabulary, not a rewriting rule for participation or mention data.
// Each term except the one context-bound alias retains its own meaning.
export const PARTICIPATION_ROLE_VOCABULARY=Object.freeze({
  arriving:'Inflyttande deltagare',
  arriving_person:'Inflyttande person, äldre uttrycklig rollkod',
  baptism_witness:'Äldre dopvittneskod; frågealias till witness endast vid baptism',
  baptized:'Döpt person',
  bereaved_spouse:'Efterlevande make eller maka',
  bride:'Brud',
  brides_guardian:'Brudens uttryckligt angivna företrädare',
  buried:'Begravd person',
  child:'Barnroll i den angivna händelsen',
  consenting_mother:'Samtyckande mor',
  deceased:'Avliden person',
  departing:'Utflyttande deltagare',
  departing_person:'Utflyttande person, äldre uttrycklig rollkod',
  emergency_baptizer:'Nöddopförrättare',
  estate_declarant:'Bouppgivare',
  family_member:'Familjemedlem i händelsen',
  father:'Fadersroll i händelsen; personrelation bedöms separat',
  giftoman:'Uttrycklig giftomannaroll',
  groom:'Brudgum',
  heir:'Arvinge',
  household_child:'Barn i hushållet',
  household_member:'Hushållsmedlem',
  migrant:'Flyttande deltagare',
  minors_representative:'Företrädare för omyndiga',
  mother:'Modersroll i händelsen; personrelation bedöms separat',
  officiant:'Förrättare',
  parent:'Föräldraroll i händelsen; personrelation bedöms separat',
  party:'Part i händelsen',
  principal:'Händelsens huvudperson',
  resident:'Boende',
  spouse:'Make eller maka i händelsen',
  subject:'Händelsens subjekt, äldre uttrycklig rollkod',
  wife:'Hustruns roll i händelsen',
  witness:'Vittne i händelsen; ingen föräldra- eller släktrelation följer',
});

/** @typedef {keyof typeof PARTICIPATION_ROLE_VOCABULARY} KnownParticipationRole */
/** @typedef {{role?:string|null,eventType?:string|null,personId?:string|null}} ParticipationFilter */

/** @returns {string|null} Known codes and unknown literal words remain distinguishable. */
export function canonicalParticipationRole(raw,eventType) {
  if(raw==null)return null;
  if(typeof raw!=='string')throw new TypeError('Deltagarroll måste vara text eller null');
  return raw==='baptism_witness'&&eventType==='baptism'?'witness':raw;
}

function filterValue(value,key) {
  if(value==null)return null;
  if(typeof value!=='string')throw new TypeError(`${key} måste vara text eller null`);
  return value.trim()||null;
}

/**
 * Read current participations with their full, separate event/mention records.
 * No disposition is filtered implicitly. personId matches only participation.person_id.
 * Empty filters mean no restriction; unknown roles remain exact searchable values.
 * @param {import('node:sqlite').DatabaseSync} db
 * @param {ParticipationFilter|null} filters
 */
export function findParticipations(db,filters={}) {
  if(filters==null)filters={};
  if(typeof filters!=='object'||Array.isArray(filters))throw new TypeError('Deltagarfilter måste vara ett objekt');
  const role=filterValue(filters.role,'role'),eventType=filterValue(filters.eventType,'eventType'),personId=filterValue(filters.personId,'personId');
  const conditions=[],args=[];
  if(eventType){conditions.push('e.event_type=?');args.push(eventType);}
  if(personId){conditions.push('p.person_id=?');args.push(personId);}
  const rows=db.prepare(`SELECT r.object_id,p.role,e.event_type FROM current_revision r
    JOIN participation p ON p.revision_id=r.id JOIN current_revision er ON er.object_id=p.event_id
    JOIN event e ON e.revision_id=er.id ${conditions.length?'WHERE '+conditions.join(' AND '):''}
    ORDER BY r.object_id`).all(...args);
  const events=new Map(),mentions=new Map();
  const cached=(cache,id)=>{if(id==null)return null;if(!cache.has(id))cache.set(id,readCurrent(db,id));return cache.get(id);};
  return rows.filter(row=>role===null||canonicalParticipationRole(row.role,row.event_type)===canonicalParticipationRole(role,row.event_type)).map(row=>{
    const participation=readCurrent(db,row.object_id);
    return {...participation,storedRole:participation.role,canonicalRole:canonicalParticipationRole(participation.role,row.event_type),
      knownRole:Object.hasOwn(PARTICIPATION_ROLE_VOCABULARY,participation.role)&&(participation.role!=='baptism_witness'||row.event_type==='baptism'),
      event:cached(events,participation.event_id),mention:cached(mentions,participation.mention_id)};
  });
}

// Reuse the domain's exact mapping. In particular, this does not silently add
// STÖDD, OLÖST INOM PRÖVAT OMFÅNG, OPEN, open or negative as recognized aliases.
export const canonicalQuestionOutcome=researchOutcome;
export const QUESTION_OUTCOME_VOCABULARY=Object.freeze({
  open:'Öppen',in_progress:'Pågår',established:'Fastställd',rejected:'Avvisad',
  unresolved:'Olöst',disputed:'Omstridd',supported:'Styrkt',not_supported:'Ej styrkt',
  passed:'Godkänd',failed:'Underkänd',reviewed:'Genomgånget',bounded:'Avgränsat',privacy_bounded:'Integritetsminimerat',
});

/** Preserve the full question, raw outcome and disposition; retirement is separate. */
export function questionOutcomeView(question) {
  const canonicalOutcome=researchOutcome(question.outcome);
  return {...question,storedOutcome:question.outcome??null,canonicalOutcome,
    knownOutcome:canonicalOutcome!==null,active:question.disposition!=='retired'};
}
