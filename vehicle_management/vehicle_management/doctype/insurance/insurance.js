// Copyright (c) 2019, stephen and contributors
// For license information, please see license.txt

frappe.ui.form.on('Insurance', {
	refresh: function(frm) {
        if(frm.doc.insurance_company){
            frm.add_custom_button(__("Create the insurance invoice"), function() {
                frm.events.make_invoice(frm)
            }).addClass("btn-primary")

        }

	},
	make_invoice: function (frm){

        return frappe.call({
            method: 'vehicle_management.vehicle_management.doctype.insurance.insurance.make_invoice',
            args: {
                amount: frm.doc.amount_paid,
                name: frm.doc.name
            },
            callback: (r) => {
               frappe.show_alert({message: __('Invoice created successfully'), indicator: 'green'})
            }
        });

	}
});
