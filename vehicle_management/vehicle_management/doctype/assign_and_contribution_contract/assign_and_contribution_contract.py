# -*- coding: utf-8 -*-
# Copyright (c) 2019, stephen and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import date_diff, add_days, flt, nowdate, getdate
from frappe.model.document import Document
import calendar

class Assignandcontributioncontract(Document):

	def validate(self):
		validate_dates(self)
		validate_vehicle(self)
		self.set_not_available()

	def tabulate_data(self):
		if (self.start_date and self.end_date):
			diff = date_diff(self.end_date, self.start_date) + 1
			for i in range(diff):
				date = getdate(add_days(self.start_date, i))
				self.get_details(date)
				i += 1
			self.calculate_total()

	def get_details(self, date):
		ex = [e for e in self.get('contributions') if str(e.date) == str(date)]
		if ex:
			ex[0].amount_deposited = self.amount_per_day
			return
		else:
			contribution = self.append('contributions', {})
			contribution.vehicle = self.vehicle
			contribution.employee = self.employee_name or self.customer_name
			contribution.date = date
			contribution.day = calendar.day_name[getdate(date).weekday()]
			contribution.amount_deposited = self.amount_per_day

	def set_not_available(self):
		if self.status == 'Active':
			veh_doc = frappe.get_doc('Vehicle Details', self.vehicle)
			veh_doc.set('vehicle_status', 'Not available')
			veh_doc.save()

	def set_available(self):
		if self.status == 'Terminated' or self.status == 'Reassigned':
			veh_doc = frappe.get_doc('Vehicle Details', self.vehicle)
			veh_doc.set('vehicle_status', 'Available')
			veh_doc.save()


	def calculate_total(self):
		if self.total_amount <= 0.000:
			for rows in self.get('contributions'):
				self.total_amount += rows.amount_deposited
			self.total_amount_expected = 0.000

def validate_dates(self):
	last_inv = get_last_tc_invoice(self.vehicle)
	if last_inv:
		start_date_inv = getdate(last_inv.get('start_date'))
		end_date_inv = getdate(last_inv.get('end_date'))
		start_date = getdate(self.start_date)
		end_date = getdate(self.end_date)
		diff = date_diff(end_date, start_date) + 1
		if start_date_inv <= start_date <= end_date_inv:
			self.set('start_date', add_days(end_date_inv, 1))
			self.set('end_date', add_days(end_date_inv, diff))
			frappe.msgprint(_('The dates correspond from what is in the invoice, dates has been regenerated'))

def validate_vehicle(self):
	if self.status == 'Active':
		get_vehicle_status = frappe.get_value('Vehicle Details', self.vehicle, 'vehicle_status')
		if get_vehicle_status == 'Not available':
			self.set('vehicle', '')
			frappe.throw(_('Cannot save, the vehicle is already assigned to another contract !!!'))



@frappe.whitelist()
def make_invoice(vehicle, amount, mode_of_payment, name=None, customer=None):
	source = frappe.get_doc('Assign and contribution contract', name)
	if source:
		validate_dates(source)
		source.save()
		invoice = frappe.new_doc('Sales Invoice')
		default_customer = load_configuration('default_customer_for_invoice')
		if not default_customer and not customer:
			frappe.throw(_('Please set default customer in the vehicle management Settings'))
		if customer:
			invoice.customer = customer
		else:
			invoice.customer = default_customer
		item = load_configuration('default_item_name')
		if not item:
			frappe.throw(_('Please set default item in the vehicle management Settings'))
		invoice.append('items', dict(item_code = item, qty = 1, rate = amount, cost_center= get_cost_center(vehicle)))
		invoice.is_pos = 1
		invoice.append('payments', dict(mode_of_payment=mode_of_payment, amount=amount))
		invoice.date_start = getdate(source.start_date)
		invoice.end_date = getdate(source.end_date)
		invoice.vehicle = source.vehicle
		invoice.driver = source.customer_name or source.employee_name
		# invoice.run_method("set_missing_values")
		invoice.save()
		invoice.submit()
		frappe.msgprint(_('Invoice created successfully for {0}'.format(source.vehicle)))
		return invoice

def load_configuration(name, default=None):
	val = frappe.db.get_single_value('Vehicle Management Setting', name)
	if val is None:
		val = default
	return val

def get_last_tc_invoice(name):
	"""
	Load the last invoice of a particular vehicle contract
	"""
	doc = frappe.get_all("Sales Invoice", ["name"], [["docstatus", "!=", 2], ["is_return", "!=", 1],
													 ["vehicle", "=", name]],
						 order_by="creation desc", limit_page_length=1)
	if doc:
		return frappe.get_doc("Sales Invoice", doc[0].name)
	else:
		return None

def get_cost_center(vehicle):
	''' this is used to return cost center '''
	cost_center = frappe.get_value('Vehicle Details', vehicle, 'vehicle_cost_center')
	if cost_center:
		return cost_center