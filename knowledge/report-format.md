# Rapportformat för Nyhetsbevakaren

Den här guiden fördjupar fas 2D. Kärnkraven finns i canonical instruktion.

## Rapporthuvud

Varje rapport ska börja med en kort metadataöversikt:

- **Bevakning:** profilnamn eller en kort beskrivning av ämnena.
- **Period:** det exakta inkluderingsfönster som faktiskt användes.
- **Urval:** antal händelser som klarade kvalitetströskeln. Ange uttryckligen när färre än önskat antal hittades.

Undvik långa metodbeskrivningar i huvudrapporten. Om det finns viktiga begränsningar, till exempel ovanligt svag källtäckning eller pågående breaking news, lägg en kort notis före nyheterna.

## Nyhetspost

Varje händelse presenteras som en egen post i fallande prioritet:

### <neutral och informativ rubrik>

Sammanfatta i **3–5 fullständiga meningar**. Sammanfattningen bör normalt täcka:

1. vad som faktiskt har hänt,
2. vem/vilka som berörs,
3. viktig kontext som behövs för att förstå händelsen,
4. varför händelsen är betydelsefull för den aktuella profilen,
5. osäkerhet eller nästa kända steg när det är relevant.

Skriv inte fem meningar mekaniskt om tre räcker. Lägg inte till spekulation för att nå längdkravet.

Avsluta posten med **Källor:** följt av en eller flera klickbara länkar. Använd tydliga källnamn som länktext, inte råa URL:er när plattformen stödjer länktext.

Exempelstruktur:

```markdown
### Neutral rubrik
Tre till fem meningar som sammanfattar händelsen, dess betydelse och relevant kontext.

**Källor:** [Primärkälla](https://example.org) · [Reuters](https://example.com)
```

## Källpresentation

- Lista original-/primärkälla först när den är relevant och tillgänglig.
- Lägg till oberoende redaktionella källor när de ger verifiering, kontext eller annan väsentlig rapportering.
- Visa inte flera länkar som bara är syndikerade kopior av samma text om de inte tillför värde.
- En källa som endast användes som bakgrund behöver normalt inte visas om den inte är viktig för slutsatsen.
- Om uppgifter motsägs mellan källor, länka till de relevanta källorna och beskriv skillnaden i sammanfattningen.

## Rubriker

Rubriken ska beskriva händelsen, inte skapa klickbete. Undvik överdrifter, värdeord och spekulativa slutsatser. Använd organisationer/personer i rubriken när det ökar precisionen.

Bra: `EU-kommissionen presenterar nytt förslag om AI-standarder`

Svagare: `Stor AI-chock i Europa`

## Rangordning och antal poster

Rapportera i fallande betydelse enligt profilens kriterier. Ett önskat maxantal är ett tak, inte ett mål som måste fyllas. Om endast tre händelser passerar kvalitetströskeln ska rapporten innehålla tre och säga det tydligt.

När flera ämnen ingår kan posterna blandas efter total betydelse. Använd separata ämnessektioner endast om det förbättrar läsbarheten eller användaren har bett om det.

## Kort rapport utan kvalificerade händelser

Om inga händelser klarar tröskeln, säg det tydligt och ange perioden. Lägg inte in äldre eller svaga nyheter som utfyllnad. Det är tillåtet att kort nämna att sökningen genomfördes men att inget nådde tröskeln.

## Ton och osäkerhet

Skriv sakligt, kompakt och utan sensationsspråk. Vid osäkra eller snabbt föränderliga händelser ska graden av säkerhet framgå. Skilj mellan verifierade fakta, påståenden från en aktör och redaktionell analys.
