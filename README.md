# Data Streaming Demo

Dette prosjektet demonstrerer hvordan en kan bruke TimescaleDB extention i Postgres til å effektivt ta i mot en strøm av data. 

## Datakilde

I dette tilfellet er det brukt en strøm av vinddata portwind.no som strømmes inn. Det hentes data fra 4 stasjoner i og rundt Stavanger. Lasten blir gjort hvert minutt of inneholder sekundsmålinger for vindhastighet og vindrettning. 

## Installasjon

Kjør `docker-compose up`

## Bruk

1. Det er satt opp en Grafana dashboard
2. En kan utforske dataene i Jupyter Lab

Begge er spunnet opp i egne kontainere.