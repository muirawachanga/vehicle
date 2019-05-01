// Copyright (c) 2019, stephen and contributors
// For license information, please see license.txt

frappe.ui.form.on('Maintenance and repair', {
	refresh: function(frm) {
	    if(frm.doc.company_pay){
            frm.add_custom_button(__("Create the repair invoice"), function() {
                frm.events.make_invoice(frm)
            }).addClass("btn-primary")

            frm.add_custom_button(__('Open Invoice'), function() {
                frappe.route_options = {
                    "maintenance_and_repair": frm.doc.name
                };
                frappe.set_route("List", "Sales Invoice");
            }, "fa fa-table");

        }
	},
	validate: function(frm){
	    if(frm.doc.company_pay){
	        if(frm.doc.amount_paid < 0 || frm.doc.amount_paid > frm.doc.repair_cost){
	             frappe.throw(__('Please adjust the costing accordingly please, amount paid by company is greater or 0'))
	        }
	        if(!frm.doc.expense_head || !frm.doc.cost_center){
	            frappe.throw(__('Please you have to set the accounting field'))

	        }

	    }
	    frappe.validated = true
	    frm.toggle_enable(['vehicle_contract', 'repair_cost'], 0)

	},
	repair_cost: function(frm){
	    if(frm.doc.company_pay){
	        frm.set_value('amount_paid', frm.doc.repair_cost)
	        refresh_field('amount_paid')
	    }

	},
	vehicle_contract: function (frm) {
	    if(frm.doc.vehicle_contract){
	        return frappe.call({
	            method: 'create_vehicle',
	            doc: frm.doc,
	            callback: function(r){
	                frm.refresh()
	            }
	        })
	    }

	},

	company_pay: function(frm){
	    frm.set_value('amount_paid', frm.doc.repair_cost)
	    refresh_field('amount_paid')

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
            method: 'vehicle_management.vehicle_management.doctype.maintenance_and_repair.maintenance_and_repair.make_invoice',
            args: {
                amount: frm.doc.amount_paid,
                mode_of_payment: data.mode_of_payment,
                name: frm.doc.name
            },
            callback: (r) => {
               frappe.show_alert({message: __('Invoice created successfully'), indicator: 'green'})
            }
        });

       },
       __("Select Mode of payment"));
    }
});

    frappe.ui.form.on("Repair items", {
    	repair_item_remove: function(frm) {
        	calculate_total_amount(frm)
        },
        amount: function(frm){
            calculate_total_amount(frm)
        },
        rate: function(frm, cdt, cdn){
            amount_from_rate(frm, cdt, cdn)
        },
        quantity: function(frm, cdt, cdn){
            amount_from_rate(frm, cdt, cdn)
        }

    })

    frappe.ui.form.on('Maintenance checks', {

        start_date: function(frm, cdt, cdn) {
            set_no_of_visits(frm, cdt, cdn)
        },

        end_date: function(frm, cdt, cdn) {
            set_no_of_visits(frm, cdt, cdn)
        },

        periodicity: function(frm, cdt, cdn) {
            set_no_of_visits(frm, cdt, cdn)
        }
    })

    var calculate_total_amount = function(frm) {
        var tl = frm.doc.repair_item || [];
        var total_amount = 0;
        for(var i=0; i<tl.length; i++) {
            if (tl[i].amount) {
                total_amount += tl[i].amount
            }
        }
        frm.set_value("repair_cost", total_amount)
        refresh_field('repair_cost')
    }

    var amount_from_rate = function(frm, cdt, cdn){
       let child =  locals[cdt][cdn]
       if(child.rate){
           amount = flt(child.rate * child.quantity);
           frappe.model.set_value(cdt, cdn, 'amount', amount)

       }
    }
    var set_no_of_visits = function(frm, cdt, cdn) {
        var item = frappe.get_doc(cdt, cdn);
        console.log('i was called too')

        if (item.start_date && item.end_date && item.periodicity) {
            if(item.start_date > item.end_date) {
                frappe.msgprint(__("Row {0}:Start Date must be before End Date", [item.idx]));
                return;
            }

            var date_diff = frappe.datetime.get_diff(item.end_date, item.start_date) + 1;

            var days_in_period = {
                "Weekly": 7,
                "Monthly": 30,
                "Quarterly": 91,
                "Half Yearly": 182,
                "Yearly": 365
            }

            var no_of_visits = cint(date_diff / days_in_period[item.periodicity]);
            frappe.model.set_value(item.doctype, item.name, "no_of_visits", no_of_visits);
        }
    }


cur_frm.cscript.generate_schedule = function(doc, cdt, cdn) {
	if (!doc.__islocal) {
		return $c('runserverobj', {'method':'generate_schedule', 'docs':doc},
			function(r, rt) {
				refresh_field('schedules');
			});
	} else {
		frappe.msgprint(__("Please save the document before generating maintenance schedule"));
	}
}
cur_frm.fields_dict['vehicle_contract'].get_query = function (doc, cdt, cdn) {
  return {
    filters: {
      'vehicle': doc.vehicle
    }
  }
}