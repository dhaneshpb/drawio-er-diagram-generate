
import itertools
from math import ceil

from .model import ERTable
from .db.postgres import get_table_json_list
from .constants import *


def execute(
        output_path: str,
        db_type: str = "postgres",
        host: str = "localhost",
        port: int = 5432,
        database: str = "postgres",
        user: str = "postgres",
        password: str = "postgres"):

    if db_type == "postgres":
        tables = get_table_json_list(host, port, database, user, password)
    else:
        raise Exception(f"DB Type {db_type} is not supported currently")
    id_iter = itertools.count()

    tables_dict = {}
    column_count = {}
    level_size = {"L1": 0, "L2": 0, "L3": 0, "L4": 0}

    # Create table and column objects
    for column_json in tables:
        table_name = column_json['parent_table']
        if table_name not in tables_dict:
            tables_dict[table_name] = ERTable(column_json, id_iter)
            column_count[table_name] = 2
        else:
            tables_dict[table_name].add_column(column_json, id_iter)
            column_count[table_name] = column_count[table_name] + 1

    max_height = row_height * max(column_count.values())

    # Identify references
    for table_er in tables_dict.values():
        for ref_tbl, ref_cols in table_er.references.items():
            ref_by_table = tables_dict[ref_tbl]
            ref_by_table.set_referenced_by(ref_by_table.table_name, ref_cols)

    # Classify tables to levels and lanes in UI
    for table_er in tables_dict.values():
        rfs_flag = len(table_er.references) > 0
        rfb_flag = len(table_er.referenced_by) > 0
        if rfb_flag:
            if rfs_flag:
                table_er.ui_level = "L2"
                level_size["L2"] = level_size["L2"] + 1
            else:
                table_er.ui_level = "L1"
                level_size["L1"] = level_size["L1"] + 1
        else:
            if rfs_flag:
                table_er.ui_level = "L3"
                level_size["L3"] = level_size["L3"] + 1
            else:
                table_er.ui_level = "L4"
                level_size["L4"] = level_size["L4"] + 1

    level_lanes = dict((l, ceil(s/x_count)) for (l, s) in level_size.items())
    level_x_counter = dict((lvl, 1) for lvl in level_size.keys())
    level_y_counter = dict((lvl, 1) for lvl in level_size.keys())

    # Set table UI coordinates
    for table_er in tables_dict.values():
        if level_x_counter[table_er.ui_level] < (x_count + 1):
            pos_x = level_x_counter[table_er.ui_level]
            level_x_counter[table_er.ui_level] = level_x_counter[table_er.ui_level] + 1
            pos_y = level_y_counter[table_er.ui_level]
        else:
            level_x_counter[table_er.ui_level] = 1
            pos_x = level_x_counter[table_er.ui_level]
            level_y_counter[table_er.ui_level] = level_y_counter[table_er.ui_level] + 1
            pos_y = level_y_counter[table_er.ui_level]
        if table_er.ui_level != "L1":
            pos_y = pos_y + level_lanes["L1"]
            if table_er.ui_level != "L2":
                pos_y = pos_y + level_lanes["L2"]
                if table_er.ui_level != "L3":
                    pos_y = pos_y + level_lanes["L3"]
        table_er.set_offsets(max_height, pos_x, pos_y)

    er_xml_body = "\n".join(list(map(lambda t: t.get_table_xml(), tables_dict.values())))

    # Setup connectors
    for table_er in tables_dict.values():
        for column_name in table_er.ref_cols:
            column_er = table_er.columns_dict[column_name]
            target_column_id = column_er.column_id
            for ref_table, ref_columns in column_er.references.items():
                source_table_er = tables_dict[ref_table]
                for ref_column in ref_columns:
                    ref_col_er = source_table_er.columns_dict[ref_column]
                    source_column_id = ref_col_er.column_id
                    component_counter = next(id_iter)
                    connector_id = f"{component_uid}-{component_counter}"
                    connector_params = {
                        "connector_id": connector_id,
                        "source_id": source_column_id,
                        "target_id": target_column_id,
                    }
                    er_xml_body = er_xml_body + connector_syntax.format(**connector_params)

    page_height = (sum(level_y_counter.values()) * (max_height + table_gap)) + table_gap

    er_xml_header_final = er_xml_header.format(
        page_uid=page_uid, default_page_width=default_page_width, page_height=page_height)
    er_xml = er_xml_header_final + er_xml_body + er_xml_footer

    if output_path.endswith(".drawio"):
        pass
    elif output_path.endswith("/"):
        output_path = f"{output_path}/er_gen.drawio"
    elif output_path.endswith("\\"):
        output_path = f"{output_path}\\er_gen.drawio"

    with open(output_path, 'w') as out_file:
        out_file.write(er_xml)
