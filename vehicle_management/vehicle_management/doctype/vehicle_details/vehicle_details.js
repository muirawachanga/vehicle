// Copyright (c) 2019, stephen and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vehicle Details', {
	refresh: function(frm){

	},
	parent_cost_center: function(frm){
		return frappe.call({
			method: "create_cost_center",
			doc: frm.doc,
			callback: function(r, rt) {
				frm.refresh();
			}
		});
	}
})