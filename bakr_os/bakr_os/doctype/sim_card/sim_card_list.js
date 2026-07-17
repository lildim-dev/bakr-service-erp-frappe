frappe.listview_settings["Sim Card"] = {
    hide_name_column: true,

    add_fields: [
        "iccid",
        "phone_number",
        "operator",
        "tariff",
        "status"
    ],

    get_indicator(doc) {
        const statusIndicators = {
            "Получена": ["Получена", "gray", "status,=,Получена"],

            "Ожидает активации": [
                "Ожидает активации",
                "orange",
                "status,=,Ожидает активации"
            ],

            "Активна": [
                "Активна",
                "green",
                "status,=,Активна"
            ],

            "Установлена": [
                "Установлена",
                "blue",
                "status,=,Установлена"
            ],

            "Приостановлена": [
                "Приостановлена",
                "yellow",
                "status,=,Приостановлена"
            ],

            "Заблокирована": [
                "Заблокирована",
                "red",
                "status,=,Заблокирована"
            ],

            "Утеряна": [
                "Утеряна",
                "red",
                "status,=,Утеряна"
            ],

            "Списана": [
                "Списана",
                "gray",
                "status,=,Списана"
            ]
        };

        return statusIndicators[doc.status] || [
            doc.status || "Без статуса",
            "gray",
            `status,=,${doc.status || ""}`
        ];
    }
};