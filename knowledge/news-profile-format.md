# Nyhetsprofil v1 – format och återanvändning

Nyhetsprofilen är den stabila konfigurationen mellan fas 1, fas 2 och fas 3. Den ska vara lätt att läsa för en människa och samtidigt tillräckligt strukturerad för att kopieras utan tolkningsglidning.

## Rekommenderat YAML-format

```yaml
version: 1
name: "Kort namn"
topics:
  - name: "Huvudämne"
    subtopics: ["Delämne A", "Delämne B"]
scope:
  include: ["...", "..."]
  exclude: ["...", "..."]
  geography: ["Globalt"]
  languages: ["sv", "en"]
importance:
  threshold: high
  criteria: ["stor faktisk påverkan", "väsentligt nytt besked", "betydande policy-/regeländring"]
freshness:
  sensitivity: high
  event_date_priority: true
sources:
  core:
    - name: "Exempelkälla"
      url: "https://example.org/"
      category: primary
      role: "Primärkälla för officiella besked"
  complementary_groups:
    - "etablerade internationella medier"
  outside_core_rules:
    - "Sök utanför kärnan när viktig händelse annars riskerar att missas"
    - "Föredra bättre primärkälla framför återrapportering"
reporting:
  summary_sentences: "3-5"
  deduplicate_by_event: true
  prefer_fewer_strong_items: true
assumptions:
  - "Härledd standard som användaren kan korrigera"
```

## Semantik

- `topics` beskriver **vad** som bevakas; delämnen är sök-/prioriteringshjälp, inte separata rapportkrav.
- `scope` beskriver vad som räknas in respektive bort och vilken geografisk/språklig täckning som eftersträvas.
- `importance` avgör tröskeln för att få plats i rapporten. Volym får inte ersätta betydelse.
- `freshness` beskriver hur känslig bevakningen är för nya utvecklingar och om händelsedatum ska väga tyngre än publiceringsdatum.
- `sources.core` är prioriterade ingångar, aldrig automatiskt en whitelist.
- `complementary_groups` beskriver källtyper som får användas utan att statiskt lista varje domän.
- `outside_core_rules` gör den öppna källstrategin explicit.
- `reporting` låser centrala presentationsregler som ska följa med till fas 3.
- `assumptions` gör härledda standardval synliga och enkla att korrigera.

## Ändringsregler

Små ändringar, exempelvis språk eller en uttrycklig exkludering, uppdaterar bara berörda fält. Ändringar av ämne, geografi eller källkrav kan göra befintlig källstrategi ogiltig; då ska berörda delar av fas 1B köras om innan profilen används vidare.

Tidsfönstret för en enskild körning hör **inte** hemma i profilen. Det anges i fas 2 eller härleds i fas 3 från schemaläggningsfrekvensen.
