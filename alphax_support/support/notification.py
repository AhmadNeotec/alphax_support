# alphax_support/support/notification.py
import frappe

@frappe.whitelist(allow_guest=True)
def send_ticket_notification(doc, method=None):
    """Send email notification to the configured support email when a new HD Ticket is created."""
    # Fetch settings
    settings = frappe.get_single("Alphax Support Settings")
    if not settings.enable_notifications:
        frappe.log("Notifications disabled in Alphax Support Settings")
        return

    # Prepare email content
    subject = f"New Ticket Raised: {doc.subject}"
    message = f"""
    A new ticket has been raised:
    Ticket ID: {doc.name}
    Subject: {doc.subject}
    Site Name: {doc.site_name or 'Not specified'}
    Ticket Type: {doc.ticket_type or 'Unspecified'}
    Plan: {doc.plan or 'Not specified'}
    Description: {doc.description or 'No description provided'}
    Raised By: {doc.raised_by or 'Guest'}
    Priority: {doc.priority or 'Medium'}
    Status: {doc.status or 'Open'}

    Please review the ticket at: https://{frappe.local.site}/helpdesk/tickets/{doc.name}
    """
    recipients = [settings.support_email]

    # Send email using Frappe's email API
    try:
        frappe.sendmail(
            recipients=recipients,
            subject=subject,
            message=message,
            sender="support@neotechiss.com"
        )
        frappe.log(f"Notification sent for ticket {doc.name}")
    except Exception as e:
        frappe.log_error(f"Failed to send notification for ticket {doc.name}: {str(e)}")