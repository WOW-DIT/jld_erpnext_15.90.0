// Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Customer Cart", {
	refresh(frm) {
        if(!frm.doc.name.startsWith("new")) {
            if(!frm.doc.invoice) {
                frm.add_custom_button(__('Create Invoice'), () => {
                    create_pos_invoice(frm);
                }, __('Actions'));

            } else {
                frm.add_custom_button(__('Open Point of Sale'), () => {
                    openPOS(frm.doc.invoice);
                }, __('Actions'));

                frm.add_custom_button(__('Update Invoice'), () => {
                    edit_pos_invoice(frm);
                }, __('Actions'));
            }
        }
	},
});

function create_pos_invoice(frm) {
    if(!frm.doc.services || frm.doc.services.length == 0) {
        frappe.throw(__("You should add 1 service at least!"))
    }
    frappe.call({
        method: "erpnext.crm.doctype.customer_cart.customer_cart.create_pos_invoice",
        args: {
            docname: frm.doc.name,
            company: frm.doc.company,
            customer: frm.doc.customer,
            items: frm.doc.services,
            date: frappe.datetime.get_today(),
            time: frappe.datetime.get_time(),
        },
        freeze: true,
        freeze_message: "يتم إنشاء فاتورة جديدة...",
        callback: function(res) {
            if(res && res.message) {
                console.log(res.message)
                const success = res.message.success;
                if (success) {
                    location.reload();
                }
            }
        }
    })
}


function edit_pos_invoice(frm) {
    if(!frm.doc.services || frm.doc.services.length == 0) {
        frappe.throw(__("You should add 1 service at least!"))
    }
    frappe.call({
        method: "erpnext.crm.doctype.customer_cart.customer_cart.edit_pos_invoice",
        args: {
            invoice_id: frm.doc.invoice,
            company: frm.doc.company,
            items: frm.doc.services,
            date: frappe.datetime.get_today(),
            time: frappe.datetime.get_time(),
        },
        freeze: true,
        freeze_message: "يتم تعديل فاتورة...",
        callback: function(res) {
            if(res && res.message) {
                console.log(res.message)
                const success = res.message.success;
                if (success) {
                    frappe.show_alert({
                        message: __("Invoice updated successfully"),
                        indicator: "green"
                    });
                } else {
                    frappe.show_alert({
                        message: __(res.message.message),
                        indicator: "red"
                    });
                }
            }
        }
    })
}

function openPOS(text) {
    navigator.clipboard.writeText(text).then(() => {
        frappe.show_alert({
            message: __('Copied to clipboard'),
            indicator: 'green'
        });
        location.href = "/app/point-of-sale";
    }).catch(() => {
        frappe.msgprint(__('Failed to copy'));
    });
}