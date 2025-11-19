"""
PART 2: Create Python controller files
Run this after create_all_files.py
"""

import os

base = r"d:\C4erp-APP\c4factory2\c4factory\c4_manufacturing\doctype"

print("="*80)
print("CREATING PYTHON CONTROLLER FILES")
print("="*80)

# Production List Python controller
pl_py = '''# Copyright (c) 2025, Connect 4 Systems and contributors
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
'''

pl_py_path = os.path.join(base, "production_list", "production_list.py")
with open(pl_py_path, 'w', encoding='utf-8') as f:
    f.write(pl_py)
print(f"✓ Created: {pl_py_path}")

# Production List Item Python
pli_py = '''# Copyright (c) 2025, Connect 4 Systems and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class ProductionListItem(Document):
\tpass
'''

pli_py_path = os.path.join(base, "production_list_item", "production_list_item.py")
with open(pli_py_path, 'w', encoding='utf-8') as f:
    f.write(pli_py)
print(f"✓ Created: {pli_py_path}")

# Test files
test_pl = '''# Copyright (c) 2025, Connect 4 Systems and Contributors
# See license.txt

from frappe.tests.utils import FrappeTestCase


class TestProductionList(FrappeTestCase):
\tpass
'''

test_pli = '''# Copyright (c) 2025, Connect 4 Systems and Contributors  
# See license.txt

from frappe.tests.utils import FrappeTestCase


class TestProductionListItem(FrappeTestCase):
\tpass
'''

test_pl_path = os.path.join(base, "production_list", "test_production_list.py")
with open(test_pl_path, 'w', encoding='utf-8') as f:
    f.write(test_pl)
print(f"✓ Created: {test_pl_path}")

test_pli_path = os.path.join(base, "production_list_item", "test_production_list_item.py")
with open(test_pli_path, 'w', encoding='utf-8') as f:
    f.write(test_pli)
print(f"✓ Created: {test_pli_path}")

# Production List JavaScript (UI buttons)
pl_js = '''// Copyright (c) 2025, Connect 4 Systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Production List', {
\trefresh: function(frm) {
\t\t// Add "Create Stock Entry" button for submitted PLs with balance
\t\tif (frm.doc.docstatus === 1 && frm.doc.status !== 'Completed') {
\t\t\tfrm.add_custom_button(__('Stock Entry'), function() {
\t\t\t\tfrappe.call({
\t\t\t\t\tmethod: "c4factory.api.production_list_stock.make_stock_entry_from_production_list",
\t\t\t\t\targs: {
\t\t\t\t\t\tproduction_list: frm.doc.name
\t\t\t\t\t},
\t\t\t\t\tcallback: function(r) {
\t\t\t\t\t\tif (r.message) {
\t\t\t\t\t\t\tvar doc = frappe.model.sync(r.message);
\t\t\t\t\t\t\tfrappe.set_route("Form", "Stock Entry", doc[0].name);
\t\t\t\t\t\t}
\t\t\t\t\t}
\t\t\t\t});
\t\t\t}, __('Create'));
\t\t}

\t\t// Add "Update Transferred Qty" button
\t\tif (frm.doc.docstatus === 1) {
\t\t\tfrm.add_custom_button(__('Update Transferred Qty'), function() {
\t\t\t\tfrm.call('update_transferred_qty').then(() => {
\t\t\t\t\tfrm.reload_doc();
\t\t\t\t});
\t\t\t}, __('Actions'));
\t\t}

\t\t// Add "Get Items with Balance" button
\t\tif (frm.doc.docstatus === 1) {
\t\t\tfrm.add_custom_button(__('View Balance Items'), function() {
\t\t\t\tfrappe.call({
\t\t\t\t\tmethod: "c4factory.api.production_list_stock.get_production_list_items_with_balance",
\t\t\t\t\targs: {
\t\t\t\t\t\tproduction_list: frm.doc.name
\t\t\t\t\t},
\t\t\t\t\tcallback: function(r) {
\t\t\t\t\t\tif (r.message && r.message.length > 0) {
\t\t\t\t\t\t\tlet msg = '<table class="table table-bordered"><thead><tr>' +
\t\t\t\t\t\t\t\t'<th>Item Code</th><th>Item Name</th><th>Required</th>' +
\t\t\t\t\t\t\t\t'<th>Transferred</th><th>Balance</th></tr></thead><tbody>';
\t\t\t\t\t\t\t
\t\t\t\t\t\t\tr.message.forEach(item => {
\t\t\t\t\t\t\t\tmsg += `<tr><td>${item.item_code}</td><td>${item.item_name}</td>` +
\t\t\t\t\t\t\t\t\t`<td>${item.required_qty}</td><td>${item.transferred_qty}</td>` +
\t\t\t\t\t\t\t\t\t`<td><b>${item.balance_qty}</b></td></tr>`;
\t\t\t\t\t\t\t});
\t\t\t\t\t\t\t
\t\t\t\t\t\t\tmsg += '</tbody></table>';
\t\t\t\t\t\t\t
\t\t\t\t\t\t\tfrappe.msgprint({
\t\t\t\t\t\t\t\ttitle: __('Items with Balance'),
\t\t\t\t\t\t\t\tmessage: msg,
\t\t\t\t\t\t\t\twide: true
\t\t\t\t\t\t\t});
\t\t\t\t\t\t} else {
\t\t\t\t\t\t\tfrappe.msgprint(__('All items have been fully transferred'));
\t\t\t\t\t\t}
\t\t\t\t\t}
\t\t\t\t});
\t\t\t}, __('Actions'));
\t\t}
\t}
});
'''

pl_js_path = os.path.join(base, "production_list", "production_list.js")
with open(pl_js_path, 'w', encoding='utf-8') as f:
    f.write(pl_js)
print(f"✓ Created: {pl_js_path}")

print("\n" + "="*80)
print("ALL PYTHON AND JAVASCRIPT FILES CREATED!")
print("="*80)
print("\nAll files are ready. Now run:")
print("  bench --site your-site migrate")
print("  bench --site your-site clear-cache")
print("  bench restart")
