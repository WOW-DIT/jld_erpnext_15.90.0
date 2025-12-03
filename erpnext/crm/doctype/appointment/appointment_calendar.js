frappe.views.calendar["Appointment"] = {
	field_map: {
		"start": "scheduled_time",
		"end": "scheduled_end_time",
		"id": "name",
		// "allDay": "all_day",
		"title": "party",
		// status: "status",
		// color: "color",
	},
	get_events_method: "frappe.desk.calendar.get_events",
};
