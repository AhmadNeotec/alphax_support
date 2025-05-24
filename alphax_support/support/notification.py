import frappe
import requests
from frappe import _
import re

@frappe.whitelist(allow_guest=True)
def send_ticket_notification(doc, method=None):
    """Send email notification and create a ticket on support.alphaxerp.com when a new HD Ticket is created."""
    settings = frappe.get_single("Alphax Support Settings")
    if not settings.enable_notifications:
        frappe.log("Notifications disabled in Alphax Support Settings")
        return

    # Determine the sender email dynamically
    raised_by = doc.raised_by or "Guest"
    # Regular expression to validate email format
    email_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    sender = raised_by if email_pattern.match(raised_by) else settings.support_email

    # Prepare email content
    subject = f"New Ticket Raised: {doc.subject}"
    message = f"""
    A new ticket has been raised:
    Ticket ID: {doc.name}
    Subject: {doc.subject}
    Site Name: {getattr(doc, 'custom_site_name', 'Not specified')}
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
    api_key = "fadbab726a5c4f4"
    api_secret = "6d1c3c0ae161d15"

    # Create ticket on support.alphaxerp.com
    try:
        # Truncate fields to avoid length issues
        truncated_subject = (doc.subject or "")[:140]
        truncated_description = (doc.description or "No description provided")[:10000]  # Arbitrary safe limit
        truncated_site_name = (getattr(doc, "custom_site_name", "") or "")[:140]
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

        response = requests.post(api_url, json=ticket_data, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        remote_ticket_id = response_data.get("data", {}).get("name")
        frappe.log(f"Created ticket {remote_ticket_id} on support.alphaxerp.com for source ticket {doc.name}")
    except Exception as e:
        # Truncate the error message to avoid CharacterLengthExceededError in Error Log
        error_message = f"Failed to create ticket on support.alphaxerp.com for {doc.name}: {str(e)}"[:120]
        frappe.log_error(error_message)
