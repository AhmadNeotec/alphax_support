// alphax_support/public/js/support_ticket_client_script.js
frappe.ui.form.on("Support Ticket", {
    refresh: function(frm) {
        // Auto-populate site_name, from_user, and raised_by_email
        frm.set_value("site_name", frappe.boot.sitename);
        frm.set_value("from_user", frappe.session.user);
        frm.set_value("raised_by_email", frappe.session.user_email || frappe.session.user);

        // Prevent edits if status is Closed
        if (frm.doc.status === "Closed") {
            frm.set_read_only();
            frappe.msgprint("This ticket is-closed and cannot be edited.");
        }
    }
});