# Copyright (c) 2025, Connect 4 Systems and contributors
# For license information, please see license.txt

"""
Add custom field 'production_list' to Stock Entry
"""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
	"""Add Production List link field to Stock Entry"""
	
	custom_fields = {
		"Stock Entry": [
			{
				"fieldname": "production_list",
				"label": "Production List",
				"fieldtype": "Link",
				"options": "Production List",
				"insert_after": "work_order",
				"read_only": 0,
				"depends_on": "eval:doc.purpose=='Material Transfer for Manufacture'",
				"description": "Link to Production List for material transfer tracking"
			}
		]
	}
	
	create_custom_fields(custom_fields, update=True)
	frappe.db.commit()
	
	print("✓ Stock Entry custom field 'production_list' added successfully")
