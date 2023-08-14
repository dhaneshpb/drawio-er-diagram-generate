import mysql.connector


def get_table_json_list(
        host: str = "localhost",
        port: int = 3306,
        database: str = "",
        user: str = "",
        password: str = "") -> list:

    conn = mysql.connector.connect(user=user,
                                   passwd=password,
                                   host=host,
                                   port=port,
                                   database=database)

    query = f"""
    SELECT
      DISTINCT '' as database_name,
      SDTables.TABLE_SCHEMA as parent_schema,
      SDTables.TABLE_NAME as parent_table,
      SDColumns.COLUMN_NAME as column_name,
      SDColumns.ORDINAL_POSITION as column_order,
      SDColumns.DATA_TYPE as data_type,
      SDColumns.CHARACTER_MAXIMUM_LENGTH as column_size,
      SDConstraints.CONSTRAINT_TYPE as constraint_type,
      SDKeys.REFERENCED_TABLE_SCHEMA as child_schema,
      SDKeys.REFERENCED_TABLE_NAME as child_table,
      SDKeys.REFERENCED_COLUMN_NAME as child_column
    FROM
      INFORMATION_SCHEMA.TABLES SDTables
      LEFT JOIN INFORMATION_SCHEMA.COLUMNS SDColumns ON SDTables.TABLE_SCHEMA = SDColumns.TABLE_SCHEMA
      AND SDTables.TABLE_NAME = SDColumns.TABLE_NAME
      LEFT JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE SDKeys ON SDColumns.TABLE_SCHEMA = SDKeys.TABLE_SCHEMA
      AND SDColumns.TABLE_NAME = SDKeys.TABLE_NAME
      AND SDColumns.COLUMN_NAME = SDKeys.COLUMN_NAME
      LEFT JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS SDConstraints ON SDKeys.CONSTRAINT_SCHEMA = SDConstraints.CONSTRAINT_SCHEMA
      AND SDKeys.CONSTRAINT_NAME = SDConstraints.CONSTRAINT_NAME
      AND SDKeys.TABLE_SCHEMA = SDConstraints.TABLE_SCHEMA
      AND SDKeys.TABLE_NAME = SDConstraints.TABLE_NAME
    WHERE
      SDTables.TABLE_TYPE = 'BASE TABLE'
      AND SDTables.TABLE_SCHEMA = '{database}'
    ORDER BY
      parent_schema,
      parent_table,
      column_order
    """

    cur = conn.cursor(dictionary=True)
    cur.execute(query)
    tables = cur.fetchall()
    conn.close()

    return tables
