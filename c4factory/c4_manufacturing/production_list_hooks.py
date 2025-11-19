# Copyright (c) 2025, Connect 4 Systems and contributors
# For license information, please see license.txt

"""
Hooks for Production List - Update status when Stock Entry is submitted/cancelled
"""

import frappe


def update_production_list_on_stock_entry(doc, method=None):
	"""
	Update Production List when Stock Entry is submitted or cancelled
	Triggered on Stock Entry on_submit and on_cancel
	"""
	if not getattr(doc, "production_list", None):
		return
	
	if doc.purpose != "Material Transfer for Manufacture":
		return
	
	# Get and update Production List
	pl = frappe.get_doc("Production List", doc.production_list)
	pl.update_transferred_qty()
	
	frappe.msgprint(
		frappe._("Production List {0} updated").format(doc.production_list),
		alert=True,
		indicator="green"
	)
