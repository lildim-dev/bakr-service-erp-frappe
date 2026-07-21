import frappe
from frappe import _


COMPANY = "Bakr-Сервис"
CURRENCY = "KGS"


ACCOUNTS = [
    # Активы: налоговые активы
    {
        "account_name": "Input VAT",
        "account_name_ru": "Входящий НДС",
        "parent_account": "Tax Assets - BС",
        "root_type": "Asset",
        "account_type": "Tax",
        "is_group": 0,
        "account_currency": CURRENCY,
        "purpose": "Учет входящего и импортного НДС, принимаемого к зачету.",
    },

    # Расходы по импорту
    {
        "account_name": "Import Expenses",
        "account_name_ru": "Расходы по импорту",
        "parent_account": "Direct Expenses - BС",
        "root_type": "Expense",
        "account_type": "",
        "is_group": 1,
        "account_currency": CURRENCY,
        "purpose": "Группа расходов, непосредственно связанных с импортом оборудования.",
    },
    {
        "account_name": "Import Duty",
        "account_name_ru": "Таможенная пошлина",
        "parent_account": "Import Expenses - BС",
        "root_type": "Expense",
        "account_type": "Chargeable",
        "is_group": 0,
        "account_currency": CURRENCY,
        "purpose": "Таможенная пошлина, включаемая в стоимость импортного товара.",
    },
    {
        "account_name": "Customs Clearance",
        "account_name_ru": "Таможенное оформление",
        "parent_account": "Import Expenses - BС",
        "root_type": "Expense",
        "account_type": "Chargeable",
        "is_group": 0,
        "account_currency": CURRENCY,
        "purpose": "Расходы на таможенное оформление импортного груза.",
    },
    {
        "account_name": "Customs Broker Services",
        "account_name_ru": "Услуги таможенного брокера",
        "parent_account": "Import Expenses - BС",
        "root_type": "Expense",
        "account_type": "Chargeable",
        "is_group": 0,
        "account_currency": CURRENCY,
        "purpose": "Вознаграждение таможенного брокера.",
    },
    {
        "account_name": "Import Certification",
        "account_name_ru": "Сертификация импортного оборудования",
        "parent_account": "Import Expenses - BС",
        "root_type": "Expense",
        "account_type": "Chargeable",
        "is_group": 0,
        "account_currency": CURRENCY,
        "purpose": "Расходы на сертификацию и разрешительные документы.",
    },
    {
        "account_name": "Cargo Insurance",
        "account_name_ru": "Страхование груза",
        "parent_account": "Import Expenses - BС",
        "root_type": "Expense",
        "account_type": "Chargeable",
        "is_group": 0,
        "account_currency": CURRENCY,
        "purpose": "Страхование импортного груза в пути.",
    },
    {
        "account_name": "Import Handling Charges",
        "account_name_ru": "Погрузочно-разгрузочные расходы",
        "parent_account": "Import Expenses - BС",
        "root_type": "Expense",
        "account_type": "Chargeable",
        "is_group": 0,
        "account_currency": CURRENCY,
        "purpose": "Погрузка, разгрузка и обработка импортного груза.",
    },
    {
        "account_name": "Other Import Expenses",
        "account_name_ru": "Прочие расходы по импорту",
        "parent_account": "Import Expenses - BС",
        "root_type": "Expense",
        "account_type": "Chargeable",
        "is_group": 0,
        "account_currency": CURRENCY,
        "purpose": "Прочие расходы, непосредственно связанные с импортом.",
    },

    # Доходы от продажи оборудования
    {
        "account_name": "Equipment Sales",
        "account_name_ru": "Продажа оборудования",
        "parent_account": "Direct Income - BС",
        "root_type": "Income",
        "account_type": "",
        "is_group": 1,
        "account_currency": CURRENCY,
        "purpose": "Группа доходов от реализации оборудования.",
    },
    {
        "account_name": "GPS Tracker Sales",
        "account_name_ru": "Продажа GPS-трекеров",
        "parent_account": "Equipment Sales - BС",
        "root_type": "Income",
        "account_type": "Income Account",
        "is_group": 0,
        "account_currency": CURRENCY,
        "purpose": "Доход от продажи GPS-трекеров.",
    },
    {
        "account_name": "Video Equipment Sales",
        "account_name_ru": "Продажа видеооборудования",
        "parent_account": "Equipment Sales - BС",
        "root_type": "Income",
        "account_type": "Income Account",
        "is_group": 0,
        "account_currency": CURRENCY,
        "purpose": "Доход от продажи видеорегистраторов и видеотелематики.",
    },
    {
        "account_name": "SIM Card Sales",
        "account_name_ru": "Продажа SIM-карт",
        "parent_account": "Equipment Sales - BС",
        "root_type": "Income",
        "account_type": "Income Account",
        "is_group": 0,
        "account_currency": CURRENCY,
        "purpose": "Доход от продажи SIM-карт.",
    },
    {
        "account_name": "Accessories Sales",
        "account_name_ru": "Продажа аксессуаров",
        "parent_account": "Equipment Sales - BС",
        "root_type": "Income",
        "account_type": "Income Account",
        "is_group": 0,
        "account_currency": CURRENCY,
        "purpose": "Доход от продажи кабелей, датчиков и аксессуаров.",
    },

    # Доходы от услуг
    {
        "account_name": "Telematics Services",
        "account_name_ru": "Телематические услуги",
        "parent_account": "Direct Income - BС",
        "root_type": "Income",
        "account_type": "",
        "is_group": 1,
        "account_currency": CURRENCY,
        "purpose": "Группа доходов от установки, мониторинга и обслуживания.",
    },
    {
        "account_name": "Installation Services",
        "account_name_ru": "Услуги установки оборудования",
        "parent_account": "Telematics Services - BС",
        "root_type": "Income",
        "account_type": "Income Account",
        "is_group": 0,
        "account_currency": CURRENCY,
        "purpose": "Доход от установки GPS- и видеооборудования.",
    },
    {
        "account_name": "Monitoring Subscription",
        "account_name_ru": "Абонентская плата за мониторинг",
        "parent_account": "Telematics Services - BС",
        "root_type": "Income",
        "account_type": "Income Account",
        "is_group": 0,
        "account_currency": CURRENCY,
        "purpose": "Регулярный доход от услуг GPS-мониторинга.",
    },
    {
        "account_name": "SIM Subscription",
        "account_name_ru": "Абонентская плата за SIM-карты",
        "parent_account": "Telematics Services - BС",
        "root_type": "Income",
        "account_type": "Income Account",
        "is_group": 0,
        "account_currency": CURRENCY,
        "purpose": "Доход от предоставления SIM-связи клиентам.",
    },
    {
        "account_name": "Technical Support Services",
        "account_name_ru": "Услуги технической поддержки",
        "parent_account": "Telematics Services - BС",
        "root_type": "Income",
        "account_type": "Income Account",
        "is_group": 0,
        "account_currency": CURRENCY,
        "purpose": "Доход от технической поддержки и обслуживания.",
    },
    {
        "account_name": "Equipment Removal Services",
        "account_name_ru": "Услуги демонтажа оборудования",
        "parent_account": "Telematics Services - BС",
        "root_type": "Income",
        "account_type": "Income Account",
        "is_group": 0,
        "account_currency": CURRENCY,
        "purpose": "Доход от демонтажа и переноса оборудования.",
    },
]


def get_company_abbr():
    return frappe.db.get_value("Company", COMPANY, "abbr")


def get_full_account_name(account_name):
    abbr = get_company_abbr()

    if not abbr:
        frappe.throw(_("Не найдена аббревиатура компании {0}").format(COMPANY))

    return f"{account_name} - {abbr}"


def validate_parent(account):
    parent = account["parent_account"]

    if not frappe.db.exists("Account", parent):
        frappe.throw(
            _("Не найден родительский счет: {0}").format(parent)
        )

    parent_data = frappe.db.get_value(
        "Account",
        parent,
        ["company", "root_type", "is_group"],
        as_dict=True,
    )

    if parent_data.company != COMPANY:
        frappe.throw(
            _("Родительский счет {0} относится к другой компании").format(parent)
        )

    if not parent_data.is_group:
        frappe.throw(
            _("Родительский счет {0} не является группой").format(parent)
        )

    if parent_data.root_type != account["root_type"]:
        frappe.throw(
            _(
                "Root Type счета {0} не совпадает с Root Type родителя {1}"
            ).format(account["account_name"], parent)
        )


def create_account(account):
    full_name = get_full_account_name(account["account_name"])

    if frappe.db.exists("Account", full_name):
        print(f"SKIP: {full_name} уже существует")
        return full_name

    validate_parent(account)

    doc = frappe.get_doc(
        {
            "doctype": "Account",
            "account_name": account["account_name"],
            "parent_account": account["parent_account"],
            "company": COMPANY,
            "root_type": account["root_type"],
            "account_type": account["account_type"] or None,
            "is_group": account["is_group"],
            "account_currency": account["account_currency"],
        }
    )

    doc.insert(ignore_permissions=True)

    print(
        f"CREATE: {doc.name} | "
        f"RU: {account['account_name_ru']} | "
        f"Parent: {account['parent_account']}"
    )

    return doc.name


def execute():
    if not frappe.db.exists("Company", COMPANY):
        frappe.throw(_("Компания {0} не найдена").format(COMPANY))

    created = []
    skipped = []
    failed = []

    for account in ACCOUNTS:
        full_name = get_full_account_name(account["account_name"])

        try:
            if frappe.db.exists("Account", full_name):
                skipped.append(full_name)
                print(f"SKIP: {full_name}")
                continue

            created.append(create_account(account))

        except Exception as exc:
            failed.append(
                {
                    "account": account["account_name"],
                    "error": str(exc),
                }
            )
            print(f"ERROR: {account['account_name']}: {exc}")

    if failed:
        frappe.db.rollback()

        print("\nИзменения отменены из-за ошибок:")
        for row in failed:
            print(f"- {row['account']}: {row['error']}")

        frappe.throw(
            _("Создание плана счетов отменено. Исправьте ошибки и повторите.")
        )

    frappe.db.commit()

    print("\nГотово.")
    print(f"Создано: {len(created)}")
    print(f"Пропущено: {len(skipped)}")
