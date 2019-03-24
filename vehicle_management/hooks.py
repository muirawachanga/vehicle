# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "vehicle_management"
app_title = "Vehicle Management"
app_publisher = "stephen"
app_description = "This app help anyone with a vehicle to manages for lease or normal use"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "wachangasteve@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/vehicle_management/css/vehicle_management.css"
# app_include_js = "/assets/vehicle_management/js/vehicle_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/vehicle_management/css/vehicle_management.css"
# web_include_js = "/assets/vehicle_management/js/vehicle_management.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "vehicle_management.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------
fixtures = [
    {
        "dt": "Custom Field",
        "filters":[["name", "in", ['Sales Invoice-remittance_references', 'Assign and contribution contract-workflow_state', 'Vehicle Owner Contract-workflow_state',
                                   'Purchase Invoice-vehicle_insured', 'Purchase Invoice-maintenance_and_repair', 'Purchase Invoice-insurance_policy', 'Purchase Invoice-driver_employee',
                                   'Purchase Invoice-driver_customer', 'Purchase Invoice-start_date', 'Purchase Invoice-vehicle', 'Purchase Invoice-end_date', 'Sales Invoice-column_break',
                                   'Sales Invoice-date_start', 'Sales Invoice-end_date', 'Sales Invoice-driver', 'Sales Invoice-vehicle', 'Sales Invoice-vehicle_details']]]
    },
    {
        "dt": "Custom Script",
        "filters":[["name", "in", ['Journal Entry-Client']]]
    },
    {
        "dt": "Workflow",
        "filters":[["name", "in", ['Assign Vehicle', 'Vehicle Owner Contract']]]
    },
    {
        "dt": "Workflow Action",
        "filters":[["name", "in", ['Reassign', 'Activate', 'Cancel', 'Suspend','Terminate','Reject', 'Approve']]]
    },
    {
        "dt": "Workflow State",
        "filters":[["name", "in", ['Reassigned', 'New', 'Active', 'Terminated', 'Suspended', 'Rejected', 'Cancelled']]]
    }
]


# before_install = "vehicle_management.install.before_install"
# after_install = "vehicle_management.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "vehicle_management.notifications.get_notification_config"

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

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"vehicle_management.tasks.all"
# 	],
# 	"daily": [
# 		"vehicle_management.tasks.daily"
# 	],
# 	"hourly": [
# 		"vehicle_management.tasks.hourly"
# 	],
# 	"weekly": [
# 		"vehicle_management.tasks.weekly"
# 	]
# 	"monthly": [
# 		"vehicle_management.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "vehicle_management.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "vehicle_management.event.get_events"
# }

