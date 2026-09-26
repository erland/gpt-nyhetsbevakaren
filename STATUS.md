# STATUS

## Produktstatus

Nyhetsbevakaren **1.0.0** är stabilt releasad efter att `1.0.0-rc.2` praktiskt provkörts utan rapporterade blockerande fel. Funktionaliteten i 1.0.0 är fortsatt referens för den beteendebevarande migreringen.

## GPT Byggaren 1.5.0-migrering

Migreringen är nu i slutlig release-readiness.

- fem aktiva runtimes: Chat ZIP, Custom GPT, Claude Projects, OpenCode och OpenAI Plugin,
- canonical instruktion: `src/instructions/system.md`,
- webbresearch/source navigation: required för aktuell nyhetsbevakning,
- persistent workspace-state: inte required,
- direkt schemaläggning: optional capability,
- nyhetsprofil och schemaläggningsprompt: portabla artefakter,
- OpenAI Plugin: Agent Plugins 1.0, skills-first, utan antagen MCP/Tasks,
- deklarativ build och release från `gpt-project.yaml`,
- exakt release-assetuppsättning valideras före publicering.

## Kvalitetsgrindar

CI verifierar:

- projektlint,
- GPT Builder 1.5 platform contracts,
- project hygiene,
- news robustness/hygiene,
- build av fem runtimes,
- distributionsvalidering,
- runtime parity,
- release asset set,
- eval suite.

Kritiska kvalitetsområden omfattar freshness, source quality, event deduplication, uncertainty, political neutrality och scheduling portability.

## Stabil releasehistorik

- Produktversion: `1.0.0`
- Föregående RC: `1.0.0-rc.2`
- Praktisk provkörning: godkänd 2026-09-12
- Instruction-adherence-evals: 33
- E2E-scenarier: 8

## Nästa åtgärd

När slutlig release-readiness och PR-CI är grön kan migrations-PR:n mergas. Därefter kan nästa stabila release skapas med semantisk release-tagg; taggen styr versionsnumret i runtime-distributionerna.

Maskinläsbar migrationsstatus finns i `migration-status.yaml`.
