# Projekt – Nyhetsbevakaren

## Syfte

Nyhetsbevakaren hjälper användaren skapa en källstrategi för ett eller flera ämnen, genomföra aktuell nyhetsbevakning och därefter skapa en självförsörjande prompt för återkommande körning.

## Huvudfaser

1. Bygg och kvalitetssäkra nyhetsprofil.
2. Kör nyhetsbevakning för ett tidsintervall.
3. Erbjud och generera återkommande bevakning.

## Canonical beteende

`src/instructions/system.md` är canonical instruktion. Kritiska regler för aktualitet, källkvalitet, händelsebaserad deduplicering, osäkerhet, politik/val-neutralitet och schemaläggning ska finnas där och får inte enbart ligga i Knowledge.

## State-modell

Projektet är research-heavy men inte stateful:

- aktuell webbresearch och source navigation krävs för faktisk nyhetsbevakning,
- persistent workspace-state krävs inte,
- chatthistorik är inte auktoritativ state,
- nyhetsprofilen är portabel konfiguration,
- schemaläggningsprompten ska vara självförsörjande.

## Distributioner

Fem aktiva runtimes byggs från samma canonical beteende:

- Chat ZIP
- Custom GPT
- Claude Projects
- OpenCode
- OpenAI Plugin

OpenAI Plugin använder Agent Plugins 1.0 och skills-first-struktur utan påhittad MCP- eller Tasks-integration.

## Kvalitet och release

CI verifierar platform contracts, hygiene, news robustness, distributioner, runtime parity, release-assets och eval suite. GitHub Release publicerar exakt de aktiva runtime-assets som deklareras i `gpt-project.yaml`.

Den ursprungliga produktutvecklingen finns kvar i `docs/development-plan.md`; GPT Byggaren 1.5.0-migreringen följs separat i `docs/migration-gpt-builder-1.5.0.md` och `migration-status.yaml`.
