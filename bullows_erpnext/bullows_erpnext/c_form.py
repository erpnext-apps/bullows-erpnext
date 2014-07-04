from __future__ import unicode_literals
import frappe

def validate_mandatory_attachment(doc, method):
	if not doc.file_list:
		frappe.throw("Please upload c-form attachment before submitting")