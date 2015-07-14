# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe.utils import flt, cint
from frappe import _

def validate(doc, method):
	validate_for_stock_item(doc)
	validate_invoice_amount_against_project(doc)
	calculate_excise_amount(doc)

def validate_for_stock_item(doc):
	stock_item_lst = []
	for d in doc.get("items"):
		is_stock_item = frappe.db.get_value("Item", d.item_code, "is_stock_item")
		if is_stock_item == "Yes":
			if d.sales_order and not d.delivery_note:
				dn_exists = frappe.db.sql("""select t1.name
					from `tabDelivery Note` t1, `tabDelivery Note Item` t2
					where t2.against_sales_order = %s and t2.item_code = %s
					and t2.parent=t1.name and t1.docstatus = 1""", (d.sales_order, d.item_code))
				if dn_exists:
					stock_item_lst.append(d.item_code)
				elif not d.delivery_note and not d.sales_order:
					stock_item_lst.append(d.item_code)

	if len(stock_item_lst) > 0 :
		frappe.throw(_("Please create Delivery Note before creating Sales Invoice for item(s) {0} as this is stock item.").format(','.join(stock_item_lst)))

def validate_invoice_amount_against_project(doc):
	if doc.is_billable == 'Y' and doc.project_name:
		billable_invoiced_amount = get_billable_invoiced_amount_against_project(doc)

		proj_val = frappe.db.get_value("Project", doc.project_name, "project_value")

		if (billable_invoiced_amount + flt(doc.base_net_total)) > proj_val:
			frappe.throw(_("Total Value of Project exceeded."))

def update_project_status(doc, method):
	if doc.is_billable == 'Y' and doc.project_name:
		billable_invoiced_amount = get_billable_invoiced_amount_against_project(doc)
		proj_val = frappe.db.get_value("Project", doc.project_name, "project_value")

		status = "Completed" if billable_invoiced_amount == proj_val else "Open"
		frappe.db.set_value("Project", doc.project_name, "status", status)

def get_billable_invoiced_amount_against_project(doc):
	billable_invoiced_amount = frappe.db.sql("""select sum(base_net_total) from `tabSales Invoice`
		where project_name = %s and docstatus = 1
		and is_billable = 'Y'""", doc.project_name)

	billable_invoiced_amount = flt(billable_invoiced_amount[0][0]) if billable_invoiced_amount else 0.0
	return billable_invoiced_amount

def calculate_excise_amount(doc):
	from frappe.utils import money_in_words
	from erpnext.setup.utils import get_company_currency

	doc.excise_amount = sum([flt(d.base_tax_amount) for d in doc.get("taxes")
			if cint(d.is_excise_account) == 1])
	doc.excise_amount_in_words = money_in_words(doc.excise_amount, get_company_currency(doc.company))
