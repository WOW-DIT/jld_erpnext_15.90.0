# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
from salon.utilities.scheduler import unify_mobile_number

class ServiceReview(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		customer: DF.Link | None
		description: DF.Text | None
		employee: DF.Link
		mobile_number: DF.ReadOnly | None
		order_id: DF.Link
		rating: DF.Rating
		rating_number: DF.Int
		service: DF.Link
		status: DF.Literal["Pending", "Reviewed"]
	# end: auto-generated types
	
	def after_insert(self):
		try:
			whatsapp_settings = frappe.get_doc("WhatsApp Settings", "WhatsApp Settings")
			api_base_url = whatsapp_settings.api_url
			api_key = whatsapp_settings.get_password("api_key")

			whatsapp_number = frappe.get_doc("WhatsApp Number", whatsapp_settings.default_review_number)

			url = f"{api_base_url}/whatsapp_integration.whatsapp_api.send_whatsapp_interactive_standalone"
			headers = {"Authorization": f"Basic {api_key}"}

			customer = frappe.get_doc("Customer", self.customer)
			body = {
				"instance_id": whatsapp_number.instance_id,
				"to_number": unify_mobile_number(customer.mobile_no, customer),
				"header_text": "Service Satisfaction Feedback",
				"body_text": f"We'd appreciate a quick rating of your experience with *{self.service}*. Your feedback helps us improve.",
				"footer_text": "Jean Louis David Salon",
				"button_text": "Rate Service",
				"sections": [
					{
						"title": self.service,
						"rows": [
							{
								"id": f"{self.name}_1",
								"title": "⭐",
								"description": "Poor"
							},
							{
								"id": f"{self.name}_2",
								"title": "⭐⭐",
								"description": "Good"
							},
							{
								"id": f"{self.name}_3",
								"title": "⭐⭐⭐",
								"description": "Very Good"
							},
							{
								"id": f"{self.name}_4",
								"title": "⭐⭐⭐⭐",
								"description": "Excellent"
							},
							{
								"id": f"{self.name}_5",
								"title": "⭐⭐⭐⭐⭐",
								"description": "Perfect"
							}
						]
					}
				]
			}
			response = requests.post(url, headers=headers, json=body)

			if response.status_code != 200:
				frappe.throw(response.text)
			
		except Exception as e:
			frappe.throw(str(e))

