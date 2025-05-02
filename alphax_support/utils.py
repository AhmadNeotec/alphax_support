# alphax_support/utils.py
import frappe

def send_ticket_notification(doc, method):
    """Send email notification to alphax@support.com when a ticket is created."""
    try:
        frappe.sendmail(
            recipients="alphax@support.com",
            subject=f"New Ticket: {doc.name}",
            message=f"""
                New support ticket created:
                - Ticket ID: {doc.name}
                - Type: {doc.ticket_type}
                - Plan: {doc.plan}
                - Priority: {doc.priority}
                - Description: {doc.description}
                - Raised By: {doc.raised_by_email}
            """,
            sender="alphax@support.com"
        )
        frappe.log(f"Notification sent for ticket {doc.name}")
    except Exception as e:
        frappe.log_error(f"Failed to send ticket notification for {doc.name}: {str(e)[:100]}")