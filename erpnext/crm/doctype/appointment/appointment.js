// Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Appointment", {
	refresh: function (frm) {
		if (frm.doc.lead) {
			frm.add_custom_button(frm.doc.lead, () => {
				frappe.set_route("Form", "Lead", frm.doc.lead);
			});
		}
		if (frm.doc.calendar_event) {
			frm.add_custom_button(__(frm.doc.calendar_event), () => {
				frappe.set_route("Form", "Event", frm.doc.calendar_event);
			});
		}
		if (frm.doc.selected_date) {
			set_available_times(frm);
		}
	},
	onload: function (frm) {
		frm.fields_dict["times"].wrapper.innerHTML = "";
		frm.set_query("appointment_with", function () {
			return {
				filters: {
					name: ["in", ["Customer", "Lead"]],
				},
			};
		});
	},
	selected_date: function (frm) {
		if(frm.doc.selected_date) {
			set_available_times(frm);
		}
	}
});


function set_available_times(frm) {
	frappe.call({
		method: "salon.appointment_api.get_available_times",
		args: {
			current_appointment_id: frm.doc.name || "new",
			date: frm.doc.selected_date,
			department: frm.doc.department,
			employee: frm.doc.employee,
		},
		callback: function(res) {
			if(res.message.times){
				const times = res.message.times;
				const duration = res.message.duration;
				build_buttons_html(frm, times, duration)
				
			}
		}
	})
}

function set_end_date(frm, start_date, duration) {
	frappe.call({
		method: "salon.appointment_api.get_end_date",
		args: {
			start_date: start_date,
			duration: duration,
		},
		callback: function(res) {
			if(res.message){
				const end_date = res.message;
				frm.set_value("scheduled_end_time", end_date);
			}
		}
	})
}

function build_buttons_html(frm, times, duration) {
	// Define how many buttons per row (e.g., 3 buttons per row)
	const buttons_per_row = 5;
	
	let html_content = '<div class="container-fluid">';

	// Loop through the buttons and create rows and columns
	for (let i = 0; i < times.length; i += buttons_per_row) {
		// Start a new row
		html_content += '<div class="row" style="margin-bottom: 10px; gap: 20px;">'; 

		// Get the buttons for the current row
		const row_times = times.slice(i, i + buttons_per_row);

		row_times.forEach(time => {
			// Determine the column size (e.g., col-md-4 for 3 columns)
			const col_size = 12 / buttons_per_row;
			
			// Add button inside a column. Use data-action to identify which button was clicked.
			html_content += `
				<div class="col-md-${col_size}">
					<button class="btn btn-primary" ${time.available ? "" : "disabled"}>
						${time.value}
					</button>
				</div>
			`;
		});

		// Close the row
		html_content += '</div>';
	}

	html_content += '</div>'; // Close container-fluid

	// --- 2. Set the HTML to the HTML field and add click handler ---
	const html_field_wrapper = frm.fields_dict["times"].wrapper;
	
	// Use jQuery to set the HTML content
	$(html_field_wrapper).html(html_content);
	
	// Attach click handler to the wrapper to handle all button clicks
	$(html_field_wrapper).on("click", (e) => {
		const selected_time = e.target.innerText;
		const start_date = `${frm.doc.selected_date} ${selected_time}`
		set_dates(frm, start_date, duration);
	});
}

function set_dates(frm, start_date, duration) {
	frm.set_value("scheduled_time", start_date);

	set_end_date(frm, start_date, duration);
}