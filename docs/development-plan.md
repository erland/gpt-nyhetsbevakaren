# Utvecklingsplan – Nyhetsbevakaren

## Projektmål

Bygg en GPT som kan konfigurera och köra aktuell nyhetsbevakning för ett eller flera ämnen och därefter skapa en fristående prompt för återkommande/schemalagd bevakning.

GPT:n ska arbeta i tre huvudfaser:

1. **Bygg och kvalitetssäkra nyhetsprofil** – analysera ämnen, hitta och bedöma relevanta källor samt skapa en källstrategi.
2. **Kör nyhetsbevakning** – söka inom angivet tidsintervall, prioritera de viktigaste händelserna, slå ihop dubbletter och presentera korta sammanfattningar med klickbara källor.
3. **Automatisera** – efter en lyckad körning erbjuda återkommande bevakning och skapa en självförsörjande schemaläggningsprompt anpassad till önskad frekvens.

## Rekommenderad projektprofil

**Profil:** `workflow_research_heavy`

Motivering: kärnuppgiften bygger på flerpass-research, källvärdering, aktualitetskontroll, händelsebaserad deduplicering och kvalitativ prioritering. Samma canonical beteende ska byggas för både Chat ZIP och Custom GPT.

## Arkitekturprinciper

- Webbsökning är en kärncapability.
- Kritiska arbetsflödesregler ligger i canonical instruktion, inte enbart i Knowledge.
- Källor i en nyhetsprofil är prioriterade, inte normalt en absolut whitelist.
- Primärkällor och etablerade redaktionella källor ska prioriteras framför aggregatorer och omskrivningar.
- Händelser dedupliceras semantiskt: flera artiklar om samma händelse blir normalt en nyhet med flera källor.
- Publiceringsdatum och händelsedatum ska skiljas åt när det är relevant.
- GPT:n får hellre rapportera färre relevanta nyheter än fylla ut rapporten med lågprioriterat material.
- Schemaläggningsprompten ska vara självförsörjande och inte förutsätta minne från konversationen.
- En återkommande prompt ska innehålla ämnen, avgränsningar, källstrategi, tidsfönster, prioriteringsregler, dedupliceringsregler och presentationsformat.

## Utvecklingssteg

### Steg 1 – Skapa projektgrund och canonical kontrakt

**Mål:** Skapa projektstruktur och formulera GPT:ns identitet, mål, tre huvudfaser, capabilities och övergripande arbetsregler.

**Leveranser:**
- `gpt-project.yaml`
- `project-status.yaml`
- `PROJECT.md`
- `STATUS.md`
- `README.md`
- `canonical/instructions.md`
- denna plan som `docs/development-plan.md`
- grundläggande CI/release-struktur

**Klart när:**
- projektet kan byggas som komplett projekt-ZIP,
- canonical instruktion beskriver hela kärnflödet utan obligatoriskt Knowledge-hopp,
- lint/hygiene för grundstrukturen passerar.

### Steg 2 – Implementera fas 1A: ämnesanalys och bevakningsbehov

**Mål:** Göra GPT:n bra på att omsätta ett eller flera ämnen till en tydlig bevakningsdefinition.

**Leveranser:**
- regler för ämnesanalys,
- regler för geografisk, språklig och innehållsmässig avgränsning,
- inkluderings- och exkluderingskriterier,
- rekommendation av tidskänslighet och typ av källor.

**Tester/evals:**
- bred AI-bevakning,
- smal AI-agentbevakning,
- svenskt val,
- kombination av flera ämnen.

**Klart när:** GPT:n kan skapa en tydlig preliminär bevakningsprofil utan onödiga följdfrågor.

### Steg 3 – Implementera fas 1B: källkartläggning och källstrategi

**Mål:** Hitta, värdera och prioritera källor som passar bevakningen.

**Leveranser:**
- flerpassflöde för källresearch,
- kategorier för primärkällor, myndigheter/organisationer, etablerade medier, specialistmedier och relevanta analys-/forskningskällor,
- källbedömningskriterier,
- regler för balans och källtäckning,
- regler för när sökning utanför kärnkällorna ska göras.

**Klart när:** GPT:n kan producera en kvalitetssäkrad källstrategi i stället för bara en osorterad URL-lista.

### Steg 4 – Definiera och serialisera nyhetsprofilen

**Mål:** Göra resultatet från fas 1 återanvändbart och stabilt.

**Leveranser:**
- schema/struktur för nyhetsprofil,
- läsbart presentationsformat,
- regler för ändring och omprövning av profilen,
- stöd för att använda profilen direkt i fas 2 och bädda in den i fas 3.

**Klart när:** en profil entydigt beskriver ämnen, avgränsningar, källstrategi och kvalitetskriterier.

### Steg 5 – Implementera fas 2A: aktuell nyhetssökning och tidsfönster

**Mål:** Söka efter kandidathändelser inom ett angivet intervall med korrekt aktualitetskontroll.

**Leveranser:**
- stöd för explicita datumintervall och relativa intervall,
- kontroll av publiceringsdatum kontra händelsedatum,
- kompletterande sökningar när kärnkällorna inte ger tillräcklig täckning,
- regler för att undvika äldre bakgrundsartiklar som felaktigt ser aktuella ut.

**Klart när:** kandidatuppsättningen är aktuell, relevant och spårbar till källor.

### Steg 6 – Implementera fas 2B: betydelsebedömning och händelsebaserad deduplicering

**Mål:** Välja de viktigaste nyheterna och slå ihop rapportering om samma underliggande händelse.

**Leveranser:**
- viktighetskriterier,
- relevansbedömning mot profilen,
- semantisk händelsegruppering,
- regler för när liknande artiklar ändå ska vara separata händelser,
- prioritering av original-/primärkällor i källistan.

**Klart när:** flera källor om samma händelse normalt ger en post med flera länkar och ingen konstgjord utfyllnad görs.

### Steg 7 – Implementera fas 2C: nyhetsrapport och presentation

**Mål:** Presentera resultatet konsekvent och lättläst.

**Leveranser:**
- rubrik per händelse,
- 3–5 meningars sammanfattning,
- klickbara länkar till en eller flera källor,
- tydlig period och ämnesprofil,
- möjlighet att ange att färre nyheter än önskat klarade kvalitetströskeln.

**Klart när:** rapporten fungerar för både dagliga och veckovisa sammanställningar och källorna går att följa vidare.

### Steg 8 – Implementera fas 3: återkommande bevakning och schemaläggningsprompt

**Mål:** Efter fas 2 erbjuda återkommande körning och generera en robust självförsörjande prompt.

**Leveranser:**
- fråga om användaren vill köra bevakningen återkommande,
- stöd för frekvens som dagligen, vardagar, veckovis eller användarens egen kadens,
- härledning av lämpligt tidsfönster från frekvensen,
- komplett prompt som bäddar in nyhetsprofil, källstrategi, prioriteringsregler, deduplicering och rapportformat,
- skydd mot att prompten blir beroende av tidigare konversationsminne.

**Klart när:** den genererade prompten kan köras fristående och ge i huvudsak samma typ av rapport som fas 2.

### Steg 9 – Robusthet, källkritik och edge cases

**Mål:** Förstärka beteendet för svåra och känsliga bevakningar.

**Leveranser:**
- regler för motstridiga uppgifter,
- hantering av paywalls och otillgängliga källor,
- hantering av breaking news och osäkra tidiga uppgifter,
- särskild försiktighet vid politiska ämnen och val,
- hantering av källor som blivit inaktuella eller bytt struktur,
- regressionsfall för vanliga fel.

**Klart när:** GPT:n tydligt skiljer fakta, osäkerhet och analys samt inte överdriver säkerhet eller betydelse.

### Steg 10 – Evals och end-to-end-validering

**Mål:** Mäta om GPT:n faktiskt följer arbetsflödet och producerar användbara rapporter.

**Scenarier:**
- dagliga AI-nyheter,
- veckovis AI-nyheter med smal avgränsning,
- svenska valet under en vecka,
- flera ämnen samtidigt,
- samma händelse publicerad av många källor,
- intervall utan tillräckligt många viktiga nyheter,
- generering av schemaläggningsprompt efter lyckad fas 2.

**Klart när:** kritiska evals passerar och kända kvalitetsbrister är dokumenterade eller åtgärdade.

### Steg 11 – Bygg Chat ZIP och Custom GPT-distribution

**Mål:** Kompilera samma canonical kontrakt till båda målplattformarna.

**Leveranser:**
- Chat ZIP,
- Custom GPT-instruktioner och Knowledge vid behov,
- dokumenterade plattformsskillnader,
- runtime-parity-rapport.

**Klart när:** båda distributionerna valideras och kritiskt beteende är likvärdigt där plattformarna tillåter det.

### Steg 12 – Release candidate och slutlig hygiene

**Mål:** Göra projektet releaseklart.

**Leveranser:**
- slutlig lint,
- project hygiene,
- distribution validation,
- checksummor,
- release-readiness-bedömning,
- RC-artefakter.

**Klart när:** inga blockerande valideringsfel återstår och komplett projekt-ZIP samt distributionsartefakter kan levereras.

### Steg 13 – Portabel schemaprompt och direkt Tasks-integration

**Mål:** Göra fas 3 enklare att använda i både Chat och Custom GPT.

**Leveranser:**
- alltid skapa schemaprompten som nedladdningsbar Markdown-fil,
- samma självförsörjande prompt i båda distributionerna,
- i Chat-läge erbjuda direkt Scheduled Task när värdmiljön stöder det,
- kräva uttryckligt godkännande före skapande av schemat,
- fallback till fil för miljöer utan direkt schemaläggning.

**Klart när:** filartefakten är obligatorisk i fas 3, Chat kan använda samma prompt för direkt schemaläggning när capability finns och runtime-pariteten dokumenterar skillnaden.

### Steg 14 – Stabil release

**Mål:** Praktiskt provköra RC:n och publicera `1.0.0` om inga blockerande fel återstår.

## Första rekommenderade genomförandesteg

**Steg 1 – Skapa projektgrund och canonical kontrakt.**

Det steget skapar den första kompletta projekt-ZIP:en och lägger grunden för att därefter kunna fortsätta med kommandot **”Gör nästa steg”**.
