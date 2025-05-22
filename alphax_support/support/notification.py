import frappe
import requests
from frappe import _
import re
from tenacity import retry, stop_after_attempt, wait_fixed

@frappe.whitelist(allow_guest=True)
def send_ticket_notification(doc, method=None):
    """Send email notification and create a ticket on support.alphaxerp.com when a new HD Ticket is created."""
    settings = frappe.get_single("Alphax Support Settings")
    if not settings.enable_notifications:
        frappe.log("Notifications disabled in Alphax Support Settings")
        return

    # Determine the sender email dynamically
    raised_by = doc.raised_by or "Guest"
    email_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    sender = raised_by if email_pattern.match(raised_by) else settings.support_email

    # Prepare email content
    subject = f"New Ticket Raised: {doc.subject}"
    message = f"""
    A new ticket has been raised:
    Ticket ID: {doc.name}
    Subject: {doc.subject}
    Site Name: {frappe.local.site}
    Ticket Type: {getattr(doc, 'ticket_type', 'Unspecified')}
    Plan: {getattr(doc, 'custom_plan', 'Not specified')}
    Description: {doc.description or 'No description provided'}
    Raised By: {raised_by}
    Priority: {doc.priority or 'Medium'}
    Status: {doc.status or 'Open'}

    Please review the ticket at: https://{frappe.local.site}/helpdesk/tickets/{doc.name}
    """
    recipients = [settings.support_email]

    # Send email
    try:
        frappe.sendmail(
            recipients=recipients,
            subject=subject,
            message=message,
            sender=sender
        )
        frappe.log(f"Notification sent for ticket {doc.name} from {sender}")
    except Exception as e:
        frappe.log_error(f"Failed to send notification for ticket {doc.name} from {sender}: {str(e)}")

    # Fetch API credentials from settings
    api_key = "ca80ab27649fc73"
    api_secret = "1142651de7e248d"

    # Create ticket on support.alphaxerp.com
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def create_remote_ticket(api_url, ticket_data, headers):
        response = requests.post(api_url, json=ticket_data, headers=headers)
        response.raise_for_status()
        return response

    try:
        truncated_subject = (doc.subject or "")[:140]
        truncated_description = (doc.description or "No description provided")[:10000]
        truncated_site_name = frappe.local.site[:140]  # Use domain
        truncated_raised_by = (raised_by)[:140]

        ticket_data = {
            "doctype": "HD Ticket",
            "subject": truncated_subject,
            "description": truncated_description,
            "status": doc.status or "Open",
            "priority": doc.priority or "Medium",
            "raised_by": truncated_raised_by,
            "custom_site_name": truncated_site_name,
            "ticket_type": getattr(doc, "ticket_type", ""),
            "custom_plan": getattr(doc, "custom_plan", ""),
            "custom_source_ticket_id": doc.name
        }

        api_url = "https://support.alphaxerp.com/api/resource/HD Ticket"
        headers = {
            "Authorization": f"token {api_key}:{api_secret}",
            "Content-Type": "application/json"
        }

        response = create_remote_ticket(api_url, ticket_data, headers)
        response_data = response.json()
        remote_ticket_id = response_data.get("data", {}).get("name")
        if remote_ticket_id:
            frappe.db.set_value("HD Ticket", doc.name, "custom_remote_ticket_id", remote_ticket_id)
            frappe.db.commit()
            frappe.log(f"Created ticket {remote_ticket_id} on support.alphaxerp.com for source ticket {doc.name}")
    except Exception as e:
        error_message = f"Failed to create ticket on support.alphaxerp.com for {doc.name}: {str(e)}"[:120]
        frappe.log_error(error_message)