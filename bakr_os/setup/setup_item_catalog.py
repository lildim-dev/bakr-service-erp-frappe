import frappe
from frappe import _


COMPANY = "Bakr-Сервис"

ITEM_GROUPS = [
    {
        "item_group_name": "BAKR Products",
        "parent_item_group": "All Item Groups",
        "is_group": 1,
    },
    {
        "item_group_name": "GPS Equipment",
        "parent_item_group": "BAKR Products",
        "is_group": 1,
    },
    {
        "item_group_name": "GPS Trackers",
        "parent_item_group": "GPS Equipment",
        "is_group": 0,
        "income_account": "GPS Tracker Sales",
        "expense_account": "Cost of Goods Sold",
        "default_warehouse": "Основной склад",
    },
    {
        "item_group_name": "Video Telematics",
        "parent_item_group": "GPS Equipment",
        "is_group": 1,
    },
    {
        "item_group_name": "Dash Cameras",
        "parent_item_group": "Video Telematics",
        "is_group": 0,
        "income_account": "Video Equipment Sales",
        "expense_account": "Cost of Goods Sold",
        "default_warehouse": "Основной склад",
    },
    {
        "item_group_name": "ADAS DMS Equipment",
        "parent_item_group": "Video Telematics",
        "is_group": 0,
        "income_account": "Video Equipment Sales",
        "expense_account": "Cost of Goods Sold",
        "default_warehouse": "Основной склад",
    },
    {
        "item_group_name": "Accessories",
        "parent_item_group": "GPS Equipment",
        "is_group": 0,
        "income_account": "Accessories Sales",
        "expense_account": "Cost of Goods Sold",
        "default_warehouse": "Основной склад",
    },
    {
        "item_group_name": "Spare Parts",
        "parent_item_group": "GPS Equipment",
        "is_group": 0,
        "income_account": "Accessories Sales",
        "expense_account": "Cost of Goods Sold",
        "default_warehouse": "Основной склад",
    },
    {
        "item_group_name": "SIM Cards",
        "parent_item_group": "BAKR Products",
        "is_group": 0,
        "income_account": "SIM Card Sales",
        "expense_account": "Cost of Goods Sold",
        "default_warehouse": "Основной склад",
    },
    {
        "item_group_name": "BAKR Services",
        "parent_item_group": "All Item Groups",
        "is_group": 1,
    },
    {
        "item_group_name": "Installation Services",
        "parent_item_group": "BAKR Services",
        "is_group": 0,
        "income_account": "Installation Services",
        "expense_account": "Administrative Expenses",
    },
    {
        "item_group_name": "Monitoring Services",
        "parent_item_group": "BAKR Services",
        "is_group": 0,
        "income_account": "Monitoring Subscription",
        "expense_account": "Administrative Expenses",
    },
    {
        "item_group_name": "SIM Services",
        "parent_item_group": "BAKR Services",
        "is_group": 0,
        "income_account": "SIM Subscription",
        "expense_account": "Administrative Expenses",
    },
    {
        "item_group_name": "Technical Support Services",
        "parent_item_group": "BAKR Services",
        "is_group": 0,
        "income_account": "Technical Support Services",
        "expense_account": "Administrative Expenses",
    },
    {
        "item_group_name": "Equipment Removal Services",
        "parent_item_group": "BAKR Services",
        "is_group": 0,
        "income_account": "Equipment Removal Services",
        "expense_account": "Administrative Expenses",
    },
]


SERVICE_ITEMS = [
    {
        "item_code": "SRV-INSTALLATION",
        "item_name": "Установка GPS-оборудования",
        "description": "Услуга установки и первичной настройки GPS-оборудования.",
        "item_group": "Installation Services",
    },
    {
        "item_code": "SRV-MONITORING",
        "item_name": "Абонентская плата за GPS-мониторинг",
        "description": "Периодическая услуга GPS-мониторинга транспорта.",
        "item_group": "Monitoring Services",
    },
    {
        "item_code": "SRV-SIM-SUBSCRIPTION",
        "item_name": "Абонентская плата за SIM-карту",
        "description": "Периодическая плата за мобильную передачу данных SIM-карты.",
        "item_group": "SIM Services",
    },
    {
        "item_code": "SRV-TECH-SUPPORT",
        "item_name": "Техническая поддержка",
        "description": "Услуги технической поддержки и обслуживания оборудования.",
        "item_group": "Technical Support Services",
    },
    {
        "item_code": "SRV-REMOVAL",
        "item_name": "Демонтаж оборудования",
        "description": "Услуга демонтажа или переноса установленного оборудования.",
        "item_group": "Equipment Removal Services",
    },
]


def company_abbr():
    abbr = frappe.db.get_value("Company", COMPANY, "abbr")

    if not abbr:
        frappe.throw(
            _("Не найдена компания или ее аббревиатура: {0}").format(COMPANY)
        )

    return abbr


def full_account_name(account_name):
    return f"{account_name} - {company_abbr()}"


def resolve_account(account_name):
    if not account_name:
        return None

    account = full_account_name(account_name)

    if not frappe.db.exists("Account", account):
        frappe.throw(
            _("Не найден счет: {0}").format(account)
        )

    if frappe.db.get_value("Account", account, "is_group"):
        frappe.throw(
            _("Счет {0} является группой и не может использоваться в проводках").format(
                account
            )
        )

    return account


def resolve_warehouse(warehouse_name):
    if not warehouse_name:
        return None

    abbr = company_abbr()
    candidates = [
        warehouse_name,
        f"{warehouse_name} - {abbr}",
    ]

    for candidate in candidates:
        if frappe.db.exists("Warehouse", candidate):
            warehouse = frappe.get_doc("Warehouse", candidate)

            if warehouse.company != COMPANY:
                frappe.throw(
                    _("Склад {0} относится к другой компании").format(candidate)
                )

            if warehouse.is_group:
                frappe.throw(
                    _("Склад {0} является группой").format(candidate)
                )

            if warehouse.disabled:
                frappe.throw(
                    _("Склад {0} отключен").format(candidate)
                )

            return candidate

    frappe.throw(
        _("Не найден склад: {0}").format(warehouse_name)
    )


def create_or_update_item_group(config):
    name = config["item_group_name"]
    parent = config["parent_item_group"]

    if not frappe.db.exists("Item Group", parent):
        frappe.throw(
            _("Не найдена родительская группа товаров: {0}").format(parent)
        )

    if frappe.db.exists("Item Group", name):
        doc = frappe.get_doc("Item Group", name)
        action = "UPDATE"
    else:
        doc = frappe.new_doc("Item Group")
        doc.item_group_name = name
        action = "CREATE"

    doc.parent_item_group = parent
    doc.is_group = config["is_group"]

    if hasattr(doc, "show_in_website"):
        doc.show_in_website = 0

    if config.get("income_account") or config.get("expense_account"):
        set_item_group_defaults(doc, config)

    doc.flags.ignore_permissions = True
    doc.save()

    print(f"{action}: Item Group {doc.name}")


def set_item_group_defaults(doc, config):
    meta = frappe.get_meta("Item Group")

    if not meta.has_field("item_group_defaults"):
        frappe.throw(
            _(
                "В текущей версии ERPNext в Item Group отсутствует "
                "таблица item_group_defaults"
            )
        )

    income_account = resolve_account(config.get("income_account"))
    expense_account = resolve_account(config.get("expense_account"))
    default_warehouse = resolve_warehouse(config.get("default_warehouse"))

    existing = None

    for row in doc.get("item_group_defaults") or []:
        if row.company == COMPANY:
            existing = row
            break

    if not existing:
        existing = doc.append("item_group_defaults", {})
        existing.company = COMPANY

    existing.income_account = income_account
    existing.expense_account = expense_account
    existing.default_warehouse = default_warehouse


def create_or_update_service_item(config):
    item_code = config["item_code"]

    if frappe.db.exists("Item", item_code):
        doc = frappe.get_doc("Item", item_code)
        action = "UPDATE"
    else:
        doc = frappe.new_doc("Item")
        doc.item_code = item_code
        action = "CREATE"

    doc.item_name = config["item_name"]
    doc.description = config["description"]
    doc.item_group = config["item_group"]
    doc.stock_uom = "Nos"
    doc.is_stock_item = 0
    doc.disabled = 0

    if hasattr(doc, "is_sales_item"):
        doc.is_sales_item = 1

    if hasattr(doc, "is_purchase_item"):
        doc.is_purchase_item = 0

    set_item_defaults_from_group(doc)

    doc.flags.ignore_permissions = True
    doc.save()

    print(f"{action}: Item {doc.name}")


def set_item_defaults_from_group(item_doc):
    group = frappe.get_doc("Item Group", item_doc.item_group)

    group_default = None

    for row in group.get("item_group_defaults") or []:
        if row.company == COMPANY:
            group_default = row
            break

    if not group_default:
        frappe.throw(
            _(
                "Для группы {0} не настроены Item Defaults компании {1}"
            ).format(item_doc.item_group, COMPANY)
        )

    existing = None

    for row in item_doc.get("item_defaults") or []:
        if row.company == COMPANY:
            existing = row
            break

    if not existing:
        existing = item_doc.append("item_defaults", {})
        existing.company = COMPANY

    existing.income_account = group_default.income_account
    existing.expense_account = group_default.expense_account

    if group_default.default_warehouse:
        existing.default_warehouse = group_default.default_warehouse


def ensure_import_duty_expense():
    account_name = "Import Duty Expense"
    full_name = full_account_name(account_name)
    parent = full_account_name("Import Expenses")

    if frappe.db.exists("Account", full_name):
        print(f"SKIP: Account {full_name}")
        return

    if not frappe.db.exists("Account", parent):
        frappe.throw(
            _("Не найдена группа расходов по импорту: {0}").format(parent)
        )

    doc = frappe.get_doc(
        {
            "doctype": "Account",
            "account_name": account_name,
            "parent_account": parent,
            "company": COMPANY,
            "root_type": "Expense",
            "account_type": "Chargeable",
            "is_group": 0,
            "account_currency": frappe.db.get_value(
                "Company",
                COMPANY,
                "default_currency",
            ),
        }
    )

    doc.insert(ignore_permissions=True)

    print(f"CREATE: Account {doc.name}")


def validate_configuration():
    if not frappe.db.exists("Company", COMPANY):
        frappe.throw(_("Компания не найдена: {0}").format(COMPANY))

    for account_name in {
        row.get("income_account")
        for row in ITEM_GROUPS
        if row.get("income_account")
    }:
        resolve_account(account_name)

    for account_name in {
        row.get("expense_account")
        for row in ITEM_GROUPS
        if row.get("expense_account")
    }:
        resolve_account(account_name)

    for row in ITEM_GROUPS:
        if row.get("default_warehouse"):
            resolve_warehouse(row["default_warehouse"])


def execute():
    try:
        ensure_import_duty_expense()
        validate_configuration()

        for config in ITEM_GROUPS:
            create_or_update_item_group(config)

        for config in SERVICE_ITEMS:
            create_or_update_service_item(config)

        frappe.db.commit()

        print("\nГотово.")
        print(f"Групп товаров обработано: {len(ITEM_GROUPS)}")
        print(f"Сервисных позиций обработано: {len(SERVICE_ITEMS)}")

    except Exception:
        frappe.db.rollback()
        print("\nОшибка. Все изменения текущего запуска отменены.")
        raise
