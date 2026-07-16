import frappe


def prevent_invalid_submit(doc, method=None):
    if doc.doctype == "DocType":
        return

    if doc.meta.module == "BAKR OS" and not doc.meta.is_submittable:
        frappe.throw(
            f"Документ «{doc.doctype}» является справочником "
            "и не может быть подтверждён через Submit."
        )


def prevent_invalid_cancel(doc, method=None):
    if doc.doctype == "DocType":
        return

    if doc.meta.module == "BAKR OS" and not doc.meta.is_submittable:
        frappe.throw(
            f"Документ «{doc.doctype}» является справочником "
            "и не может быть отменён через Cancel."
        )
