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