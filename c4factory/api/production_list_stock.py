# Copyright (c) 2025, Connect 4 Systems and contributors
# For license information, please see license.txt

"""
Stock Entry creation from Production List instead of BOM
"""

import frappe
from frappe import _
from frappe.utils import flt, nowdate, nowtime


@frappe.whitelist()
def make_stock_entry_from_production_list(production_list, qty_dict=None):
	"""
	Create Stock Entry (Material Transfer for Manufacture) from Production List
	
	Args:
		production_list: Production List name
		qty_dict: Optional JSON dict of {item_code: qty} for partial transfer
	"""
	import json
	
	pl = frappe.get_doc("Production List", production_list)
	
	if pl.docstatus != 1:
		frappe.throw(_("Production List must be submitted first"))
	
	# Parse qty_dict if provided
	partial_qtys = {}
	if qty_dict:
		if isinstance(qty_dict, str):
			partial_qtys = json.loads(qty_dict)
		else:
			partial_qtys = qty_dict
	
	# Get Work Order details
	wo = frappe.get_doc("Work Order", pl.work_order)
	
	# Create Stock Entry
	se = frappe.new_doc("Stock Entry")
	se.purpose = "Material Transfer for Manufacture"
	se.work_order = pl.work_order
	se.production_list = pl.name
	se.company = pl.company
	se.from_bom = 0  # NOT from BOM - from Production List
	se.bom_no = pl.bom_no
	se.fg_completed_qty = wo.qty
	se.use_multi_level_bom = 0
	se.stock_entry_type = "Material Transfer for Manufacture"
	se.to_warehouse = wo.wip_warehouse
	se.posting_date = nowdate()
	se.posting_time = nowtime()
	
	# Add items from Production List
	for pl_item in pl.items:
		# Check if this item has balance
		balance = (pl_item.required_qty or 0) - (pl_item.transferred_qty or 0)
		
		if balance <= 0:
			continue  # Skip fully transferred items
		
		# Use partial qty if specified, otherwise use balance
		qty_to_transfer = balance
		if partial_qtys and pl_item.item_code in partial_qtys:
			qty_to_transfer = min(flt(partial_qtys[pl_item.item_code]), balance)
		
		if qty_to_transfer <= 0:
			continue
		
		# Add Stock Entry Detail row
		se.append("items", {
			"item_code": pl_item.item_code,
			"item_name": pl_item.item_name,
			"description": pl_item.description,
			"qty": qty_to_transfer,
			"uom": pl_item.uom,
			"stock_uom": pl_item.stock_uom,
			"conversion_factor": pl_item.conversion_factor or 1.0,
			"s_warehouse": pl_item.source_warehouse,
			"t_warehouse": wo.wip_warehouse,
			"allow_zero_valuation_rate": 0,
		})
	
	if not se.items:
		frappe.throw(_("No items available for transfer"))
	
	return se.as_dict()


@frappe.whitelist()
def get_production_list_items_with_balance(production_list):
	"""
	Get items from Production List that still have balance quantity
	
	Returns: List of items with balance_qty > 0
	"""
	pl = frappe.get_doc("Production List", production_list)
	
	items_with_balance = []
	for item in pl.items:
		balance = (item.required_qty or 0) - (item.transferred_qty or 0)
		if balance > 0:
			items_with_balance.append({
				"item_code": item.item_code,
				"item_name": item.item_name,
				"required_qty": item.required_qty,
				"transferred_qty": item.transferred_qty,
				"balance_qty": balance,
				"source_warehouse": item.source_warehouse,
				"uom": item.uom
			})
	
	return items_with_balance
