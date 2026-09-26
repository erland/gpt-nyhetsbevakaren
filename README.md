# Nyhetsbevakaren

GPT-projekt för att konfigurera, köra och automatisera ämnesbaserad nyhetsbevakning.

Projektet bygger fem aktiva runtime-distributioner från samma canonical beteende:

- Chat ZIP
- Custom GPT
- Claude Projects
- OpenCode
- OpenAI Plugin

## Canonical modell

- Canonical instruktion: `src/instructions/system.md`
- Knowledge: `knowledge/`
- Eval-manifest: `evals/test-manifest.yaml`
- Projektkontrakt: `gpt-project.yaml`
- Runtime-paritet: `docs/runtime-parity.md`

Nyhetsbevakning kräver aktuell webbresearch och källöppning. Persistent workspace-state krävs inte; återanvändbar konfiguration bärs av nyhetsprofilen och den självförsörjande schemaläggningsprompten.

## Utveckling

- Ursprunglig produktplan: `docs/development-plan.md`
- GPT Byggaren 1.5.0-migrering: `docs/migration-gpt-builder-1.5.0.md`
- Produktstatus: `project-status.yaml`
- Migrationsstatus: `migration-status.yaml`

## GitHub Actions

CI verifierar projektlint, platform contracts, project hygiene, news robustness, build av fem runtimes, distributionsvalidering, runtime parity, release-assetuppsättning och eval suite.

En publicerad GitHub Release använder release-taggen som versionskälla. Exakt de aktiva runtime-assets som deklareras i `gpt-project.yaml` publiceras tillsammans med `SHA256SUMS.txt` och `DELIVERY-MANIFEST.json`.

## Stabil produktversion

Aktuell stabil produktversion är `1.0.0`. Release candidate `1.0.0-rc.2` praktiskt provkördes utan rapporterade blockerande fel före stabilisering. Se `docs/release-1.0.0.md` och `docs/release-candidate.md` för releasehistorik.
