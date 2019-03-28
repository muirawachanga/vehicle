# Copyright (c) 2013, steve and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.desk.reportview import build_match_conditions

def execute(filters=None):
	# if not filters:
	# 	filters = {}
	# elif filters.get("start_date") or filters.get("to_date"):
	# 	filters["from_time"] = "00:00:00"
	# 	filters["to_time"] = "24:00:00"

	columns = get_column()
	conditions = get_conditions(filters)
	data = get_data(conditions, filters)

	return columns, data

def get_column():
	return [_("Vehicle") + ":Link/Vehicle Details:120", _("Customer") + ":Link/Customer:150", _("Customer name") + "::150",
			_("Status") + "::150", _("Start Date") + "::140", _("End Date") + "::140", _("Total amount") + "::150"]

def get_data(conditions, filters):
	vehicle_details = frappe.db.sql(""" select `tabAssign and contribution contract`.vehicle, `tabAssign and contribution contract`.customer, `tabAssign and contribution contract`.customer_name,
		`tabVehicle Details`.vehicle_status, `tabAssign and contribution contract`.start_date, `tabAssign and contribution contract`.end_date, `tabAssign and contribution contract`.total_amount
		 from `tabAssign and contribution contract`, `tabVehicle Details` where
		`tabAssign and contribution contract`.vehicle = `tabVehicle Details`.vehicle_registration and %s order by `tabAssign and contribution contract`.vehicle"""% conditions, filters, as_list=1)

	return vehicle_details

def get_conditions(filters):
	conditions = "`tabAssign and contribution contract`.status = 'Active'"
	if filters.get("start_date"):
		conditions += " and `tabAssign and contribution contract`.start_date >= date(%(start_date)s)"
	if filters.get("end_date"):
		conditions += " and `tabAssign and contribution contract`.end_date <= date(%(end_date)s)"
	if filters.get("status"):
		conditions += "and `tabVehicle Details`.vehicle_status = ('%s')" % filters.get("status")
	match_conditions = build_match_conditions("Assign and contribution contract")
	if match_conditions:
		conditions += " and %s" % match_conditions

	return conditions