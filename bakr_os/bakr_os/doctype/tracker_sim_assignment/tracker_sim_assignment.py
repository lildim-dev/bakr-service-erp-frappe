# Copyright (c) 2026, BAKR Service and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class TrackerSIMAssignment(Document):
    def validate(self):
        self.validate_active_assignment()

    def on_update(self):
        self.update_sim_card_status()

    def on_trash(self):
        self.release_sim_card()

    def validate_active_assignment(self):
        """
        Проверяет, что:
        1. SIM-карта имеет только одну активную привязку.
        2. Трекер имеет только одну активную SIM-карту.
        """

        if self.status != "Активна":
            return

        existing_sim_assignment = frappe.db.exists(
            "Tracker SIM Assignment",
            {
                "iccid": self.iccid,
                "status": "Активна",
                "name": ["!=", self.name],
            },
        )

        if existing_sim_assignment:
            frappe.throw(
                _(
                    "SIM-карта {0} уже имеет активную привязку {1}."
                ).format(
                    frappe.bold(self.iccid),
                    frappe.bold(existing_sim_assignment),
                )
            )

        existing_tracker_assignment = frappe.db.exists(
            "Tracker SIM Assignment",
            {
                "tracker_serial_no": self.tracker_serial_no,
                "status": "Активна",
                "name": ["!=", self.name],
            },
        )

        if existing_tracker_assignment:
            frappe.throw(
                _(
                    "Трекер {0} уже имеет активную SIM-карту в привязке {1}."
                ).format(
                    frappe.bold(self.tracker_serial_no),
                    frappe.bold(existing_tracker_assignment),
                )
            )

    def update_sim_card_status(self):
        """
        При активной привязке устанавливает SIM-карте статус «Установлена».
        При снятии привязки — «Свободна».
        """

        previous_doc = self.get_doc_before_save()

        # Если в существующей привязке заменили SIM-карту,
        # освобождаем предыдущую SIM.
        if (
            previous_doc
            and previous_doc.iccid
            and previous_doc.iccid != self.iccid
        ):
            self.set_sim_free_if_unused(previous_doc.iccid)

        if not self.iccid:
            return

        if self.status == "Активна":
            frappe.db.set_value(
                "Sim Card",
                self.iccid,
                "status",
                "Установлена",
                update_modified=True,
            )
        else:
            self.set_sim_free_if_unused(self.iccid)

    def release_sim_card(self):
        """
        Освобождает SIM-карту при удалении привязки.
        """

        if self.iccid:
            self.set_sim_free_if_unused(
                self.iccid,
                exclude_current=False,
            )

    def set_sim_free_if_unused(
        self,
        sim_card,
        exclude_current=True,
    ):
        """
        Делает SIM-карту свободной только тогда,
        когда у нее нет другой активной привязки.
        """

        filters = {
            "iccid": sim_card,
            "status": "Активна",
        }

        if exclude_current:
            filters["name"] = ["!=", self.name]

        active_assignment = frappe.db.exists(
            "Tracker SIM Assignment",
            filters,
        )

        if not active_assignment:
            frappe.db.set_value(
                "Sim Card",
                sim_card,
                "status",
                "Свободна",
                update_modified=True,
            )
