from __future__ import unicode_literals
import frappe

def custom_validate(doc, method):
	for d in doc.get("po_details"):
		if d.is_scrapped_item == "No":
			if not d.rate:
				frappe.throw("Row {0}: Rate is mandatory".format(d.idx))
			if not d.amount:
				frappe.throw("Row {0}: Amount is mandatory".format(d.idx))
			if d.uom != d.stock_uom and d.conversion_factor == 1:
				frappe.throw("Row {0}: Wrong conversion factor entered for UOM conversion".format(d.idx))