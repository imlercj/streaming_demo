# Data Streaming Demo

Dette prosjektet demonstrerer hvordan man kan bruke TimescaleDB-utvidelsen i PostgreSQL for å effektivt motta og lagre en kontinuerlig strøm av data. Løsningen er løst basert på et eksempel fra https://github.com/timescale/examples og ble laget som et eksempel i forbindelse med en intern Podcase jeg spilte inn i Bouvet.

## Datakilde

I dette tilfellet benyttes en datastrøm fra **portwind.no**, som leverer sanntids vinddata fra fire målestasjoner i og rundt Stavanger. Det hentes inn data hvert minutt, med sekundvise målinger av både vindhastighet og vindretning.

## Installasjon
Start systemet med følgende kommando:

```bash
docker-compose up
```

## Bruk

1. Et **Grafana-dashboard** er satt opp for visualisering av dataene.
2. Dataene kan også utforskes i **Jupyter Lab**.
Begge verktøyene kjører i egne Docker-kontainere.
