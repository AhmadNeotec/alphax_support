import frappe
from frappe import _

@frappe.whitelist(allow_guest=False)
def update_ticket_status(ticket_id, status, support_ticket_id):
    """Update the status of a ticket on the customer site based on the support site."""
    try:
        # Verify the ticket exists
        if not frappe.db.exists("HD Ticket", ticket_id):
            frappe.log_error(f"Ticket {ticket_id} not found on site {frappe.local.site}")
            return {"status": "error", "message": f"Ticket {ticket_id} not found"}

        # Update the ticket status
        ticket = frappe.get_doc("HD Ticket", ticket_id)
        ticket.status = status
        ticket.save(ignore_permissions=True)

        frappe.log(f"Updated ticket {ticket_id} status to {status} based on support ticket {support_ticket_id}")
        return {"status": "success", "message": f"Ticket {ticket_id} updated to {status}"}
    except Exception as e:
        frappe.log_error(f"Failed to update ticket {ticket_id} status: {str(e)}")
        return {"status": "error", "message": str(e)}