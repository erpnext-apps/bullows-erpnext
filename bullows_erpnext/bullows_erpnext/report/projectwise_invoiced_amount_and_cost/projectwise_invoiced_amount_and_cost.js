// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.query_reports["Projectwise Invoiced Amount and Cost"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("company"),
			"reqd": 1
		},
		{
			"fieldname":"project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": 'Project',
		},
		{
			"fieldname":"report_date",
			"label": __("Date"),
			"fieldtype": "Date",
			"default": get_today(),
			"reqd": 1
		},
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": 'Customer',
		},
	]
}
