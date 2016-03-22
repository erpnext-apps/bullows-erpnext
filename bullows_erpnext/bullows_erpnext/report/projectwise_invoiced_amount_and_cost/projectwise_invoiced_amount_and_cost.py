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
		r = [d.name, d.project, d.status, d.customer, d.territory, d.estimated_costing,
			d.est_material_cost, d.estimated_cost_bo, d.total_estimated_cost, d.gross_margin]

		# Invoiced amount
		billable_invoiced_amount = flt(projectwise_invoiced_amount.get(d.name, {}).get("billable"))
		non_billable_invoiced_amount = flt(projectwise_invoiced_amount.get(d.name, {}).get("non_billable"))

		# Pending to Invoice
		pending_to_invoice = flt(d.estimated_costing) - billable_invoiced_amount
		pending_to_invoice_percentage = pending_to_invoice * 100 / flt(d.estimated_costing) \
			if d.estimated_costing else 0

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
			est_material_cost, estimated_costing, gross_margin
		from tabProject
		where
			docstatus < 2 and company=%(company)s {conditions}
		""".format(conditions=get_conditions(filters)), filters, as_dict=1)

def get_invoiced_amount(filters):
	projectwise_invoiced_amount = frappe._dict()

	conditions = " and project=%(project)s" if filters.get("project") else ""

	for si in frappe.db.sql("""select project, is_billable, sum(ifnull(base_net_total, 0)) as amount
		from `tabSales Invoice` where docstatus=1 and posting_date<%(report_date)s {0}
		group by project, is_billable""".format(conditions), filters, as_dict=1):
			projectwise_invoiced_amount.setdefault(si.project, {
				"billable": 0,
				"non_billable": 0
			})
			if si.is_billable == "Y":
				projectwise_invoiced_amount[si.project]["billable"] = si.amount
			else:
				projectwise_invoiced_amount[si.project]["non_billable"] = si.amount


	return projectwise_invoiced_amount

def get_received_amount(filters):
	projectwise_received_amount = frappe._dict()

	conditions = " and t2.project=%(project)s" if filters.get("project") else ""

	for pr in frappe.db.sql("""select t2.project, sum(t2.base_net_amount) as amount
		from `tabPurchase Receipt` t1, `tabPurchase Receipt Item` t2
		where t1.name = t2.parent and t2.docstatus = 1 and t1.posting_date <= %(report_date)s {0}
		group by t2.project""".format(conditions), filters, as_dict=1):
			projectwise_received_amount.setdefault(pr.project, pr.amount)

	return projectwise_received_amount

def get_conditions(filters):
	conditions = ""
	if filters.get("customer"):
		conditions += " and customer=%(customer)s"
	if filters.get("project"):
		conditions += " and name=%(project)s"

	return conditions
