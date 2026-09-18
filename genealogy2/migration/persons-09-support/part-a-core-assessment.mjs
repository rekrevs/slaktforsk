import {cs} from './genealogy2-persons09-combined.mjs';

// Individuella identitetsbedömningar; flera läsningar av samma post är en källa.
const assessments = {
  'P-0401': ['CORROBORATED', ['C-0491','C-0492'], 'Anna Adelia återfinns med samma familj och födelseår i census 1910 och senare hushållsbok. Kedjan stödjer den avgränsade personidentiteten, inte oberoende födelsedatum eller kontraktsgodkännande.'],
  'P-0402': ['CORROBORATED', ['C-0506'], 'Brita Greta binds genom födelsenotisen 1821 och den separata hushållsposten med samma föräldrar. C0506 innehåller två skilda poster; flera läsningar av dem är inte extra belägg.'],
  'P-0403': ['CORROBORATED', ['C-0509','C-0510'], 'Nils Pehrsson binds som Lars Olssons far i födelsenotisen 1836 och den senare familjeposten. Detta stödjer vuxenidentiteten utan att styrka hans rapporterade födelse eller den första vigseln.'],
  'P-0404': ['TRANSCRIBED', ['C-0509'], 'Lisa Stina Larsdotters avgränsade existens som namngiven mor stöds av barnets födelsepost 1836. Flera läsningar av samma post är inte korroborering; egen födelse och civilstånd är oprövade.'],
  'P-0405': ['TRANSCRIBED', ['C-0510'], 'Lisa Stina Jonsdotter är en egen namngiven hustru i en hushållspost. Om- och andraläsningar av denna post ger inte en oberoende identitetskedja; hon hålls skild från Larsdotter.'],
  'P-0406': ['TRANSCRIBED', ['C-0510'], 'Lisa Cajsa är ett avgränsat namngivet barn i en hushållspost. Egen födelsenotis och senare egen närvaro har inte lästs; familjens andra poster gör inte hennes identitet korroborerad.'],
  'P-0407': ['CORROBORATED', ['C-0388','C-0389','C-0512'], 'Nils Petter har sammanhängande namn, födelseår, föräldrar och syskon i hushållspost och census 1880/1890. Serien stödjer familjeidentiteten men är beroende för födelseuppgiften.'],
  'P-0408': ['CORROBORATED', ['C-0388','C-0389','C-0390','C-0512'], 'Lars Olof har sammanhängande namn, födelseår och familj i hushållspost och census 1880/1890/1900. Identiteten är jämförd mellan poster; kyrkoboksberoendet gör inte födelsedatumet oberoende belagt.'],
  'P-0409': ['CORROBORATED', ['C-0388','C-0389','C-0512'], 'Katarina Petronella binds genom namnets uttryckliga varianter, födelseår och samma familj i hushållspost och census 1880/1890. Strykningen ger ingen egen döds- eller flyttuppgift.'],
  'P-0410': ['CORROBORATED', ['C-0389','C-0390','C-0512'], 'Erik Emanuel binds genom namn, födelseår och samma familj i hushållspost och census 1890/1900. Han är inte belagd i den bevarade censusavskriften 1880.'],
  'P-0411': ['CORROBORATED', ['C-0521','C-0600','C-0645','C-0323','C-0322'], 'Johan August binds i den granskade kedjan av namn, datum och familj mellan födelse, vigsel och senare hushåll. Faderskonflikt och brödernas okända hel-/halvrelation begränsar härledningen utan att upplösa hans egen identitet.'],
  'P-0413': ['CORROBORATED', ['C-0521','C-0672','C-0688'], 'Anna Britas avgränsade kvinnliga identitet stöds av namn, datum och barnet i jämförda födelse-, vigsel- och hushållsposter. Konflikten mellan uppgiven barnafader och vigsel samt tvåkvinnorshypotesen kvarstår uttryckligt.'],
  'P-0414': ['CORROBORATED', ['C-0600','C-0645','C-0323','C-0322'], 'Anna Lovisas vuxenidentitet binds genom egen vigsel och efterföljande poster med samma make och barn. Ursprungsidentiteten och det exakta födelsedatumet får inte fler röster genom denna kedja.'],
  'P-0415': ['CORROBORATED', ['C-0531','C-1030','C-0530','C-1042'], 'Jonas binds genom jämförd egen födelseuppgift, vigsel och familjeposter. Namnbytet och den olösta läsningen av faderns patronymikon görs inte till styrkta uppåtgående länkar.'],
  'P-0416': ['CORROBORATED', ['C-0532','C-0857','C-1030','C-0530','C-1042'], 'Gertrud binds genom barndoms- och vuxenhushåll, vigsel och barns födelsepost. Två hushåll anger 23 januari, medan födelsepostens rådag förblir osäker och andraläsningen inte är en extra originalkälla.'],
  'P-0417': ['CORROBORATED', ['C-0857','C-0532'], 'Olof binds mellan egen hushållsrad med hustru och dotter samt separata fader- och vittnesposter 1812. Den prövade vuxenidentiteten innebär ingen accepterad länk till de äldre männen i hushållet.'],
};

export function assessPartACore(p) {
  const assessment=assessments[p.person];
  if (!assessment) throw Error(`Ingen individuell kärnbedömning för ${p.person}`);
  const core=p.changes.find(x=>x.id===p.person&&x.kind==='person');
  if (!core) throw Error(`Ingen personkärna för ${p.person}`);
  const [status,citations,rationale]=assessment;
  core.evidenceStatus=status;
  core.rationale=rationale;
  for (const citation of citations) {
    const origin=cs(citation);
    if (!core.origins.some(o=>JSON.stringify(o)===JSON.stringify(origin))) core.origins.push(origin);
  }
}
