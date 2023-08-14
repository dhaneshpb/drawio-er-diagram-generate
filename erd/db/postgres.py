import psycopg2
from psycopg2.extras import RealDictCursor


def get_table_json_list(
        host: str = "localhost",
        port: int = 5432,
        database: str = "postgres",
        user: str = "postgres",
        password: str = "") -> list:

    conn = psycopg2.connect(user=user,
                            password=password,
                            host=host,
                            port=port,
                            database=database)

    query = """
    SELECT DISTINCT
        SDTables.table_catalog as database_name,
        SDTables.table_schema as parent_schema,
        SDTables.table_name as parent_table,
        SDColumns.column_name as column_name,
        SDColumns.ordinal_position as column_order,
        SDColumns.data_type as data_type,
        SDColumns.character_maximum_length as column_size,
        SDConstraints.constraint_type as constraint_type,
        SDKeys2.table_schema as child_schema,
        SDKeys2.table_name as child_table,
        SDKeys2.column_name as child_column
    FROM 
        information_schema.tables SDTables
        NATURAL LEFT JOIN 
            information_schema.columns SDColumns
        LEFT JOIN (
            information_schema.key_column_usage SDKeys
            NATURAL JOIN 
                information_schema.table_constraints SDConstraints
            NATURAL LEFT JOIN 
                information_schema.referential_constraints SDReference
        )
        ON SDColumns.table_catalog=SDKeys.table_catalog 
            AND SDColumns.table_schema=SDKeys.table_schema 
            AND SDColumns.table_name=SDKeys.table_name 
            AND SDColumns.column_name=SDKeys.column_name
        LEFT JOIN 
            information_schema.key_column_usage SDKeys2
        ON SDKeys.position_in_unique_constraint=SDKeys2.ordinal_position 
            AND SDReference.unique_constraint_catalog=SDKeys2.constraint_catalog 
            AND SDReference.unique_constraint_schema=SDKeys2.constraint_schema 
            AND SDReference.unique_constraint_name=SDKeys2.constraint_name
    WHERE 
        SDTables.TABLE_TYPE='BASE TABLE' 
        AND SDTables.table_schema NOT IN('information_schema','pg_catalog')
    ORDER BY 
        parent_schema, parent_table, column_order
    """

    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(query)
    tables = cur.fetchall()
    conn.close()

    return tables
