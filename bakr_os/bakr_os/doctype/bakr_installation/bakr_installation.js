// Copyright (c) 2026, BAKR Service

frappe.ui.form.on("BAKR Installation", {
    refresh(frm) {
        if (!frm.is_new() && !frm.doc.subscription) {
            frm.add_custom_button(__("Активировать подписку"), () => {
                frappe.call({
                    doc: frm.doc,
                    method: "create_subscription",
                    freeze: true,
                    freeze_message: __("Создание подписки...")
                }).then(() => {
                    frm.reload_doc();
                });
            });
        }

        if (frm.doc.subscription) {
            frm.add_custom_button(__("Открыть подписку"), () => {
                frappe.set_route(
                    "Form",
                    "Subscription",
                    frm.doc.subscription
                );
            });
        }
    }
});

frappe.ui.form.on("BAKR Installation", {
    setup(frm) {
        frm.set_query("tracker_serial_no", () => {
            return {
                query: [
                    "bakr_os.bakr_os.doctype.bakr_installation",
                    "bakr_installation.get_available_trackers"
                ].join("."),
                filters: {
                    dealer_center: frm.doc.dealer_center,
                    current_installation: frm.doc.name
                }
            };
        });
    },

    dealer_center(frm) {
        frm.set_value("tracker_serial_no", null);
        frm.set_value("tracker_item", null);
    },

    tracker_serial_no(frm) {
        if (!frm.doc.tracker_serial_no) {
            frm.set_value("tracker_item", null);
            return;
        }

        frappe.db.get_value(
            "Serial No",
            frm.doc.tracker_serial_no,
            ["item_code", "customer", "status"]
        ).then((response) => {
            const serial = response.message;

            if (!serial) {
                return;
            }

            frm.set_value("tracker_item", serial.item_code);
        });
    }
});