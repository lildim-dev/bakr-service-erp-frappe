# Copyright (c) 2026, BAKR Service and contributors
# For license information, please see license.txt

from datetime import timedelta

import frappe
from dateutil.relativedelta import relativedelta
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate


class BAKRInstallation(Document):

    def validate(self):
        """Проверки документа перед сохранением."""

        self._validate_tracker_not_installed()
        self._validate_tracker_customer()

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
        subscription.start_date = getdate(
            self.subscription_start_date
        )
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
            _("Подписка {0} успешно создана.").format(
                subscription.name
            ),
            alert=True,
        )

    def _validate_tracker_not_installed(self) -> None:
        """Запретить повторную установку одного трекера."""

        if not self.tracker_serial_no:
            return

        filters = {
            "tracker_serial_no": self.tracker_serial_no,
            "docstatus": ["!=", 2],
            "status": [
                "not in",
                ["Демонтирована", "Закрыта"],
            ],
        }

        if not self.is_new():
            filters["name"] = ["!=", self.name]

        existing_installation = frappe.db.get_value(
            "BAKR Installation",
            filters,
            "name",
        )

        if existing_installation:
            frappe.throw(
                _(
                    "Трекер {0} уже установлен по документу {1}."
                ).format(
                    frappe.bold(self.tracker_serial_no),
                    frappe.get_desk_link(
                        "BAKR Installation",
                        existing_installation,
                    ),
                ),
                title=_("Трекер уже установлен"),
            )

    def _validate_tracker_customer(self) -> None:
        """
        Проверить, что трекер продан юридическому лицу
        выбранного дилерского центра.
        """

        if not self.tracker_serial_no or not self.dealer_center:
            return

        dealer_customer = frappe.db.get_value(
            "Dealer Center",
            self.dealer_center,
            "customer",
        )

        if not dealer_customer:
            frappe.throw(
                _(
                    "У дилерского центра {0} не заполнено "
                    "поле «Юридическое наименование»."
                ).format(
                    frappe.bold(self.dealer_center)
                ),
                title=_("Не указано юридическое лицо"),
            )

        tracker_data = frappe.db.get_value(
            "Serial No",
            self.tracker_serial_no,
            [
                "customer",
                "item_code",
                "status",
            ],
            as_dict=True,
        )

        if not tracker_data:
            frappe.throw(
                _("Серийный номер {0} не найден.").format(
                    frappe.bold(self.tracker_serial_no)
                )
            )

        if not tracker_data.customer:
            frappe.throw(
                _(
                    "Трекер {0} не числится проданным покупателю. "
                    "В карточке Serial No поле Customer не заполнено."
                ).format(
                    frappe.bold(self.tracker_serial_no)
                ),
                title=_("Трекер не продан"),
            )

        if tracker_data.customer != dealer_customer:
            frappe.throw(
                _(
                    "Трекер {0} продан покупателю {1}, "
                    "но юридическое лицо дилерского центра — {2}."
                ).format(
                    frappe.bold(self.tracker_serial_no),
                    frappe.bold(tracker_data.customer),
                    frappe.bold(dealer_customer),
                ),
                title=_("Покупатель трекера не совпадает"),
            )

        if tracker_data.status != "Delivered":
            frappe.throw(
                _(
                    "Трекер {0} имеет статус Serial No «{1}». "
                    "Для установки трекер должен иметь "
                    "статус «Delivered»."
                ).format(
                    frappe.bold(self.tracker_serial_no),
                    frappe.bold(
                        tracker_data.status or "не указан"
                    ),
                ),
                title=_("Трекер не отгружен"),
            )

        if (
            self.tracker_item
            and self.tracker_item != tracker_data.item_code
        ):
            frappe.throw(
                _(
                    "Выбранная модель трекера {0} "
                    "не соответствует товару серийного номера "
                    "{1}: {2}."
                ).format(
                    frappe.bold(self.tracker_item),
                    frappe.bold(self.tracker_serial_no),
                    frappe.bold(tracker_data.item_code),
                ),
                title=_("Модель трекера не совпадает"),
            )

        self.tracker_item = tracker_data.item_code

    def _validate_subscription(self):
        """Проверить обязательные данные подписки."""

        if not self.billing_customer:
            frappe.throw(_("Укажите плательщика."))

        if not self.subscription_plan:
            frappe.throw(_("Укажите план подписки."))

        if not self.subscription_start_date:
            frappe.throw(_("Укажите дату начала подписки."))

    def _calculate_subscription_dates(self, plan):
        """Рассчитать срок и дату окончания подписки."""

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
                _(
                    "Неподдерживаемый Billing Interval: {0}"
                ).format(interval)
            )

        return duration, end


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_available_trackers(
    doctype,
    txt,
    searchfield,
    start,
    page_len,
    filters,
):
    """
    Вернуть трекеры, доступные для выбранного
    дилерского центра.
    """

    filters = filters or {}

    dealer_center = filters.get("dealer_center")
    current_installation = filters.get(
        "current_installation"
    )

    if not dealer_center:
        return []

    dealer_customer = frappe.db.get_value(
        "Dealer Center",
        dealer_center,
        "customer",
    )

    if not dealer_customer:
        return []

    serial_no = frappe.qb.DocType("Serial No")
    installation = frappe.qb.DocType(
        "BAKR Installation"
    )

    installed_query = (
        frappe.qb.from_(installation)
        .select(installation.tracker_serial_no)
        .where(installation.docstatus != 2)
        .where(
            installation.status.notin(
                ["Демонтирована", "Закрыта"]
            )
        )
        .where(
            installation.tracker_serial_no.isnotnull()
        )
    )

    if current_installation:
        installed_query = installed_query.where(
            installation.name != current_installation
        )

    search_text = f"%{txt}%"

    query = (
        frappe.qb.from_(serial_no)
        .select(
            serial_no.name,
            serial_no.item_code,
            serial_no.item_name,
        )
        .where(serial_no.customer == dealer_customer)
        .where(serial_no.status == "Delivered")
        .where(
            serial_no.name.notin(installed_query)
        )
        .where(
            (serial_no.name.like(search_text))
            | (serial_no.item_code.like(search_text))
            | (serial_no.item_name.like(search_text))
        )
        .orderby(
            serial_no.modified,
            order=frappe.qb.desc,
        )
        .limit(page_len)
        .offset(start)
    )

    return query.run()