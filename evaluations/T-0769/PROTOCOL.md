# T-0769 – fryst protokoll

60 nya subagentkontexter: 3 uppgifter × 4 modeller × 5 upprepningar.
Modeller: gpt-6-astra, gpt-5.6-sol, gpt-5.6-terra, gpt-5.6-luna.
Alla medium reasoning, priority enligt verktygets miljö, fork_turns=none.
Slumpad startordning seed769, högst tre parallella försök.
Samma uppgiftspaket och wrapper per uppgift; endast RUN_DIR skiljer sig.
Inga adaptiva tips, ingen rättningsrunda. Max15min per försök, timeout räknas
som misslyckat försök med kvarvarande artefakt. Inget försök ersätts för låg kvalitet.

X:25 avgränsade bildfält i två verkliga källutsnitt. Y:16 syntetiserade
objekt och9requests kring verkliga projekttyper. Z: litet nativepaket på
isolerad databas. Begränsad mikrouppgiftsjämförelse, inte full forskning.

Försöken får bara läsa eget inputpaket; inga tidigare svar eller facit.
Gemensamt filsystem ger instruktionsbaserad isolering, inte OS-sandbox per
försök. Verktygsloggar kontrolleras för otillåten läsning. Sådant gör ett
försök kontaminerat och rapporteras separat; ingen tyst ersättning.

Råa svar fryses innan bedömning. Bedömningskopior får slump-ID utan
modellnamn. Automatiska kontroller används för struktur, beslut,
versionshantering och apply. Bildläsning och sakmotiveringar granskas
blint mot förberett underlag. Samma AI-familjs granskning är en begränsning;
modellen är inte ett mänskligt oberoende facit. Alternativa giltiga svar
får inte underkännas av strängmatchning.

Mät: godkänd andel, partiell kvalitet, kritiska fel, tid från agentstart
till avslut, verktygsanrop, input/cached/output/reasoning-token om exponerat.
Beredning/granskning redovisas separat från försök. Ingen påhittad faktisk
debitering; använd kostnadsformel och brytpunkter om verifierade priser
inte finns. Fem upprepningar på samma material mäter körstabilitet,
inte fem oberoende genealogiska fall eller generell säkerhet.

Officiell vägledning kontrollerad2026-09-19:
https://learn.chatgpt.com/docs/agent-configuration/subagents
Lokalt collaboration-verktyg avgör tillgängliga exakta modell-ID:n.
