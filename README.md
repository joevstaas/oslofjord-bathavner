# Småbåthavner i Oslofjorden

Godkjent status: **456 polygoner fra 14 kommuner**. Batchen Bærum, Asker, Lier, Drammen og Oslo er godkjent. Ingen neste kommune er startet.

## Åpne på Mac

Pakk ut `oslofjord-bathavner-prosjekt.zip`. Flytt mappen `oslofjord-bathavner` til `~/Prosjekter/`.
Valgfri bildefil: pakk ut `oslofjord-bathavner-bildeunderlag.zip` i samme overordnede mappe slik at innholdet legges inn i samme prosjektmappe. Bevar eksisterende prosjektfiler.

```bash
cd ~/Prosjekter/oslofjord-bathavner
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/validate_project.py
claude
```

Python 3.11 eller nyere anbefales. Installer Python separat dersom det mangler.
Claude Code må være installert separat. Ingen kontoer, API-nøkler eller lokal Claude-konfigurasjon følger med.

## Innhold

- `CLAUDE.md`: korte prosjektinstrukser til Claude Code.
- `docs/METODIKK.md`: full metodikk og kommunelogger.
- `docs/OVERLEVERING.md`: filkart, begrensninger og videreføring.
- `status.json`: gjeldende status, med relative primærstier.
- `data/samlet/`: godkjent samlefil og manifest.
- `data/kommuner/`: kommunevise uttrekk fra samlefilen, med metadata og tilgjengelige kontroll-/kildenotater.
- `archive/original/`: originale leveranser, arbeidsnotater, skript og rådata. Bildeunderlaget legges her fra den separate ZIP-filen.
- `work/`: arbeidsmappe for neste autoriserte kommune.
- `scripts/validate_project.py`: lokal kontroll uten nettverk eller endringer i leveranser.

Godkjenning fjerner ikke klassifiserings-/geometriusikkerhet. Datasettene er ikke offisielle havne- eller eiendomsgrenser.
