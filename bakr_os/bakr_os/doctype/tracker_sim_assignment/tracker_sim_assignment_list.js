frappe.listview_settings["Tracker SIM Assignment"] = {
    hide_name_column: true,

    add_fields: [
        "tracker",
        "sim_card",
        "status"
    ],

    get_indicator(doc) {
        const statusIndicators = {
            "Активна": [
                "Активна",
                "green",
                "status,=,Активна"
            ],

            "Завершена": [
                "Завершена",
                "gray",
                "status,=,Завершена"
            ]
        };

        return statusIndicators[doc.status] || [
            doc.status || "Без статуса",
            "gray",
            `status,=,${doc.status || ""}`
        ];
    }
};
