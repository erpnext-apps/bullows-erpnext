app_name = "bullows_erpnext"
app_title = "Bullows-ERPNext"
app_publisher = "Webnotes"
app_description = "Bullows ERPNext Extension"
app_icon = "icon-picture"
app_color = "#2A7E51"
app_email = "developers@erpnext.com"
app_url = "frappe.io"
app_version = "0.0.1"

hide_in_installer = True

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/bullows_erpnext/css/bullows_erpnext.css"
# app_include_js = "/assets/bullows_erpnext/js/bullows_erpnext.js"

# include js, css files in header of web template
# web_include_css = "/assets/bullows_erpnext/css/bullows_erpnext.css"
# web_include_js = "/assets/bullows_erpnext/js/bullows_erpnext.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "bullows_erpnext.install.before_install"
# after_install = "bullows_erpnext.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "bullows_erpnext.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.core.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.core.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Sales Invoice": {
		"validate": "bullows_erpnext.bullows_erpnext.sales_invoice.validate",
	},
	"Purchase Order": {
		"validate": "bullows_erpnext.bullows_erpnext.purchase_order.custom_validate"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"bullows_erpnext.tasks.all"
# 	],
# 	"daily": [
# 		"bullows_erpnext.tasks.daily"
# 	],
# 	"hourly": [
# 		"bullows_erpnext.tasks.hourly"
# 	],
# 	"weekly": [
# 		"bullows_erpnext.tasks.weekly"
# 	]
# 	"monthly": [
# 		"bullows_erpnext.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "bullows_erpnext.install.before_tests"

