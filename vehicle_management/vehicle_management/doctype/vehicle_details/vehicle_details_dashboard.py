from frappe import _


def get_data():
    return {
        "heatmap": True,
        "heatmap_message": _(
            "This is based on transactions against this vehicle. See timeline below for details"
        ),
        "fieldname": "vehicle",
        "transactions": [
            {
                "label": _("Driver contract"),
                "items": ["Assign and contribution contract"],
            },
            {
                "label": _("Maintenance"),
                "items": ["Maintenance and repair", "Maintenance Visits"],
            },
            {
                "label": _("Owner contract and remittance"),
                "items": ["Vehicle Owner Contract", "Vehicle Remittance"],
            },
            {"label": _("Accounting"), "items": ["Sales Invoice"]},
        ],
    }
