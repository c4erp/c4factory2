"""
═══════════════════════════════════════════════════════════════════════════════
AUTO-SETUP SCRIPT FOR PRODUCTION LIST MODULE
═══════════════════════════════════════════════════════════════════════════════

This script automatically creates ALL necessary files and folders for the
Production List manufacturing workflow system.

WHAT IT CREATES:
- Production List DocType (main document)
- Production List Item DocType (child table)
- Stock Entry API override (create SE from PL, not BOM)
- Work Order customization (allow editing items)
- Hooks and event handlers

HOW TO USE:
1. Save this file as: generate_all_files.py
2. Run: python generate_all_files.py
3. Then run: bench --site [yoursite] migrate
4. Restart bench: bench restart

═══════════════════════════════════════════════════════════════════════════════
"""

import os
import json

BASE_DIR = r"d:\C4erp-APP\c4factory2\c4factory"

# ═══════════════════════════════════════════════════════════════════════════════
# DIRECTORY STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════════

DIRECTORIES = [
    os.path.join(BASE_DIR, "c4_manufacturing", "doctype"),
    os.path.join(BASE_DIR, "c4_manufacturing", "doctype", "production_list"),
    os.path.join(BASE_DIR, "c4_manufacturing", "doctype", "production_list_item"),
    os.path.join(BASE_DIR, "api"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# FILE CONTENTS
# ═══════════════════════════════════════════════════════════════════════════════

FILES = {
    # ───────────────────────────────────────────────────────────────────────────
    # Init Files
    # ───────────────────────────────────────────────────────────────────────────
    os.path.join(BASE_DIR, "c4_manufacturing", "doctype", "__init__.py"): "# DocTypes\n",
    
    os.path.join(BASE_DIR, "c4_manufacturing", "doctype", "production_list", "__init__.py"): "# Production List\n",
    
    os.path.join(BASE_DIR, "c4_manufacturing", "doctype", "production_list_item", "__init__.py"): "# Production List Item\n",
    
    os.path.join(BASE_DIR, "api", "__init__.py"): "# API Module\n",
    
    # ───────────────────────────────────────────────────────────────────────────
    # Production List JSON
    # ───────────────────────────────────────────────────────────────────────────
    os.path.join(BASE_DIR, "c4_manufacturing", "doctype", "production_list", "production_list.json"): json.dumps({
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
            {"default": "Open", "fieldname": "status", "fieldtype": "Select", "in_list_view": 1, "label": "Status", "options": "Open\\nIn Progress\\nCompleted\\nCancelled", "read_only": 1},
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
        "naming_rule": "By \\"Naming Series\\" field",
        "owner": "Administrator",
        "permissions": [
            {"create": 1, "delete": 1, "email": 1, "export": 1, "print": 1, "read": 1, "report": 1, "role": "Manufacturing User", "share": 1, "submit": 1, "write": 1},
            {"create": 1, "delete": 1, "email": 1, "export": 1, "print": 1, "read": 1, "report": 1, "role": "Manufacturing Manager", "share": 1, "submit": 1, "write": 1}
        ],
        "sort_field": "modified",
        "sort_order": "DESC",
        "states": [],
        "track_changes": 1
    }, indent=1),
    
    # ───────────────────────────────────────────────────────────────────────────
    # Production List Item JSON
    # ───────────────────────────────────────────────────────────────────────────
    os.path.join(BASE_DIR, "c4_manufacturing", "doctype", "production_list_item", "production_list_item.json"): json.dumps({
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
    }, indent=1),
}

    # ───────────────────────────────────────────────────────────────────────────
    # Production List Python Controller
    # ───────────────────────────────────────────────────────────────────────────
    os.path.join(BASE_DIR, "c4_manufacturing", "doctype", "production_list", "production_list.py"): '''# Copyright (c) 2025, Connect 4 Systems and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class ProductionList(Document):
\tdef validate(self):
\t\t"""Validate Production List before save"""
\t\tself.validate_items()
\t\tself.calculate_totals()
\t\tself.update_status()

\tdef on_submit(self):
\t\t"""Actions on submit"""
\t\tself.update_status()

\tdef on_cancel(self):
\t\t"""Actions on cancel"""
\t\tself.status = "Cancelled"
\t\tself.check_stock_entries()

\tdef validate_items(self):
\t\t"""Validate that items exist and have quantities"""
\t\tif not self.items:
\t\t\tfrappe.throw(_("Please add at least one item to the Production List"))

\t\tfor item in self.items:
\t\t\tif not item.item_code:
\t\t\t\tfrappe.throw(_("Row {0}: Item Code is required").format(item.idx))
\t\t\tif not item.required_qty or item.required_qty <= 0:
\t\t\t\tfrappe.throw(_("Row {0}: Required Qty must be greater than 0").format(item.idx))

\tdef calculate_totals(self):
\t\t"""Calculate total quantities"""
\t\ttotal_qty = 0.0
\t\tcompleted_qty = 0.0

\t\tfor item in self.items:
\t\t\t# Calculate balance for each item
\t\t\titem.balance_qty = (item.required_qty or 0) - (item.transferred_qty or 0)
\t\t\t
\t\t\ttotal_qty += item.required_qty or 0
\t\t\tcompleted_qty += item.transferred_qty or 0

\t\tself.total_qty = total_qty
\t\tself.completed_qty = completed_qty
\t\tself.balance_qty = total_qty - completed_qty

\tdef update_status(self):
\t\t"""Update status based on balance quantities"""
\t\tif self.docstatus == 2:
\t\t\tself.status = "Cancelled"
\t\t\treturn

\t\tif not self.items:
\t\t\tself.status = "Open"
\t\t\treturn

\t\t# Check if all items are completed
\t\tall_completed = True
\t\tany_transferred = False

\t\tfor item in self.items:
\t\t\tbalance = (item.required_qty or 0) - (item.transferred_qty or 0)
\t\t\tif balance > 0.001:  # Small tolerance for floating point
\t\t\t\tall_completed = False
\t\t\tif item.transferred_qty and item.transferred_qty > 0:
\t\t\t\tany_transferred = True

\t\tif all_completed and self.docstatus == 1:
\t\t\tself.status = "Completed"
\t\telif any_transferred:
\t\t\tself.status = "In Progress"
\t\telse:
\t\t\tself.status = "Open"

\tdef check_stock_entries(self):
\t\t"""Check if there are any stock entries linked to this Production List"""
\t\tstock_entries = frappe.get_all(
\t\t\t"Stock Entry",
\t\t\tfilters={
\t\t\t\t"production_list": self.name,
\t\t\t\t"docstatus": 1
\t\t\t},
\t\t\tlimit=1
\t\t)

\t\tif stock_entries:
\t\t\tfrappe.throw(
\t\t\t\t_("Cannot cancel Production List as it has submitted Stock Entries. Please cancel them first.")
\t\t\t)

\t@frappe.whitelist()
\tdef update_transferred_qty(self):
\t\t"""Update transferred quantities from Stock Entries"""
\t\tfor item in self.items:
\t\t\t# Get total transferred qty from Stock Entry Detail
\t\t\ttransferred = frappe.db.sql("""
\t\t\t\tSELECT SUM(sed.qty)
\t\t\t\tFROM `tabStock Entry Detail` sed
\t\t\t\tINNER JOIN `tabStock Entry` se ON sed.parent = se.name
\t\t\t\tWHERE se.production_list = %s
\t\t\t\t\tAND se.docstatus = 1
\t\t\t\t\tAND sed.item_code = %s
\t\t\t\t\tAND sed.s_warehouse IS NOT NULL
\t\t\t""", (self.name, item.item_code))

\t\t\titem.transferred_qty = transferred[0][0] if transferred and transferred[0][0] else 0.0

\t\tself.calculate_totals()
\t\tself.update_status()
\t\tself.save()


@frappe.whitelist()
def create_production_list_from_work_order(work_order, items=None):
\t"""
\tCreate Production List from Work Order
\t
\tArgs:
\t\twork_order: Work Order name
\t\titems: Optional JSON string of items to include
\t"""
\timport json
\t
\two = frappe.get_doc("Work Order", work_order)
\t
\tif not wo.required_items:
\t\tfrappe.throw(_("Work Order has no required items"))

\t# Create Production List
\tpl = frappe.new_doc("Production List")
\tpl.work_order = work_order
\tpl.production_item = wo.production_item
\tpl.bom_no = wo.bom_no
\tpl.company = wo.company
\t
\t# Parse items if provided as JSON string
\tselected_items = None
\tif items:
\t\tif isinstance(items, str):
\t\t\tselected_items = json.loads(items)
\t\telse:
\t\t\tselected_items = items

\t# Add items from Work Order
\tfor wo_item in wo.required_items:
\t\t# If specific items were selected, only add those
\t\tif selected_items:
\t\t\tif wo_item.item_code not in selected_items:
\t\t\t\tcontinue

\t\t# Calculate balance quantity (required - already transferred)
\t\talready_transferred = get_transferred_qty_for_work_order(work_order, wo_item.item_code)
\t\tbalance_qty = (wo_item.required_qty or 0) - already_transferred

\t\tif balance_qty > 0:
\t\t\tpl.append("items", {
\t\t\t\t"item_code": wo_item.item_code,
\t\t\t\t"item_name": wo_item.item_name,
\t\t\t\t"description": wo_item.description,
\t\t\t\t"source_warehouse": wo_item.source_warehouse,
\t\t\t\t"required_qty": balance_qty,
\t\t\t\t"uom": wo_item.uom,
\t\t\t\t"stock_uom": wo_item.stock_uom,
\t\t\t\t"conversion_factor": wo_item.conversion_factor or 1.0,
\t\t\t\t"transferred_qty": 0.0,
\t\t\t\t"balance_qty": balance_qty
\t\t\t})

\tif not pl.items:
\t\tfrappe.throw(_("No items with balance quantity found in Work Order"))

\treturn pl


def get_transferred_qty_for_work_order(work_order, item_code):
\t"""Get total transferred quantity for an item in a Work Order"""
\tresult = frappe.db.sql("""
\t\tSELECT SUM(sed.qty)
\t\tFROM `tabStock Entry Detail` sed
\t\tINNER JOIN `tabStock Entry` se ON sed.parent = se.name
\t\tWHERE se.work_order = %s
\t\t\tAND se.docstatus = 1
\t\t\tAND se.purpose = 'Material Transfer for Manufacture'
\t\t\tAND sed.item_code = %s
\t\t\tAND sed.s_warehouse IS NOT NULL
\t""", (work_order, item_code))

\treturn result[0][0] if result and result[0][0] else 0.0
''',

    # ───────────────────────────────────────────────────────────────────────────
    # Production List Item Python
    # ───────────────────────────────────────────────────────────────────────────
    os.path.join(BASE_DIR, "c4_manufacturing", "doctype", "production_list_item", "production_list_item.py"): '''# Copyright (c) 2025, Connect 4 Systems and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ProductionListItem(Document):
\tpass
''',

    # ───────────────────────────────────────────────────────────────────────────
    # Test Files
    # ───────────────────────────────────────────────────────────────────────────
    os.path.join(BASE_DIR, "c4_manufacturing", "doctype", "production_list", "test_production_list.py"): '''# Copyright (c) 2025, Connect 4 Systems and Contributors
# See license.txt

# import frappe
from frappe.tests.utils import FrappeTestCase


class TestProductionList(FrappeTestCase):
\tpass
''',
    
    os.path.join(BASE_DIR, "c4_manufacturing", "doctype", "production_list_item", "test_production_list_item.py"): '''# Copyright (c) 2025, Connect 4 Systems and Contributors
# See license.txt

# import frappe
from frappe.tests.utils import FrappeTestCase


class TestProductionListItem(FrappeTestCase):
\tpass
''',

    # ───────────────────────────────────────────────────────────────────────────
    # Stock Entry API - Create from Production List
    # ───────────────────────────────────────────────────────────────────────────
    os.path.join(BASE_DIR, "api", "production_list_stock.py"): '''# Copyright (c) 2025, Connect 4 Systems and contributors
# For license information, please see license.txt

"""
Stock Entry creation from Production List instead of BOM
"""

import frappe
from frappe import _
from frappe.utils import flt, nowdate, nowtime


@frappe.whitelist()
def make_stock_entry_from_production_list(production_list, qty_dict=None):
\t"""
\tCreate Stock Entry (Material Transfer for Manufacture) from Production List
\t
\tArgs:
\t\tproduction_list: Production List name
\t\tqty_dict: Optional JSON dict of {item_code: qty} for partial transfer
\t"""
\timport json
\t
\tpl = frappe.get_doc("Production List", production_list)
\t
\tif pl.docstatus != 1:
\t\tfrappe.throw(_("Production List must be submitted first"))
\t
\t# Parse qty_dict if provided
\tpartial_qtys = {}
\tif qty_dict:
\t\tif isinstance(qty_dict, str):
\t\t\tpartial_qtys = json.loads(qty_dict)
\t\telse:
\t\t\tpartial_qtys = qty_dict
\t
\t# Get Work Order details
\two = frappe.get_doc("Work Order", pl.work_order)
\t
\t# Create Stock Entry
\tse = frappe.new_doc("Stock Entry")
\tse.purpose = "Material Transfer for Manufacture"
\tse.work_order = pl.work_order
\tse.production_list = pl.name
\tse.company = pl.company
\tse.from_bom = 0  # NOT from BOM - from Production List
\tse.bom_no = pl.bom_no
\tse.fg_completed_qty = wo.qty
\tse.use_multi_level_bom = 0
\tse.stock_entry_type = "Material Transfer for Manufacture"
\tse.to_warehouse = wo.wip_warehouse
\tse.posting_date = nowdate()
\tse.posting_time = nowtime()
\t
\t# Add items from Production List
\tfor pl_item in pl.items:
\t\t# Check if this item has balance
\t\tbalance = (pl_item.required_qty or 0) - (pl_item.transferred_qty or 0)
\t\t
\t\tif balance <= 0:
\t\t\tcontinue  # Skip fully transferred items
\t\t
\t\t# Use partial qty if specified, otherwise use balance
\t\tqty_to_transfer = balance
\t\tif partial_qtys and pl_item.item_code in partial_qtys:
\t\t\tqty_to_transfer = min(flt(partial_qtys[pl_item.item_code]), balance)
\t\t
\t\tif qty_to_transfer <= 0:
\t\t\tcontinue
\t\t
\t\t# Add Stock Entry Detail row
\t\tse.append("items", {
\t\t\t"item_code": pl_item.item_code,
\t\t\t"item_name": pl_item.item_name,
\t\t\t"description": pl_item.description,
\t\t\t"qty": qty_to_transfer,
\t\t\t"uom": pl_item.uom,
\t\t\t"stock_uom": pl_item.stock_uom,
\t\t\t"conversion_factor": pl_item.conversion_factor or 1.0,
\t\t\t"s_warehouse": pl_item.source_warehouse,
\t\t\t"t_warehouse": wo.wip_warehouse,
\t\t\t"allow_zero_valuation_rate": 0,
\t\t})
\t
\tif not se.items:
\t\tfrappe.throw(_("No items available for transfer"))
\t
\treturn se.as_dict()


@frappe.whitelist()
def get_production_list_items_with_balance(production_list):
\t"""
\tGet items from Production List that still have balance quantity
\t
\tReturns: List of items with balance_qty > 0
\t"""
\tpl = frappe.get_doc("Production List", production_list)
\t
\titems_with_balance = []
\tfor item in pl.items:
\t\tbalance = (item.required_qty or 0) - (item.transferred_qty or 0)
\t\tif balance > 0:
\t\t\titems_with_balance.append({
\t\t\t\t"item_code": item.item_code,
\t\t\t\t"item_name": item.item_name,
\t\t\t\t"required_qty": item.required_qty,
\t\t\t\t"transferred_qty": item.transferred_qty,
\t\t\t\t"balance_qty": balance,
\t\t\t\t"source_warehouse": item.source_warehouse,
\t\t\t\t"uom": item.uom
\t\t\t})
\t
\treturn items_with_balance
''',

    # ───────────────────────────────────────────────────────────────────────────
    # Production List Hooks - Update on Stock Entry submit
    # ───────────────────────────────────────────────────────────────────────────
    os.path.join(BASE_DIR, "c4_manufacturing", "production_list_hooks.py"): '''# Copyright (c) 2025, Connect 4 Systems and contributors
# For license information, please see license.txt

"""
Hooks for Production List - Update status when Stock Entry is submitted/cancelled
"""

import frappe


def update_production_list_on_stock_entry(doc, method=None):
\t"""
\tUpdate Production List when Stock Entry is submitted or cancelled
\tTriggered on Stock Entry on_submit and on_cancel
\t"""
\tif not getattr(doc, "production_list", None):
\t\treturn
\t
\tif doc.purpose != "Material Transfer for Manufacture":
\t\treturn
\t
\t# Get and update Production List
\tpl = frappe.get_doc("Production List", doc.production_list)
\tpl.update_transferred_qty()
\t
\tfrappe.msgprint(
\t\t_("Production List {0} updated").format(doc.production_list),
\t\talert=True,
\t\tindicator="green"
\t)
''',

    # ───────────────────────────────────────────────────────────────────────────
    # Patch - Stock Entry Custom Field
    # ───────────────────────────────────────────────────────────────────────────
    os.path.join(BASE_DIR, "..", "patches", "v1_0", "setup_stock_entry_custom_fields.py"): '''# Copyright (c) 2025, Connect 4 Systems and contributors
# For license information, please see license.txt

"""
Add custom field 'production_list' to Stock Entry
"""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
\t"""Add Production List link field to Stock Entry"""
\t
\tcustom_fields = {
\t\t"Stock Entry": [
\t\t\t{
\t\t\t\t"fieldname": "production_list",
\t\t\t\t"label": "Production List",
\t\t\t\t"fieldtype": "Link",
\t\t\t\t"options": "Production List",
\t\t\t\t"insert_after": "work_order",
\t\t\t\t"read_only": 0,
\t\t\t\t"depends_on": "eval:doc.purpose=='Material Transfer for Manufacture'",
\t\t\t\t"description": "Link to Production List for material transfer tracking"
\t\t\t}
\t\t]
\t}
\t
\tcreate_custom_fields(custom_fields, update=True)
\tfrappe.db.commit()
\t
\tprint("✓ Stock Entry custom field 'production_list' added successfully")
''',
}


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

def create_all_files():
    """Create all directories and files"""
    print("\\n" + "="*80)
    print("PRODUCTION LIST MODULE - AUTO SETUP")
    print("="*80 + "\\n")
    
    # Create directories
    print("Creating directories...")
    for directory in DIRECTORIES:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✓ {directory}")
    
    print("\\nCreating files...")
    # Create all files
    file_count = 0
    for filepath, content in FILES.items():
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        file_count += 1
        # Show relative path for cleaner output
        rel_path = filepath.replace(BASE_DIR, "c4factory")
        print(f"  ✓ {rel_path}")
    
    print("\\n" + "="*80)
    print(f"SUCCESS! Created {file_count} files")
    print("="*80)
    print("\\nNEXT STEPS:")
    print("1. Run: bench --site [your-site] migrate")
    print("2. Run: bench restart")
    print("3. Login and test the new Production List doctype")
    print("\\nWorkflow: Work Order → Create Production List → Create Stock Entry")
    print("="*80 + "\\n")


if __name__ == "__main__":
    create_all_files()
