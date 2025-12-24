# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class MonthlyTarget(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		daily_target_amount: DF.Float
		date: DF.Date
		fiscal_year: DF.Link
		monthly_target_amount: DF.Float
	# end: auto-generated types

	def validate(self):
		self.calculate_daily_target()


	def calculate_daily_target(self):
		daily_target = self.monthly_target_amount / 30
		self.daily_target_amount = daily_target
