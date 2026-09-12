# End-to-end-validering – steg 10

## Omfattning

Testsviten täcker hela Nyhetsbevakarens kontrakt från profilskapande till rapport och schemaläggningsprompt. E2E-scenarierna är scenario-/kontraktsbaserade och valideras deterministiskt i projektet; faktisk modellkvalitet ska dessutom bedömas vid runtime-testning av Chat ZIP och Custom GPT.

## Scenarier

1. Daglig bred AI-bevakning.
2. Veckovis smal bevakning av agentisk AI.
3. Svenska riksdagsvalet under en vecka.
4. Flera ämnen i samma profil.
5. Många källor om samma underliggande händelse.
6. Tunt tidsfönster med färre kvalificerade nyheter än önskat.
7. Schemaläggningsprompt efter godkänd fas 2.

## Kvalitetsgrindar

- Alla YAML-fall måste vara syntaktiskt giltiga och följa respektive schema.
- Alla obligatoriska E2E-scenarier måste finnas.
- Testmanifestet måste täcka profilskapande, källstrategi, aktualitet, betydelse, deduplicering, rapportformat, osäkerhet och schemaläggning.
- Kritiska beteenden ligger fortsatt i canonical instruktion; Knowledge är fördjupning.
- Live-resultat kan variera med nyhetsläget och bedöms därför mot kvalitetskriterier snarare än exakta artiklar.

## Kända begränsningar

Den deterministiska projektvalideringen kör inte en extern språkmodell och kan därför inte ensam bevisa semantisk kvalitet i verkliga webbsökningar. Detta hanteras genom scenarioevals och följs upp i distributions-/runtime-valideringen i nästa steg.
