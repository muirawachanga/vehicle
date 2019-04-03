# -*- coding: utf-8 -*-
# Copyright (c) 2019, stephen and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _
from frappe.utils import date_diff, add_days, flt, nowdate, getdate, cint
from frappe.model.document import Document


class Maintenanceandrepair(Document):
	def generate_schedule(self):
		self.set('schedules', [])
		frappe.db.sql("""delete from `tabMaintenance checks`
			where parent=%s""", (self.name))
		count = 1
		for d in self.get('maintenance_checks'):
			self.validate_maintenance_detail()
			s_list = []
			s_list = self.create_schedule_list(d.start_date, d.end_date, d.no_of_visits)
			for i in range(d.no_of_visits):
				child = self.append('schedules')
				# child.item_code = d.item_code
				# child.item_name = d.item_name
				child.vehicle = self.vehicle
				child.scheduled_date = s_list[i].strftime('%Y-%m-%d')
				# if d.serial_no:
				# 	child.serial_no = d.serial_no
				child.idx = count
				count = count + 1
				# child.sales_person = d.sales_person

		self.save()

	def validate(self):
		self.validate_dates()
		self.validate_maintenance_detail()
		self.validate_dates_with_periodicity()

	def create_vehicle(self):
		if self.vehicle_contract:
			vehicle = frappe.get_value('Assign and contribution contract', self.vehicle_contract, 'vehicle')
			if vehicle:
				self.set('vehicle', vehicle)

	def create_vehicle_contract(self):
		if self.vehicle:
			vehicle_contract = frappe.get_value('Assign and contribution contract', self.vehicle, 'name')
			if vehicle_contract:
				frappe.msgprint(_(vehicle_contract))
				self.set('vehicle_contract', vehicle_contract)

	def validate_maintenance_detail(self):
		if self.maintenance_check_button:
			if not self.get('maintenance_checks'):
				throw(_("Please enter Maintaince Details first"))

			for d in self.get('maintenance_checks'):
				if not d.item_code:
					throw(_("Please select item code"))
				elif not d.start_date or not d.end_date:
					throw(_("Please select Start Date and End Date for Item {0}".format(d.item_code)))
				elif not d.no_of_visits:
					throw(_("Please mention no of visits required"))
				# elif not d.sales_person:
				# 	throw(_("Please select Incharge Person's name"))

				if getdate(d.start_date) >= getdate(d.end_date):
					throw(_("Start date should be less than end date for Item {0}").format(d.item_code))

	def create_schedule_list(self, start_date, end_date, no_of_visit):
		schedule_list = []
		start_date_copy = start_date
		date_diff = (getdate(end_date) - getdate(start_date)).days
		add_by = date_diff / no_of_visit

		for visit in range(cint(no_of_visit)):
			if (getdate(start_date_copy) < getdate(end_date)):
				start_date_copy = add_days(start_date_copy, add_by)
				if len(schedule_list) < no_of_visit:
					# schedule_date = self.validate_schedule_date_for_holiday_list(getdate(start_date_copy),
					# 															 sales_person)
					# if schedule_date > getdate(end_date):
					schedule_date = getdate(end_date)
					schedule_list.append(schedule_date)

		return schedule_list

	def validate_dates_with_periodicity(self):
		for d in self.get("maintenance_checks"):
			if d.start_date and d.end_date and d.periodicity and d.periodicity!="Random":
				date_diff = (getdate(d.end_date) - getdate(d.start_date)).days + 1
				days_in_period = {
					"Weekly": 7,
					"Monthly": 30,
					"Quarterly": 90,
					"Half Yearly": 180,
					"Yearly": 365
				}

				if date_diff < days_in_period[d.periodicity]:
					throw(_("Row {0}: To set {1} periodicity, difference between from and to date \
						must be greater than or equal to {2}")
						  .format(d.idx, d.periodicity, days_in_period[d.periodicity]))

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
def make_invoice(amount, mode_of_payment, name=None):
	source = frappe.get_doc('Maintenance and repair', name)
	if source:
		if source.company_pay:
			invoice = frappe.new_doc('Purchase Invoice')
			default_customer = load_configuration('default_customer_for_invoice')
			if not source.driver_employee and not source.driver_customer:
				source.driver_customer = default_customer
				if not default_customer:
					frappe.throw(_('Please set default customer in the vehicle management Settings'))
			if source.driver_customer:
				invoice.driver_customer = source.driver_customer
			else:
				invoice.driver_employee = source.driver_employee
			item = source.repair_item
			if not item:
				frappe.throw(_('Please set default item in the vehicle management Settings'))
			sync_items(invoice, item, amount, source.cost_center, source.expense_head)
			invoice.start_date = getdate(source.start_date)
			invoice.end_date = getdate(source.end_date)
			invoice.vehicle = source.vehicle
			invoice.supplier = source.main_supplier
			invoice.maintenance_and_repair = source.name
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
	for d in items:
		invoice.append('items', dict(
			item_code = d.get('items'),
			item_name = d.get('items'),
			qty = d.get('quantity'),
			rate = d.get('rate'),
			amount =amount,
			cost_center = cost_center,
			expense_account = expense_account,
			conversion_factor = 1,
			uom= 'Nos'
		))
	return invoice.as_dict()

def load_configuration(name, default=None):
	val = frappe.db.get_single_value('Vehicle Management Setting', name)
	if val is None:
		val = default
	return val