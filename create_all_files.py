"""
COMPLETE FILE GENERATOR - Run this to create ALL missing files
This will create the Production List module completely
"""

import os
import json

print("="*80)
print("CREATING ALL PRODUCTION LIST FILES")
print("="*80)

# Base directory
base = r"d:\C4erp-APP\c4factory2\c4factory"

# Step 1: Create all directories
print("\n1. Creating directories...")
dirs = [
    os.path.join(base, "c4_manufacturing", "doctype"),
    os.path.join(base, "c4_manufacturing", "doctype", "production_list"),
    os.path.join(base, "c4_manufacturing", "doctype", "production_list_item"),
]

for d in dirs:
    os.makedirs(d, exist_ok=True)
    print(f"   ✓ {d}")

# Step 2: Create __init__.py files
print("\n2. Creating init files...")

init_files = {
    os.path.join(base, "c4_manufacturing", "doctype", "__init__.py"): "# DocTypes\n",
    os.path.join(base, "c4_manufacturing", "doctype", "production_list", "__init__.py"): "# Production List\n",
    os.path.join(base, "c4_manufacturing", "doctype", "production_list_item", "__init__.py"): "# Production List Item\n",
}

for filepath, content in init_files.items():
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"   ✓ {filepath}")

# Step 3: Create Production List JSON
print("\n3. Creating Production List JSON...")

pl_json = {
    "actions": [],
    "allow_rename": 1,
    "autoname": "naming_series:",
    "creation": "2025-01-19 09:00:00.000000",
    "doctype": "DocType",
    "editable_grid": 1,
    "engine": "InnoDB",
    "field_order": [
        "naming_series", "work_order", "production_item", "bom_no",
        "column_break_4", "company", "posting_date", "posting_time",
        "section_break_7", "items", "section_break_9",
        "status", "total_qty", "completed_qty", "balance_qty", "amended_from"
    ],
    "fields": [
        {"fieldname": "naming_series", "fieldtype": "Select", "label": "Series", "options": "PL-.YYYY.-", "reqd": 1},
        {"fieldname": "work_order", "fieldtype": "Link", "in_list_view": 1, "label": "Work Order", "options": "Work Order", "reqd": 1},
        {"fetch_from": "work_order.production_item", "fieldname": "production_item", "fieldtype": "Link", "label": "Production Item", "options": "Item", "read_only": 1},
        {"fetch_from": "work_order.bom_no", "fieldname": "bom_no", "fieldtype": "Link", "label": "BOM No", "options": "BOM", "read_only": 1},
        {"fieldname": "column_break_4", "fieldtype": "Column Break"},
        {"fetch_from": "work_order.company", "fieldname": "company", "fieldtype": "Link", "label": "Company", "options": "Company", "reqd": 1},
        {"default": "Today", "fieldname": "posting_date", "fieldtype": "Date", "label": "Posting Date", "reqd": 1},
        {"default": "Now", "fieldname": "posting_time", "fieldtype": "Time", "label": "Posting Time", "reqd": 1},
        {"fieldname": "section_break_7", "fieldtype": "Section Break", "label": "Items"},
        {"fieldname": "items", "fieldtype": "Table", "label": "Production List Items", "options": "Production List Item", "reqd": 1},
        {"fieldname": "section_break_9", "fieldtype": "Section Break", "label": "Status & Summary"},
        {"default": "Open", "fieldname": "status", "fieldtype": "Select", "in_list_view": 1, "label": "Status", "options": "Open\nIn Progress\nCompleted\nCancelled", "read_only": 1},
        {"fieldname": "total_qty", "fieldtype": "Float", "label": "Total Qty", "read_only": 1},
        {"fieldname": "completed_qty", "fieldtype": "Float", "label": "Completed Qty", "read_only": 1},
        {"fieldname": "balance_qty", "fieldtype": "Float", "label": "Balance Qty", "read_only": 1},
        {"fieldname": "amended_from", "fieldtype": "Link", "label": "Amended From", "no_copy": 1, "options": "Production List", "print_hide": 1, "read_only": 1}
    ],
    "index_web_pages_for_search": 1,
    "is_submittable": 1,
    "links": [],
    "modified": "2025-01-19 09:00:00.000000",
    "modified_by": "Administrator",
    "module": "C4 Manufacturing",
    "name": "Production List",
    "naming_rule": "By \"Naming Series\" field",
    "owner": "Administrator",
    "permissions": [
        {"create": 1, "delete": 1, "email": 1, "export": 1, "print": 1, "read": 1, "report": 1, "role": "Manufacturing User", "share": 1, "submit": 1, "write": 1},
        {"create": 1, "delete": 1, "email": 1, "export": 1, "print": 1, "read": 1, "report": 1, "role": "Manufacturing Manager", "share": 1, "submit": 1, "write": 1}
    ],
    "sort_field": "modified",
    "sort_order": "DESC",
    "states": [],
    "track_changes": 1
}

pl_json_path = os.path.join(base, "c4_manufacturing", "doctype", "production_list", "production_list.json")
with open(pl_json_path, 'w') as f:
    json.dump(pl_json, f, indent=1)
print(f"   ✓ {pl_json_path}")

# Step 4: Create Production List Item JSON
print("\n4. Creating Production List Item JSON...")

pli_json = {
    "actions": [],
    "creation": "2025-01-19 09:00:00.000000",
    "doctype": "DocType",
    "editable_grid": 1,
    "engine": "InnoDB",
    "field_order": [
        "item_code", "item_name", "description",
        "column_break_3", "source_warehouse",
        "section_break_5", "required_qty", "transferred_qty", "balance_qty",
        "section_break_8", "uom", "stock_uom", "conversion_factor"
    ],
    "fields": [
        {"fieldname": "item_code", "fieldtype": "Link", "in_list_view": 1, "label": "Item Code", "options": "Item", "reqd": 1},
        {"fetch_from": "item_code.item_name", "fieldname": "item_name", "fieldtype": "Data", "in_list_view": 1, "label": "Item Name", "read_only": 1},
        {"fetch_from": "item_code.description", "fieldname": "description", "fieldtype": "Text Editor", "label": "Description"},
        {"fieldname": "column_break_3", "fieldtype": "Column Break"},
        {"fieldname": "source_warehouse", "fieldtype": "Link", "label": "Source Warehouse", "options": "Warehouse"},
        {"fieldname": "section_break_5", "fieldtype": "Section Break", "label": "Quantity"},
        {"fieldname": "required_qty", "fieldtype": "Float", "in_list_view": 1, "label": "Required Qty", "reqd": 1},
        {"fieldname": "transferred_qty", "fieldtype": "Float", "in_list_view": 1, "label": "Transferred Qty", "read_only": 1},
        {"fieldname": "balance_qty", "fieldtype": "Float", "in_list_view": 1, "label": "Balance Qty", "read_only": 1},
        {"fieldname": "section_break_8", "fieldtype": "Section Break", "label": "UOM"},
        {"fetch_from": "item_code.stock_uom", "fieldname": "uom", "fieldtype": "Link", "label": "UOM", "options": "UOM"},
        {"fetch_from": "item_code.stock_uom", "fieldname": "stock_uom", "fieldtype": "Link", "label": "Stock UOM", "options": "UOM", "read_only": 1},
        {"default": "1", "fieldname": "conversion_factor", "fieldtype": "Float", "label": "Conversion Factor"}
    ],
    "index_web_pages_for_search": 1,
    "istable": 1,
    "links": [],
    "modified": "2025-01-19 09:00:00.000000",
    "modified_by": "Administrator",
    "module": "C4 Manufacturing",
    "name": "Production List Item",
    "owner": "Administrator",
    "permissions": [],
    "sort_field": "modified",
    "sort_order": "DESC",
    "states": []
}

pli_json_path = os.path.join(base, "c4_manufacturing", "doctype", "production_list_item", "production_list_item.json")
with open(pli_json_path, 'w') as f:
    json.dump(pli_json, f, indent=1)
print(f"   ✓ {pli_json_path}")

print("\n" + "="*80)
print("ALL FILES CREATED SUCCESSFULLY!")
print("="*80)
print("\nNEXT STEPS:")
print("1. Run: bench --site your-site migrate")
print("2. Run: bench --site your-site clear-cache")
print("3. Run: bench restart")
print("\nThe Production List module is ready to use!")
print("="*80)
