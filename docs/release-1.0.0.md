# Release – 1.0.0

Nyhetsbevakaren 1.0.0 är den första stabila releasen.

## Verifiering före release

- `1.0.0-rc.2` har praktiskt provkörts av användaren utan rapporterade blockerande fel.
- Canonical beteende är gemensamt för Chat ZIP och Custom GPT.
- Schemaläggningsprompten skapas som portabel Markdown-fil i båda lägena när filskapande stöds.
- Chat kan dessutom erbjuda direkt Scheduled Task när värdmiljön stöder det och användaren uttryckligen godkänner skapandet.
- Custom GPT och miljöer utan direkt Tasks-stöd använder samma fil som portabel fallback.

## Huvudfunktioner

1. Bygg och kvalitetssäkra en ämnes- och källbaserad nyhetsprofil.
2. Sök och rangordna aktuella nyhetshändelser inom ett angivet tidsfönster.
3. Slå ihop flera artiklar om samma händelse och redovisa flera relevanta källor.
4. Presentera varje vald nyhet med rubrik, 3–5 meningars sammanfattning och klickbara källor.
5. Skapa en självförsörjande prompt för återkommande bevakning som nedladdningsbar Markdown-fil.
6. Erbjud capability-styrd direkt schemaläggning i Chat när Scheduled Tasks finns tillgängligt.

## Releaseprincip

Funktionaliteten från RC.2 är fryst i 1.0.0. Endast release- och statusmetadata har ändrats inför stabil release.
