# drawio-er-diagram-generate
Generate drawio ER diagram from existing database tables. Supports Postgres currently

### Command line execution:

> **usage:**
>
> python generate_erd.py [-h] [-t DB_TYPE] -a HOST [-p PORT] -d DATABASE -u USERNAME -k PASSWORD [-o OUTPUT_PATH]

### options:

| Option                                    | Description                                          |
|-------------------------------------------|------------------------------------------------------|
| -t DB_TYPE, --db-type DB_TYPE             | Database type (default: postgres)                    |
| -a HOST, --host HOST                      | sql database host                                    |
| -p PORT, --port PORT                      | sql database port                                    |
| -d DATABASE, --database DATABASE          | sql database name                                    |
| -u USERNAME, --username USERNAME          | sql database username                                |
| -k PASSWORD, --password PASSWORD          | sql database password                                |
| -o OUTPUT_PATH, --output-path OUTPUT_PATH | Diagram output file path (default: er_gen.drawio)    |
