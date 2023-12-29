# ES 0. crear (y pullear) repo para tener todo lo de soda en algún lugar
# EN 0. create (and pull) a repo to have somewhere to save all soda stuff

# ES 1. activar entorno virtual (.venv)
# EN 1. activate virtual environment (.venv)
    (primero revisar que estén python, pip y virtualenv actualizados)
    (estar en la carpeta donde vamos a crear el entorno)
    source ./.venv/bin/activate

# 2. pip install -i https://pypi.cloud.soda.io soda-postgres
    (instala Soda Library)

# ES 3. levantar la imagen en Docker de la DB on-prem con
# EN 3. deploy Docker image for an on-prem DB with
    docker run --name sip-of-soda -p 5432:5432 -e POSTGRES_PASSWORD=secret sodadata/soda-adventureworks

# ES 4. crear un archivo de configuración
# EN 4. create a configuration file
    configuration.yml

    TIENE que tener
        data_source adventureworks:
            type: postgres
            connection:
                host: localhost
                username: postgres
                password: secret
                database: postgres
                schema: public

        soda_cloud:  
            host: cloud.us.soda.io
            api_key_id: tu-api-key-id
            api_key_secret: tu-api-key-secret

# ES 5. testear conexión
# EN 5. test connection
    soda test-connection -d adventureworks -c configuration.yml

# ES 6a. crear checks
# EN 6a. create checks
    checks.yml
    e ir armando los checks
## ES 6b. correr checks
## EN 6b. run checks
    soda scan -d adventureworks -c configuration.yml checks.yml [-T templates.yml]

# ES 7. usar soda suggest
# EN 7. use soda suggest
    soda suggest -d adventureworks -c configuration.yml -ds dim_customer
    (te sugiere posibles checkeos)

# ES 8. deployar un soda agent
# EN 8. deploy a soda agent
    nosotros lo armamos en Azure y llevaba varios pasos que no voy a documentar
## ES 8.1. configurar una integración de notificaciones y alertas
## EN 8.1. configure a notification/alert integration
    (usamos Slack)
## ES 8.2. configurar un atributo para los checks
## EN 8.2. configure an attribute for checks 
    dimensión con accuracy (acierto), completeness (completitud), consistency (consistencia), timeliness (temporalidad), validity (validez), y uniqueness (unicidad)
## ES 8.3. configurar un atributo para los datasets
## EN 8.3. configure an attribute for datasets
    dimensión multivariable con los distintos datasets

# ES 9. registrar un dataset para perfilamiento y sampleo
# EN 9. register a dataset for profiling & sampling
    (y aplicarle la dimensión de dataset)

# ES 10. crear un agreement que contenga checks para al menos un dataset
# EN 10. create an agreement with checks for at least one dataset
-
## 10.1. 2 anomaly score
## 10.2. 2 missing checks
-
## ES 10.3. elegir una integración para notificación
## EN 10.3. choose an integration to notify

<PROGRESS>

# ES 11. orquestar 
# EN 11. orchestrate
## 11.1. con Airflow/DBT
## 11.2. con GitHub Actions

# ES 12. crear un reporte
# EN 12. create a report
## ES 12.1 bajarlo a una tabla
## EN 12.1 choose a table for it
    usamos Snowflake
## ES 12.2 usar una herramienta BI
## EN 12.2 use a BI tool
    con PowerBI, armar un reporte para datasets, dimensiones y checkeos

# ES 13. contactar a quien corresponda
# EN 13. get in touch with whoever's relevant