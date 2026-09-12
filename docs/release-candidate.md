# Release candidate – 1.0.0-rc.2

Nyhetsbevakaren RC.2 var sista release candidate före stabil 1.0.0.

## Ändring från rc.1

- Fas 3 skapar alltid schemaprompten som nedladdningsbar Markdown när filskapande finns.
- Filen innehåller metadata och den kompletta självförsörjande körprompten.
- Chat-läge får erbjuda direkt Scheduled Task när värdmiljön stöder funktionen.
- Schemat skapas först efter uttryckligt användargodkännande och använder exakt samma prompt som filen.
- Custom GPT och andra miljöer utan Tasks använder samma fil som manuell fallback.

## Utfall

RC.2 praktiskt provkördes 2026-09-12 utan rapporterade blockerande fel och godkändes därefter för stabil `1.0.0`.
