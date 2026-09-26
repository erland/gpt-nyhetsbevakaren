# Migreringsplan – GPT Byggaren 1.5.0

Projekt: **Nyhetsbevakaren**  
Utgångsläge: stabil produktversion **1.0.0** med Chat ZIP och Custom GPT.

Målet är att migrera projektets struktur och distributionsmodell till GPT Byggaren 1.5.0 utan att förändra Nyhetsbevakarens etablerade kärnbeteende eller ersätta den befintliga produktens utvecklingshistorik.

## Principer

- `src/instructions/system.md` förblir canonical beteendekälla.
- Befintliga evals, E2E-scenarier och Knowledge-filer behålls som kvalitetsgrund.
- Webbsökning är fortsatt en kärncapability för faktisk nyhetsbevakning.
- Nyhetsprofil, aktualitetskontroll, källvärdering, händelsebaserad deduplicering och schemaläggningsprompt får inte försvagas.
- Persistent workspace-state ska inte införas som krav; fristående profil/prompt ska bära återanvändbar konfiguration.
- Befintlig produktplan i `docs/development-plan.md` behålls. Denna fil beskriver en separat migrationsplan.
- Chat ZIP och Custom GPT ska fortsätta fungera genom hela migreringen.
- Nya runtimes aktiveras först när build, validation och parity är verifierade.

## Steg

### 1. Inför separat 1.5.0-migrationsstatus och normalisera projektkontrakt
Lägg till migrationsplan/status och deklarera migrationen i `gpt-project.yaml` utan att ändra befintliga runtime-distributioner.

### 2. Inför fulla plattformsneutrala kontrakt
Modellera capabilities, artifacts, state och tools. Webbresearch ska vara required för aktuell nyhetsbevakning.

### 3. Normalisera build-modellen
Gör runtime-val, artifact-namn och runtime-källor deklarativa från `gpt-project.yaml` samtidigt som befintliga Chat ZIP/Custom GPT behåller kompatibilitet.

### 4. Lägg till Claude Projects
Skapa Claude Projects-distribution från samma canonical instruktion, Knowledge och researchkontrakt.

### 5. Lägg till OpenCode
Skapa OpenCode-runtime med samma research-, källkritik- och rapportkontrakt.

### 6. Lägg till OpenAI Plugin
Skapa skills-first Agent Plugins 1.0-distribution utan att anta MCP eller andra integrationer som inte finns.

### 7. Runtime parity, hygiene och robustness
Utöka kontrollerna för aktualitet, source quality, event deduplication, osäkerhet, politik/val-neutralitet och fristående schemaläggningsprompt.

### 8. Generalisera CI och release
Bygg, validera och publicera exakt de aktiva runtime-assets som deklareras i `gpt-project.yaml`.

### 9. Slutlig release-readiness
Synkronisera dokumentation/status och verifiera att fem runtimes är beteendebevarande, testade och merge-/releaseklara.
