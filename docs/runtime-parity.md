# Runtime-paritet – Nyhetsbevakaren

## Mål

Chat ZIP, Custom GPT och Claude Projects ska ge samma kärnbeteende för Nyhetsbevakaren. Skillnader får endast bero på respektive körmiljös sätt att bära instruktioner, Knowledge och verktyg.

## Gemensamt kärnbeteende

Samtliga aktiva användarruntimes ska:

- följa flödet **bygg och kvalitetssäkra nyhetsprofil → kör nyhetsbevakning → erbjud återkommande bevakning**,
- använda aktuell webbsökning när värdmiljön erbjuder webbåtkomst,
- behandla källprofilen som en prioriterad strategi och inte som en absolut whitelist,
- skilja publiceringsdatum, uppdateringsdatum och händelsedatum när det är relevant,
- använda **Händelsebaserad deduplicering**,
- rangordna efter betydelse och relevans i stället för publiceringsvolym,
- ge 3–5 meningars sammanfattning per kvalificerad händelse med klickbara källor när plattformen stöder det,
- hellre rapportera färre kvalificerade händelser än fylla ut,
- kunna skapa en **självförsörjande schemaläggningsprompt som nedladdningsbar Markdown-fil** utan beroende av tidigare chattminne.

## Plattformsskillnader

| Område | Chat ZIP | Custom GPT | Claude Projects | Paritetsbedömning |
|---|---|---|---|---|
| Canonical instruktion | Levereras som `assistant/instructions.md` | Kompileras till `builder/instructions.md` | Levereras byte-identiskt som `assistant/instructions.md` | Likvärdig kärnlogik |
| Knowledge | Samtliga runtime-relevanta Knowledge-filer medföljer ZIP | Valda Knowledge-filer laddas upp i Builder | Samtliga canonical Knowledge-filer medföljer | Likvärdig med nuvarande korpus |
| Webbsökning | Kräver webbåtkomst i körmiljön | Web browsing måste vara aktiverat | Kräver aktuell webbresearch/källöppning i Claude-miljön | Samma krav, olika aktivering |
| Scheman/script/mallar | Kan medfölja som filer i ZIP och användas som stöd | Ingår inte som körbar runtime-logik | Ingår inte som krav för kärnflödet | Reducerad artefakttillgång påverkar inte kärnbeteende |
| Samtalsstartare | Medföljer i ZIP-kontexten | Sätts explicit som Builder conversation starters | Medföljer som runtime-underlag | Likvärdigt |
| Återkommande körning | Genererar alltid Markdown-fil och kan, när Tasks finns, erbjuda direkt schemaläggning efter godkännande | Genererar samma Markdown-fil; direkt Tasks kan saknas | Genererar samma självförsörjande Markdown-prompt; direkt schemaläggning är optional | Samma promptartefakt, capability-beroende action |
| Persistens mellan körningar | Får inte förutsättas | Får inte förutsättas | Får inte förutsättas | Likvärdigt |

## Reducerade funktioner i Custom GPT

Custom GPT-distributionen innehåller inte projektets utvecklings- och valideringsscript som en del av GPT:ns kärnbeteende. Dessa används vid bygge och kvalitetssäkring, inte för nyhetsanalysen. Detta ska därför inte påverka användarens nyhetsresultat.

Om Knowledge-paketet i framtiden överstiger plattformens filgräns måste byggsteget prioritera eller konsolidera material utan att flytta kritiska arbetsflödesregler från canonical instruktionen.

## Schemaläggning

Alla tre aktiva användarruntimes genererar samma självförsörjande schemaläggningsprompt som en nedladdningsbar Markdown-fil när filskapande stöds. Filen är den portabla canonical leveransen.

När Chat-värdmiljön erbjuder Scheduled Tasks får Chat-versionen dessutom erbjuda att skapa schemat direkt efter användarens uttryckliga godkännande och då använda exakt samma prompt. Custom GPT eller annan miljö utan denna capability lämnar filen för manuell användning. Direkt schemaläggning är därför en runtime-förbättring, inte en dold förutsättning för kärnbeteendet.

## Krav på värdmiljön

För full funktion krävs:

1. aktuell webbsökning/browsing,
2. möjlighet att öppna källor och lämna klickbara länkar,
3. tillgång till bifogad Knowledge där den används för detaljregler.

Om webbsökning saknas ska GPT:n säga att den inte kan verifiera aktuella nyheter i stället för att presentera minnesbaserad information som aktuell.

## Paritetsgräns

Paritet betyder samma beslutsregler och rapportkontrakt, inte byte-för-byte-identiska svar. Sökresultat, ranking och formulering kan variera mellan körningar eftersom nyhetsläget och sökresultaten förändras.
