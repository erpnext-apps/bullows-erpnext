# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd.
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt

def execute(filters=None):
	columns = get_columns()
	results = get_results(filters)

	return columns, results


def get_columns():
	return ["Project:Link/Project:100", "Project Name::120", "Project Status::110",
		"Customer:Link/Customer:100", "Territory: Link/Territory:100", "Project Value:Currency:120",
		"Estimated Cost RM:Currency:140", "Estimated Cost BO:Currency:140",
		"Total Estimated Cost: Currency:150", "Gross Margin Value:Currency:150",

		'Invoiced Amt (Billable):Currency:160', 'Invoiced Amt (Non-Billable):Currency:160',
		'Pending Invoice Amt:Currency:150', 'Pending Invoice (%):Currency:150', 'GRN Amount:Currency:120',
		'Actual Gross Margin:Currency:150', 'Actual Gross Margin (%):Currency:170']


def get_results(filters):
	project_details = get_project_details(filters)
	projectwise_invoiced_amount = get_invoiced_amount(filters)
	projectwise_received_amount = get_received_amount(filters)

	res = []
	for d in project_details:
		r = [d.name, d.project_name, d.status, d.customer, d.territory, d.project_value,
			d.est_material_cost, d.estimated_cost_bo, d.total_estimated_cost, d.gross_margin_value]

		# Invoiced amount
		billable_invoiced_amount = flt(projectwise_invoiced_amount.get(d.name, {}).get("billable"))
		non_billable_invoiced_amount = flt(projectwise_invoiced_amount.get(d.name, {}).get("non_billable"))

		# Pending to Invoice
		pending_to_invoice = flt(d.project_value) - billable_invoiced_amount
		pending_to_invoice_percentage = pending_to_invoice * 100 / flt(d.project_value) \
			if d.project_value else 0

		# Received Amount
		received_amount = flt(projectwise_received_amount.get(d.name))

		# Gross margin value
		gross_margin = billable_invoiced_amount - received_amount

		# gross margin %
		gross_margin_percentage = gross_margin * 100 / billable_invoiced_amount \
			if billable_invoiced_amount else 0

		r += [billable_invoiced_amount, non_billable_invoiced_amount, pending_to_invoice,
			pending_to_invoice_percentage, received_amount, gross_margin, gross_margin_percentage]

		res.append(r)


	return res

def get_project_details(filters):
	return frappe.db.sql("""
		select
			name, project_name, status, territory, customer, estimated_cost_bo, total_estimated_cost,
			est_material_cost, project_value, gross_margin_value
		from tabProject
		where
			docstatus < 2 and company=%s {conditions}
		""".format(conditions=get_conditions(filters)), filters.company, as_dict=1)

def get_invoiced_amount(filters):
	projectwise_invoiced_amount = frappe._dict()

	conditions = " and project_name={}".format(filters.project) if filters.get("project") else ""

	for si in frappe.db.sql("""select project_name, is_billable, sum(ifnull(net_total, 0)) as amount
		from `tabSales Invoice` where docstatus=1 and posting_date<%s {0}
		group by project_name, is_billable""".format(conditions), filters.get("report_date"), as_dict=1):
			projectwise_invoiced_amount.setdefault(si.project_name, {
				"billable": si.amount if si.is_billable=="Y" else 0,
				"non_billable": si.amount if si.is_billable=="N" else 0
			})

	return projectwise_invoiced_amount

def get_received_amount(filters):
	projectwise_received_amount = frappe._dict()

	conditions = " and project_name={}".format(filters.project) if filters.get("project") else ""

	for pr in frappe.db.sql("""select t2.project_name, sum(t2.amount) as amount
		from `tabPurchase Receipt` t1, `tabPurchase Receipt Item` t2
		where t1.name = t2.parent and t2.docstatus = 1 and t1.posting_date <= %s {0}
		group by t2.project_name""".format(conditions), filters.get("report_date"), as_dict=1):
			projectwise_received_amount.setdefault(pr.project_name, pr.amount)

	return projectwise_received_amount

def get_conditions(filters):
	conditions = ""
	if filters.get("customer"):
		conditions += " and customer={0}".format(filters.customer)
	if filters.get("project"):
		conditions += " and name={0}".format(filters.project)

	return conditions
