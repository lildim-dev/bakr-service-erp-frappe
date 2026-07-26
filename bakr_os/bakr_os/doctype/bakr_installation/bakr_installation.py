# Copyright (c) 2026, BAKR Service and contributors
# For license information, please see license.txt

from datetime import timedelta

import frappe
from dateutil.relativedelta import relativedelta
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate


class BAKRInstallation(Document):

    @frappe.whitelist()
    def create_subscription(self):
        """Создать стандартную ERPNext Subscription."""

        self._validate_subscription()

        if self.subscription:
            frappe.throw(_("Подписка уже создана."))

        plan = frappe.get_doc(
            "Subscription Plan",
            self.subscription_plan,
        )

        duration, end_date = self._calculate_subscription_dates(plan)

        company = (
            frappe.defaults.get_user_default("Company")
            or frappe.db.get_single_value(
                "Global Defaults",
                "default_company",
            )
        )

        if not company:
            frappe.throw(_("Не настроена компания по умолчанию."))

        subscription = frappe.new_doc("Subscription")
        subscription.party_type = "Customer"
        subscription.party = self.billing_customer
        subscription.company = company
        subscription.start_date = getdate(self.subscription_start_date)
        subscription.end_date = end_date

        subscription.append(
            "plans",
            {
                "plan": self.subscription_plan,
                "qty": 1,
            },
        )

        subscription.insert()

        frappe.db.set_value(
            "BAKR Installation",
            self.name,
            {
                "subscription": subscription.name,
                "subscription_duration": duration,
                "subscription_end_date": end_date,
            },
        )

        self.subscription = subscription.name
        self.subscription_duration = duration
        self.subscription_end_date = end_date

        frappe.msgprint(
            _("Подписка {0} успешно создана.").format(subscription.name),
            alert=True,
        )

    def _validate_subscription(self):
        """Проверка обязательных данных."""

        if not self.billing_customer:
            frappe.throw(_("Укажите плательщика."))

        if not self.subscription_plan:
            frappe.throw(_("Укажите план подписки."))

        if not self.subscription_start_date:
            frappe.throw(_("Укажите дату начала подписки."))

    def _calculate_subscription_dates(self, plan):
        """Рассчитать срок и дату окончания."""

        start = getdate(self.subscription_start_date)

        interval = plan.billing_interval
        count = plan.billing_interval_count or 1

        if interval == "Day":
            end = start + timedelta(days=count)
            duration = count

        elif interval == "Week":
            end = start + relativedelta(weeks=count)
            duration = count * 7

        elif interval == "Month":
            end = start + relativedelta(months=count)
            duration = count

        elif interval == "Year":
            end = start + relativedelta(years=count)
            duration = count * 12

        else:
            frappe.throw(
                _("Неподдерживаемый Billing Interval: {0}").format(interval)
            )

        return duration, end