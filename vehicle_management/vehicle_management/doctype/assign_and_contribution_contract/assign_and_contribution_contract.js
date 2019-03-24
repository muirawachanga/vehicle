// Copyright (c) 2019, stephen and contributors
// For license information, please see license.txt

frappe.ui.form.on('Assign and contribution contract', {
	refresh: function(frm) {
	    if(frm.doc.__islocal){
	        frm.trigger('calculate_date_amount')
	    }
	    if (frm.doc.status == 'Active' || frm.doc.status == 'Suspended') {
            frm.add_custom_button(__("Create Invoice"), function() {
                frm.events.make_invoice(frm)
            }).addClass("btn-primary");
        }
        if (frm.doc.status == 'Reassigned' || frm.doc.status == 'Terminated' || frm.doc.status == 'Rejected'){
            return frappe.call({
                method: 'set_available',
                doc: frm.doc
            })

        }

    },
    validate: function(frm){
        if (!frm.doc.total_amount){
            frappe.throw(__('The total amount cannot be less than zero, please change the table'))

        }
    },
    onload: function(frm){
        if (frm.doc.__islocal && frm.doc.contributions) {
            calculate_total_amount(frm);
        }
    },
    make_invoice: function(frm){
        frappe.prompt([
            {
                fieldname: 'mode_of_payment',
                label: __('Mode of Payment'),
                fieldtype: 'Link',
                reqd: 1,
                options: 'Mode of Payment',
                'default': frm.mode_of_payment || ''
            }
        ], (data) => {
            // cache this for next entry
            frm.mode_of_payment = data.mode_of_payment
        return frappe.call({
            method: 'vehicle_management.vehicle_management.doctype.assign_and_contribution_contract.assign_and_contribution_contract.make_invoice',
            args: {
                vehicle: frm.doc.vehicle,
                amount: frm.doc.total_amount,
                mode_of_payment: data.mode_of_payment,
                name: frm.doc.name,
                customer: frm.doc.customer

            },
            callback: (r) => {
               frappe.show_alert({message: __('Invoice created successfully'), indicator: 'green'})
            }
        });

       },
       __("Select Mode of payment"));
    },
    calculate_date_amount: function(frm){
        if(frm.doc.start_date && frm.doc.end_date){
            var start_date = moment(frm.doc.start_date)
            var end_date = moment(frm.doc.end_date)
            var diff = end_date.diff(start_date, 'days') + 1
            if(frm.doc.amount_per_day){
                var total_amount = diff * frm.doc.amount_per_day
                var msg = __('The number of days to be billed are: ') + diff
                frappe.msgprint(msg)
                frm.set_value('total_amount_expected', total_amount)
                frm.set_value('contributions', [])
                frm.set_value('total_amount', total_amount)
            }
        }
    },
    end_date: function(frm){
        frm.trigger('calculate_date_amount')
        frm.set_value('termination_date', frm.doc.end_date)
        if (frm.doc.vehicle_status == 'Self Drive'){

        }
    },
    total_amount_expected: function(frm){
        if (frm.doc.total_amount_expected != frm.doc.total_amount){
            frm.set_value('total_amount', frm.doc.total_amount_expected)
            refresh_field('total_amount')
        }

    },
    amount_per_day: function(frm){
        frm.trigger('calculate_date_amount')

    },
    tabulate: function(frm){
        if(!frm.doc.end_date || !frm.doc.amount_per_day){
            frappe.throw(__('You must set the start and end date and amount for the system to tabulate'))

        }
        if (frm.doc.start_date > frm.doc.end_date) {
            frappe.msgprint(__('The start date is greater than period end. Cannot load.'));
            return;
        }
        return frappe.call({
            method: "tabulate_data",
            doc: frm.doc,
            callback: function(r) {
                frm.toggle_enable(['total_amount_expected'], 0)
                frm.set_value('total_amount_expected', 0.00)
                refresh_field('total_amount_expected')
                refresh_field('contributions')
                calculate_total_amount(frm)
            }
        })
    }

    });
    frappe.ui.form.on("Contribution", {
    	contributions_remove: function(frm) {
        	calculate_total_amount(frm);
        },
        amount_deposited: function(frm){
            calculate_total_amount(frm);
        }

    });
cur_frm.fields_dict['vehicle'].get_query = function (doc, cdt, cdn) {
  return {
    filters: {
      'vehicle_status': 'Available'
    }
  }
}

//     used to calculate the total in the contribution table

var calculate_total_amount = function(frm) {
    var tl = frm.doc.contributions || [];
    var total_amount = 0;
    for(var i=0; i<tl.length; i++) {
        if (tl[i].amount_deposited) {
            total_amount += tl[i].amount_deposited;
        }
    }
    frm.set_value("total_amount", total_amount);
    refresh_field('total_amount')
}
