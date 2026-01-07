# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
import json
import frappe
from frappe.model.document import Document
from frappe import _

class CustomerCart(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from erpnext.crm.doctype.customer_cart_item.customer_cart_item import CustomerCartItem
		from frappe.types import DF

		amended_from: DF.Link | None
		company: DF.Link
		customer: DF.Link
		invoice: DF.Link | None
		mobile_number: DF.Data | None
		services: DF.Table[CustomerCartItem]
	# end: auto-generated types
	
@frappe.whitelist()
def create_pos_invoice(docname, company, customer, date, time, items):
	try:
		doc = frappe.get_doc("Customer Cart", docname)
		pos_profiles = frappe.get_list("POS Profile", filters={"company": company, "disabled": 0})
		
		if pos_profiles:
			pos_profile = frappe.get_doc("POS Profile", pos_profiles[0].name)
		else:
			frappe.throw(_("No POS Profile found"))

		items = json.loads(items)
		inv = frappe.new_doc("POS Invoice")
		inv.company = company
		inv.customer = customer
		inv.posting_date = date
		inv.posting_time = time
		inv.is_pos = 1
		
		inv.items = []
		inv.payments = []
		inv.taxes = []
		for item in items:
			service = frappe.get_doc("Item", item["service"])
			item_defaults = service.item_defaults
			item_price = frappe.get_list("Item Price", filters={"item_code": service.name}, fields=["name", "price_list_rate"])
			
			item_row = {
				"item_code": service.name,
				"item_name": service.item_name,
				"item_name_in_arabic": service.item_name_in_arabic,
				"uom": service.stock_uom if service.stock_uom else "Session",
				"qty": 1,
				"price_list_rate": item_price[0].price_list_rate if item_price else 0.0,
				"rate": item_price[0].price_list_rate if item_price else 0.0,
				"description": service.description,
				"description_in_arabic": service.description_in_arabic,
				"income_account": item_defaults[0].income_account,
				"cost_center": item_defaults[0].selling_cost_center,
			}
			if service.taxes:
				item_row["item_tax_template"] = service.taxes[0].item_tax_template,
			
			inv.append("items", item_row)

		for payment in pos_profile.payments:
			inv.append("payments", {
				"mode_of_payment": payment.mode_of_payment,
			})

		sales_taxes_templates = frappe.get_list("Sales Taxes and Charges Template", filters={"company": company, "is_default": 1})
		if sales_taxes_templates:
			sales_taxes_template = frappe.get_doc("Sales Taxes and Charges Template", sales_taxes_templates[0].name)
			for tax in sales_taxes_template.taxes:
				inv.append("taxes", {
					"charge_type": tax.charge_type,
					"account_head": tax.account_head,
					"description": tax.description,
					"rate": tax.rate,
					"cost_center": tax.cost_center,
					"account_currency": tax.account_currency,
					"tax_amount": tax.tax_amount,
				})
		
		inv.insert()
		doc.invoice = inv.name
		doc.save()
		frappe.db.commit()

		return {"success": True}
	except Exception as e:
		return {"success": False, "message": str(e)}


@frappe.whitelist()
def edit_pos_invoice(invoice_id, company, date, time, items):
	try:
		pos_profiles = frappe.get_list("POS Profile", filters={"company": company, "disabled": 0})
		
		if pos_profiles:
			pos_profile = frappe.get_doc("POS Profile", pos_profiles[0].name)
		else:
			frappe.throw(_("No POS Profile found"))

		items = json.loads(items)
		inv = frappe.get_doc("POS Invoice", invoice_id)
		inv.posting_date = date
		inv.posting_time = time
		
		inv.items = []
		inv.payments = []
		inv.taxes = []

		for item in items:
			service = frappe.get_doc("Item", item["service"])
			item_defaults = service.item_defaults
			item_price = frappe.get_list("Item Price", filters={"item_code": service.name}, fields=["name", "price_list_rate"])
			
			item_row = {
				"item_code": service.name,
				"item_name": service.item_name,
				"item_name_in_arabic": service.item_name_in_arabic,
				"uom": service.stock_uom if service.stock_uom else "Session",
				"qty": 1,
				"price_list_rate": item_price[0].price_list_rate if item_price else 0.0,
				"rate": item_price[0].price_list_rate if item_price else 0.0,
				"description": service.description,
				"description_in_arabic": service.description_in_arabic,
				"income_account": item_defaults[0].income_account,
				"cost_center": item_defaults[0].selling_cost_center,
			}
			if service.taxes:
				item_row["item_tax_template"] = service.taxes[0].item_tax_template,
			
			inv.append("items", item_row)

		for payment in pos_profile.payments:
			inv.append("payments", {
				"mode_of_payment": payment.mode_of_payment,
			})

		sales_taxes_templates = frappe.get_list("Sales Taxes and Charges Template", filters={"company": company, "is_default": 1})
		if sales_taxes_templates:
			sales_taxes_template = frappe.get_doc("Sales Taxes and Charges Template", sales_taxes_templates[0].name)
			for tax in sales_taxes_template.taxes:
				inv.append("taxes", {
					"charge_type": tax.charge_type,
					"account_head": tax.account_head,
					"description": tax.description,
					"rate": tax.rate,
					"cost_center": tax.cost_center,
					"account_currency": tax.account_currency,
					"tax_amount": tax.tax_amount,
				})
		
		inv.save()
		frappe.db.commit()

		return {"success": True}
	except Exception as e:
		return {"success": False, "message": str(e)}
