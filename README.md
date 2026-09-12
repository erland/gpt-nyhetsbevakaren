# Nyhetsbevakaren

GPT-projekt för att konfigurera, köra och automatisera ämnesbaserad nyhetsbevakning.

Projektet bygger både Chat ZIP och Custom GPT från samma canonical instruktion.

## Utveckling

- Utvecklingsplan: `docs/development-plan.md`
- Canonical instruktion: `src/instructions/system.md`
- Projektstatus: `project-status.yaml`
- Runtime-paritet: `docs/runtime-parity.md`

## GitHub Actions

CI lintar och bygger distributioner vid push/PR. En publicerad GitHub Release använder release-taggen som versionskälla och laddar upp byggda artefakter.

## Stabil release

Aktuell stabil version är `1.0.0`. Release candidate `1.0.0-rc.2` praktiskt provkördes utan rapporterade blockerande fel före stabilisering. Se `docs/release-1.0.0.md` för releaseinformation och `docs/release-candidate.md` för RC-historiken.
