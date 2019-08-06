# -*- coding: utf-8 -*-
# Copyright (c) 2019, stephen and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document


class VehicleDetails(Document):
    def create_cost_center(self):
        """
		Create cost center with the name of the property under the selected parent cost center
		"""
        if self.vehicle_registration in (None, ""):
            frappe.msgprint(_("Please set vehicle registration first."))
            self.parent_cost_center = ""
            return
        from erpnext.setup.doctype.company.company import get_name_with_abbr

        real_name = get_name_with_abbr(self.vehicle_registration, self.company)
        # Check if the cost center exists before creating
        if frappe.db.exists("Cost Center", real_name):
            cost_c = frappe.get_doc("Cost Center", real_name)
            if cost_c.parent_cost_center == self.parent_cost_center:
                self.vehicle_cost_center = cost_c.name
                return
            frappe.msgprint(
                _(
                    "A Cost Center with this vehicle exists under another parent. You can make changes only in Cost Centers."
                )
            )
            self.parent_cost_center = cost_c.parent_cost_center
            return

        cost_c = frappe.get_doc(
            {
                "doctype": "Cost Center",
                "cost_center_name": self.vehicle_registration,
                "parent_cost_center": self.parent_cost_center,
                "company": self.company,
                "is_group": 0,
            }
        )
        frappe.db.begin()
        cost_c = cost_c.insert()
        frappe.db.commit()
        self.vehicle_cost_center = cost_c.name
