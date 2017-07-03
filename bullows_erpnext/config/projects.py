from frappe import _

def get_data():
	return [
		{
			"label": _("Bullows Reports"),
			"icon": "icon-paper-clip",
			"items": [
				{
					"type": "report",
					"is_query_report": True,
					"name": "Projectwise Invoiced Amount and Cost",
					"doctype": "Project",
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Projectwise Costs and Expenses",
					"doctype": "Project",
				}
			]
		}
	]
