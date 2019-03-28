// Copyright (c) 2016, stephen and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Daily summary"] = {
	"filters": [
        {
            "fieldname":"start_date",
            "label": __("Start Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        },
        {
            "fieldname":"end_date",
            "label": __("End Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        },
        {
            "fieldname":"status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": ['Not available', 'Available'],
            "default": 'Not available'
        }
	]
}
