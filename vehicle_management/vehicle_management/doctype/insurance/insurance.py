# -*- coding: utf-8 -*-
# Copyright (c) 2019, stephen and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import date_diff, add_days, flt, nowdate, getdate
from frappe.model.document import Document

class Insurance(Document):
	def validate(self):
		self.validate_dates()


	def validate_dates(self):
		last_inv = get_last_tc_invoice(self.vehicle)
		if last_inv:
			start_date_inv = getdate(last_inv.get('start_date'))
			end_date_inv = getdate(last_inv.get('end_date'))
			start_date = getdate(self.start_date)
			end_date = getdate(self.end_date)
			diff = date_diff(end_date, start_date) + 1
			if start_date_inv <= start_date <= end_date_inv:
				frappe.msgprint(_('The dates correspond from what is in the invoice, dates has been regenerated'))
				self.set('start_date', add_days(end_date_inv, 1))
				self.set('end_date', add_days(end_date_inv, diff))

@frappe.whitelist()
def make_invoice(amount, name=None):
	source = frappe.get_doc('Insurance', name)
	if source:
		if source.insurance_company:
			invoice = frappe.new_doc('Purchase Invoice')
			# default_customer = load_configuration('default_customer_for_invoice')
			# if not source.driver_employee and not source.driver_customer:
			# 	frappe.throw(_('Please set default customer in the vehicle management Settings'))
			# if source.driver_customer:
			# 	invoice.driver_customer = source.driver_customer
			# else:
			# 	invoice.driver_employee = source.driver_employee
			item = source.select_item_for_insurance
			if not item:
				frappe.throw(_('Please set default item in the vehicle management Settings'))
			sync_items(invoice, item, amount, source.cost_center, source.expense_account)
			invoice.start_date = getdate(source.start_date)
			invoice.end_date = getdate(source.end_date)
			invoice.vehicle = source.vehicle
			invoice.supplier = source.insurance_company
			invoice.insurance_policy = source.name
			# invoice.run_method("set_missing_values")
			invoice.save()
			invoice.submit()
			frappe.msgprint(_('Invoice created successfully for {0}'.format(source.vehicle)))
			return invoice


def get_last_tc_invoice(name):
	"""
	Load the last invoice of a particular vehicle contract
	"""
	doc = frappe.get_all("Purchase Invoice", ["name"], [["docstatus", "!=", 2], ["is_return", "!=", 1],
														["vehicle", "=", name]],
						 order_by="creation desc", limit_page_length=1)
	if doc:
		return frappe.get_doc("Purchase Invoice", doc[0].name)
	else:
		return None
# Todo make sure the purhase invoice item is purchase item when doing the query.
# Todo make sure the expense account is not a group, still when you are doing the query
def sync_items(invoice, items, amount, cost_center, expense_account):
	invoice.items = []
	invoice.append('items', dict(
		item_code = items,
		item_name = items,
		qty = 1.00,
		rate = amount,
		amount =amount,
		cost_center = cost_center,
		expense_account = expense_account,
		conversion_factor = 1,
		uom= 'Nos'
	))
	return invoice.as_dict()
