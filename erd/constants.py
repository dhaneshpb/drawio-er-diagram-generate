import string
import random

# Generate IDs

uid_len = 20
component_uid = str(''.join(
    random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=uid_len)))
page_uid = str(''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=uid_len)))

# defaults
default_key_width = 30
default_col_width = 240
default_typ_width = 120
row_height = 30
default_table_width = default_key_width + default_col_width + default_typ_width
table_gap = 150
x_count = 7
default_page_width = (default_table_width * x_count) + (table_gap * (x_count + 1))

# Graphics
table_header_color = "#006666"  # "#303030"
table_entries_color = "#009999"  # "#5C5C5C"
border_color = "#CCFFFF"  # "#D1D1D1"
font_color = "#E2E2E2"


table_xml_syntax = """
        <mxCell id="{table_id}" value="{table_name}" style="shape=table;startSize=30;container=1;collapsible=1;childLayout=tableLayout;fixedRows=1;rowLines=0;fontStyle=1;align=center;resizeLast=1;flipH=0;flipV=0;direction=east;fillColor={table_header_color};fontColor={font_color};swimlaneFillColor={table_entries_color};strokeWidth=0.2;strokeColor={border_color};rounded=1;" parent="1" vertex="1">
          <mxGeometry x="{offset_x}" y="{offset_y}" width="{total_width}" height="{total_height}" as="geometry" />
        </mxCell>
"""
column_xml_syntax = """
        <mxCell id="{column_parent_id}" value="" style="shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;fillColor=none;collapsible=0;dropTarget=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;strokeColor=inherit;top=0;left=0;right=0;bottom=0;" parent="{table_id}" vertex="1">
          <mxGeometry y="{column_y_offset}" width="{total_width}" height="{row_height}" as="geometry" />
        </mxCell>
        <mxCell id="{column_key_id}" value="{column_key}" style="shape=partialRectangle;overflow=hidden;connectable=0;fillColor=none;strokeColor=inherit;top=0;left=0;bottom=0;right=0;fontStyle=0;fontColor={font_color};" parent="{column_parent_id}" vertex="1">
          <mxGeometry width="{key_width}" height="{row_height}" as="geometry">
            <mxRectangle width="{key_width}" height="{row_height}" as="alternateBounds" />
          </mxGeometry>
        </mxCell>
        <mxCell id="{column_name_id}" value="{column_name}" style="shape=partialRectangle;overflow=hidden;connectable=0;fillColor=none;align=left;strokeColor=inherit;top=0;left=0;bottom=0;right=0;spacingLeft=6;fontStyle=0;fontColor={font_color};" parent="{column_parent_id}" vertex="1">
          <mxGeometry x="{column_name_x_offset}" width="{column_name_width}" height="{row_height}" as="geometry">
            <mxRectangle width="{column_name_width}" height="{row_height}" as="alternateBounds" />
          </mxGeometry>
        </mxCell>
        <mxCell id="{column_typ_id}" value="{column_type}" style="shape=partialRectangle;overflow=hidden;connectable=0;fillColor=none;align=right;strokeColor=inherit;top=0;left=0;bottom=0;right=0;spacingLeft=6;fontStyle=0;spacingRight=6;fontColor={font_color};" parent="{column_parent_id}" vertex="1">
          <mxGeometry x="{column_typ_x_offset}" width="{column_typ_width}" height="{row_height}" as="geometry">
            <mxRectangle width="{column_typ_width}" height="{row_height}" as="alternateBounds" />
          </mxGeometry>
        </mxCell>
"""
connector_syntax = """
    <mxCell id="{connector_id}" style="edgeStyle=orthogonalEdgeStyle;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;startArrow=ERone;startFill=0;endArrow=ERmany;endFill=0;endSize=14;startSize=14;jumpSize=10;rounded=1;" parent="1" source="{source_id}" target="{target_id}" edge="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
"""

er_xml_header = """<mxfile host="Electron" version="21.6.5" type="device">
  <diagram name="Page-1" id="{page_uid}">
    <mxGraphModel dx="1036" dy="606" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" 
        page="1" pageScale="1" pageWidth="{default_page_width}" pageHeight="{page_height}" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
"""

er_xml_footer = """
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
