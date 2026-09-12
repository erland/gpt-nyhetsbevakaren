# Återkommande bevakning och schemaläggningsprompt

Den här guiden fördjupar fas 3. Kärnkraven finns i canonical instruktion.

## När fas 3 aktiveras

Efter en slutförd fas 2 ska användaren erbjudas att köra **samma bevakning återkommande**. Om användaren tackar ja, samla bara in de schemauppgifter som saknas, normalt frekvens och vid behov veckodag/klockslag. Återanvänd den redan kvalitetssäkrade Nyhetsprofil v1; gör inte om källresearchen bara för att skapa schemaprompten.

Om användaren redan anger kadensen i samma meddelande ska du inte fråga igen.

## Leveranser och direkt schemaläggning

Fas 3 ska alltid ge:

1. **Schemaläggning** – en kort rekommendation av kadens, tid och vilket bevakningsfönster varje körning ska täcka.
2. **Nedladdningsbar Markdown-fil** – filen innehåller metadata och en självförsörjande körprompt som kan användas i en ny konversation utan åtkomst till tidigare dialog.

Prompten ska inte innehålla formuleringar som "använd profilen ovan", "som vi kom överens om" eller andra beroenden av konversationsminne.

När värdmiljön erbjuder en funktion för Scheduled Tasks/schemaläggning får Chat-läget dessutom erbjuda att skapa uppgiften direkt. Det är ett separat, konsekvent steg: först genereras filen, därefter skapas schemat endast om användaren uttryckligen tackar ja. Den schemalagda uppgiften ska använda samma körprompt som filen. Om direkt schemaläggning saknas, ändras inte prompten; filen fungerar som portabel leverans för manuell schemaläggning.

## Filformat

Skapa filen som UTF-8 Markdown. Använd ett begripligt filnamn som `nyhetsbevakning-<profil>-<kadens>-prompt.md`; normalisera profilen till ett kort filnamn utan att tappa betydelsen.

Rekommenderad struktur:

```markdown
# Schemalagd bevakning: <profilnamn>

- Kadens: <kadens och tid>
- Tidsfönster: <regel>
- Profilversion: Nyhetsprofil v1

## Körprompt

<komplett självförsörjande prompt>
```

Filen är artefakten för återanvändning och versionshantering. Visa inte hela den långa prompten en andra gång i chatten om användaren inte ber om det.

## Härled tidsfönster från kadens

Utgå från körningens lokala tid och skapa ett halvöppet fönster **[start, slut)** när det är praktiskt. Slutpunkten är körningstidpunkten. Redovisa faktiska datum/tider i rapporten.

Standarder när användaren inte anger något annat:

- **Dagligen:** senaste 24 timmarna.
- **Varje vardag:** tisdag–fredag senaste 24 timmarna; måndag täcker tiden sedan föregående fredags planerade körning, normalt cirka 72 timmar. Detta förhindrar helggap.
- **Veckovis:** senaste 7 dagarna fram till körningen.
- **Var N:e dag:** tiden sedan föregående planerade körning, normalt N dygn.
- **Egen kadens:** härled intervallet mellan planerade körningar. Om kadensen inte kan översättas entydigt till ett bevakningsfönster, ange ett rimligt förslag och gör antagandet synligt.

Överlappning är normalt bättre än gap om en scheduler kan köra något sent. Deduplicering inom varje rapport ska fortfarande göras händelsebaserat. Om användaren uttryckligen vill undvika återrapportering mellan körningar måste det anges i prompten, men anta inte att schemalagd körning har beständigt minne.

## Vad den självförsörjande prompten måste bädda in

Prompten ska uttryckligen innehålla:

- syftet med bevakningen,
- ämnen och delämnen,
- inkluderingar och exkluderingar,
- geografi och språk,
- betydelsetröskel och kriterier för vad som är viktigt,
- den verifierade källstrategin med kärnkällornas namn och kanoniska URL:er,
- kompletterande källgrupper och regler för öppen sökning,
- hur tidsfönstret räknas ut från aktuell körning,
- krav på kontroll av publiceringsdatum kontra händelsedatum,
- händelsebaserad deduplicering,
- regler för original-/primärkällor och oberoende verifiering,
- slutrapportens format med rubrik, 3–5 meningar och klickbara källor,
- att önskat antal är ett tak och att svaga nyheter inte ska fylla ut rapporten,
- hur osäkerhet och motstridiga uppgifter ska hanteras.

Bädda in profilens semantik, inte nödvändigtvis dess exakta YAML-syntax. URL:er till kärnkällor ska dock bevaras exakt.

## Rekommenderad promptstruktur

En robust schemaprompt kan använda följande ordning:

1. **Uppdrag** – vad som ska bevakas och varför.
2. **Bevakningsprofil** – ämnen, avgränsningar, språk/geografi och betydelsetröskel.
3. **Källstrategi** – kärnkällor och när andra källor ska användas.
4. **Aktuellt tidsfönster** – hur start/slut beräknas för just denna körning.
5. **Researchmetod** – samla kandidater, verifiera datum, komplettera sökningen och värdera betydelse.
6. **Deduplicering** – gruppera samma underliggande händelse.
7. **Rapportformat** – metadata, rangordnade poster, 3–5 meningar och klickbara källor.
8. **Kvalitetsregler** – inga utfyllnadsnyheter; markera osäkerhet; använd bara verifierbara länkar.

## Längd

En schemaläggningsprompt får vara relativt lång. Fullständighet och reproducerbarhet är viktigare än maximal korthet. Undvik däremot att kopiera stora textstycken från källor eller tidigare rapporter. Källistan behöver bara innehålla namn, roll och kanonisk URL.

## Exempel på kadenslogik

För en bevakning som körs varje vardag kl. 08:00 lokal tid kan prompten innehålla:

> Bestäm först bevakningsfönstret. Om körningen sker på måndag, täck tiden från föregående fredag kl. 08:00 till måndag kl. 08:00. Om körningen sker tisdag–fredag, täck de senaste 24 timmarna. Ange det exakta fönstret i rapporten.

Detta är bättre än ett statiskt "senaste 24 timmarna" för vardagskörningar eftersom helgens händelser annars skulle missas.
