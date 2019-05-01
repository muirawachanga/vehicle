from __future__ import unicode_literals

from frappe import _


def get_data():
    return [
        {
            "label": _("Fleet Management"),
            "icon": "icon-star",
            "items": [
                {
                    "type": "doctype",
                    "name": "Vehicle Details",
                    "description": _("Vehicle details provision.")
                },
                {
                    "type": "doctype",
                    "name": "Assign and contribution contract",
                    "description": _("Feed in the contribution for the vehicle")
                },
                {
                    "type": "doctype",
                    "name": "Maintenance and repair",
                    "description": _("Feed in the maintenance logs")
                },
                {
                    "type": "doctype",
                    "name": "Insurance",
                    "description": _("Feed in the insurance details")
                },


            ]
        },
        {
            "label": _("Setup"),
            "icon": "icon-star",
            "items": [
                {
                    "type": "doctype",
                    "name": "Vehicle Management Setting",
                    "description": _("Vehicle management settings for the system")
                }
            ]
        },
        {
            "label": _("Vehicle Overview"),
            "icon": "icon-star",
            "items": [
               # {
               #   "type": "doctype",
               #    "name": "Maintenance Visits",
               #    "description": _("Maintenance Visits of the vehicle booking in the system")
               # },
                {
                    "type": "doctype",
                    "name": "Vehicle Owner Contract",
                    "description": _("This carter for any agreement between the owner of the vehicle")
                },
                {
                    "type": "doctype",
                    "name": "Vehicle Remittance",
                    "description": _("Carters for how much the owner of the vehicle is remitted")
                },
                {
                    "type": "doctype",
                    "name": "Remittance Payment",
                    "description": _("Explain the amount the owner should be given")
                }

            ]
        },
        {
			"label": _("Main Reports"),
			"icon": "fa fa-table",
			"items": [
                {
                    "type": "report",
                    "name": "Daily summary",
                    "doctype": "Assign and contribution contract",
                    "is_query_report": True,
                },
                {
                    "type": "page",
                    "name": "sales-analytics",
                    "label": _("Sales Analytics"),
                    "icon": "fa fa-bar-chart",
                },
				{
					"type": "report",
					"name":"General Ledger",
					"doctype": "GL Entry",
					"is_query_report": True,
				},
				{
                    "type": "report",
                    "name": "Trial Balance",
                    "doctype": "GL Entry",
                    "is_query_report": True,
                },
                {
                    "type": "report",
                    "name": "Balance Sheet",
                    "doctype": "GL Entry",
                    "is_query_report": True
                },
                {
                    "type": "report",
                    "name": "Cash Flow",
                    "doctype": "GL Entry",
                    "is_query_report": True
                },
                {
                    "type": "report",
                    "name": "Profit and Loss Statement",
                    "doctype": "GL Entry",
                    "is_query_report": True
                },
            ]
        },

		{
			"label": _("Other Reports"),
			"icon": "fa fa-table",
			"items": [
				{
					"type": "report",
					"name": "Trial Balance for Party",
					"doctype": "GL Entry",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Profitability Analysis",
					"doctype": "GL Entry",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Payment Period Based On Invoice Date",
					"is_query_report": True,
					"doctype": "Journal Entry"
				},
				{
					"type": "report",
					"name": "Item-wise Sales Register",
					"is_query_report": True,
					"doctype": "Sales Invoice"
				},
				{
					"type": "report",
					"name": "Item-wise Purchase Register",
					"is_query_report": True,
					"doctype": "Purchase Invoice"
				},
				{
					"type": "report",
					"name": "Accounts Receivable Summary",
					"doctype": "Sales Invoice",
					"is_query_report": True
				},
				{
					"type": "report",
					"name": "Accounts Payable Summary",
					"doctype": "Purchase Invoice",
					"is_query_report": True
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Customer Credit Balance",
					"doctype": "Customer"
				}
			]
		}

    ]
