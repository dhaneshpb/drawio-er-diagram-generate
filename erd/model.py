from collections import OrderedDict
from itertools import count as iter_count
from .constants import *


class ERTable:
    def __init__(self, col_json: dict, id_iter: iter_count) -> None:
        component_counter = next(id_iter)
        self.table_id = f"{component_uid}-{component_counter}"
        self.table_name = col_json['parent_table']
        self.table_x_offset = 150
        self.table_y_offset = 150
        self.table_height = 30
        self.ui_level = "L1"
        self.ui_lane = 1
        self.references = {}
        self.referenced_by = {}
        self.ref_cols = []
        init_column = ERColumn(col_json, self.table_id, id_iter)
        self.columns_dict = OrderedDict()
        self.columns_dict[init_column.column_name] = init_column
        self.set_reference(col_json)

    def add_column(self, col_json: dict, id_iter: iter_count) -> None:
        column_name = col_json['column_name']
        if column_name not in self.columns_dict:
            column = ERColumn(col_json, self.table_id, id_iter)
            self.columns_dict[column_name] = column
        else:
            self.columns_dict[column_name].add_constraint(col_json)
        self.set_reference(col_json)

    def set_reference(self, col_json: dict) -> None:
        if col_json['constraint_type'] == "FOREIGN KEY":
            self.ref_cols.append(col_json['column_name'])
            ref_table = col_json['child_table']
            ref_column = col_json['child_column']
            if ref_table not in self.references:
                self.references[ref_table] = [ref_column]
            else:
                self.references[ref_table].append(ref_column)

    def set_referenced_by(self, ref_table: str, ref_columns: list[str]) -> None:
        self.referenced_by[ref_table] = ref_columns

    def set_offsets(self, max_height: int, pos_x: int, pos_y: int) -> None:
        self.table_x_offset = ((pos_x - 1) * default_table_width) + (pos_x * table_gap)
        self.table_y_offset = ((pos_y - 1) * max_height) + (pos_y * table_gap)
        self.table_height = (len(self.columns_dict) + 1) * row_height

    def get_table_params(self) -> dict:
        table_params = {
            "table_id": self.table_id,
            "table_name": self.table_name,
            "offset_x": self.table_x_offset,
            "offset_y": self.table_y_offset,
            "total_width": default_table_width,
            "total_height": self.table_height,
            'table_header_color': table_header_color,
            'table_entries_color': table_entries_color,
            'font_color': font_color,
            'border_color': border_color
        }
        return table_params

    def get_table_xml(self) -> str:
        table_params = self.get_table_params()
        table_xml = table_xml_syntax.format(**table_params)
        for column_name, column_er in self.columns_dict.items():
            column_xml = column_er.get_column_xml()
            table_xml = table_xml + column_xml
        return table_xml


class ERColumn:
    def __init__(self, col_json: dict, table_id: str, id_iter: iter_count) -> None:
        self.column_name = col_json['column_name']
        component_counter = next(id_iter)
        self.column_id = f"{component_uid}-{component_counter}"
        self.table_id = table_id
        self.column_ord = col_json['column_order']
        self.column_type = col_json['data_type']
        self.references = {}

        self.column_keys = []
        if col_json['constraint_type'] == "PRIMARY KEY":
            self.column_keys.append("PK")
        elif col_json['constraint_type'] == "FOREIGN KEY":
            self.column_keys.append("FK")
            self.set_reference(col_json)
        elif col_json['constraint_type'] == "UNIQUE KEY":
            self.column_keys.append("UK")

        component_counter = next(id_iter)
        self.column_key_id = f"{component_uid}-{component_counter}"
        component_counter = next(id_iter)
        self.column_name_id = f"{component_uid}-{component_counter}"
        component_counter = next(id_iter)
        self.column_typ_id = f"{component_uid}-{component_counter}"

    def add_constraint(self, col_json: dict) -> None:
        if col_json['constraint_type'] == "PRIMARY KEY":
            self.column_keys.append("PK")
        elif col_json['constraint_type'] == "FOREIGN KEY":
            self.column_keys.append("FK")
            self.set_reference(col_json)
        elif col_json['constraint_type'] == "UNIQUE KEY":
            self.column_keys.append("UK")

    def set_reference(self, col_json: dict) -> None:
        ref_table = col_json['child_table']
        ref_column = col_json['child_column']
        if ref_table not in self.references:
            self.references[ref_table] = [ref_column]
        else:
            self.references[ref_table].append(ref_column)

    def get_column_params(self) -> dict:
        column_params = {
            "column_parent_id": self.column_id,
            "column_key_id": self.column_key_id,
            "column_name_id": self.column_name_id,
            "column_typ_id": self.column_typ_id,
            "table_id": self.table_id,
            "column_y_offset": self.column_ord * row_height,
            "total_width": default_table_width,
            "row_height": row_height,
            "column_key": ",".join(self.column_keys),
            "key_width": default_key_width,
            "column_name": self.column_name,
            "column_name_x_offset": default_key_width,
            "column_name_width": default_col_width,
            "column_type": self.column_type,
            "column_typ_x_offset": default_key_width + default_col_width,
            "column_typ_width": default_typ_width,
            "font_color": font_color
        }
        return column_params

    def get_column_xml(self) -> str:
        column_params = self.get_column_params()
        column_xml = column_xml_syntax.format(**column_params)
        return column_xml
