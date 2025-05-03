// alphax_support/public/js/helpdesk_custom.js
frappe.provide("frappe.helpdesk");

// Override the Helpdesk ticket creation form
frappe.ui.form.on("HD Ticket", {
    before_save(frm) {
        if (window.location.pathname.includes("/helpdesk/tickets")) {
            // Fetch the site name before saving
            frappe.call({
                method: "alphax_support.support.utils.get_current_site",
                callback: function(r) {
                    if (r.message && !frm.doc.custom_site_name) {
                        frm.set_value("custom_site_name", r.message);
                        console.log("Set custom_site_name in Helpdesk UI:", r.message);
                    }
                }
            });
        }
    }
});