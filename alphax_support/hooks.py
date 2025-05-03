app_name = "alphax_support"
app_title = "Alphax Support"
app_publisher = "Neotec"
app_description = "Report an Issue"
app_email = "Neotec@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "alphax_support",
# 		"logo": "/assets/alphax_support/logo.png",
# 		"title": "Alphax Support",
# 		"route": "/alphax_support",
# 		"has_permission": "alphax_support.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/alphax_support/css/alphax_support.css"
# app_include_js = "/assets/alphax_support/js/alphax_support.js"
app_include_js = [
    "/assets/alphax_support/js/helpdesk_custom.js"
]

# include js, css files in header of web template
# web_include_css = "/assets/alphax_support/css/alphax_support.css"
# web_include_js = "/assets/alphax_support/js/alphax_support.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "alphax_support/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "alphax_support/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "alphax_support.utils.jinja_methods",
# 	"filters": "alphax_support.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "alphax_support.install.before_install"
# after_install = "alphax_support.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "alphax_support.uninstall.before_uninstall"
# after_uninstall = "alphax_support.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "alphax_support.utils.before_app_install"
# after_app_install = "alphax_support.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "alphax_support.utils.before_app_uninstall"
# after_app_uninstall = "alphax_support.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "alphax_support.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# doc_events = {
#     "Support Ticket": {
#         "after_insert": "alphax_support.utils.send_ticket_email",
#         "autoname": "alphax_support.utils.set_ticket_id"
#     }
# }


doc_events = {
    "HD Ticket": {
        "after_insert": "alphax_support.support.notification.send_ticket_notification"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"alphax_support.tasks.all"
# 	],
# 	"daily": [
# 		"alphax_support.tasks.daily"
# 	],
# 	"hourly": [
# 		"alphax_support.tasks.hourly"
# 	],
# 	"weekly": [
# 		"alphax_support.tasks.weekly"
# 	],
# 	"monthly": [
# 		"alphax_support.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "alphax_support.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "alphax_support.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "alphax_support.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["alphax_support.utils.before_request"]
# after_request = ["alphax_support.utils.after_request"]

# Job Events
# ----------
# before_job = ["alphax_support.utils.before_job"]
# after_job = ["alphax_support.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"alphax_support.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

fixtures = [
    {"doctype": "Custom Field", "filters": [["dt", "in", ["HD Ticket", "HD Ticket Template"]]]},
    {"dt": "Client Script", "filters": [["name", "in", ["HD Ticket Custom View", "HD Ticket Auto Set and Dependency", "HD Ticket List View Custom"]]]},
    {"dt": "HD Ticket Template"},
    {"dt": "HD Ticket Template Field"}
]
# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

