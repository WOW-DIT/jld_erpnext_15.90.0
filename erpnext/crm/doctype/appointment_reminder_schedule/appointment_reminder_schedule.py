# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AppointmentReminderSchedule(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		before_date: DF.Duration
		channel: DF.Literal["", "WhatsApp", "SMS", "WhatsApp & SMS"]
		enabled: DF.Check
		title: DF.Data
		whatsapp_template: DF.Link | None
	# end: auto-generated types
	pass
