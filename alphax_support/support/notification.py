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
    email_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    sender = raised_by if email_pattern.match(raised_by) else settings.support_email

    # Validate sender and recipient emails
    if not email_pattern.match(sender):
        frappe.log_error(f"Invalid sender email: {sender} for ticket {doc.name}")
        return
    if not settings.support_email or not email_pattern.match(settings.support_email):
        frappe.log_error(f"Invalid support email in Alphax Support Settings: {settings.support_email}")
        return

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

    # Send email (ensure it goes to Email Queue)
    try:
        email_args = {
            "recipients": recipients,
            "subject": subject,
            "message": message,
            "sender": sender,
            "now": False  # Ensure email is queued
        }
        # Enqueue the email manually to inspect the process
        email_queue_entry = frappe.enqueue(
            method=frappe.sendmail,
            queue="short",
            timeout=300,
            is_async=True,
            **email_args
        )
        frappe.log(f"Email queued for ticket {doc.name} from {sender} to {recipients}. Queue ID: {email_queue_entry}")
    except Exception as e:
        frappe.log_error(f"Failed to queue email for ticket {doc.name} from {sender}: {str(e)}")
        return

    # Hardcoded API credentials
    api_key = "fadbab726a5c4f4"
    api_secret = "6d1c3c0ae161d15"

    # Create ticket on support.alphaxerp.com
    try:
        truncated_subject = (doc.subject or "")[:140]
        truncated_description = (doc.description or "No description provided")[:10000]
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

        frappe.log(f"Sending ticket data to support.alphaxerp.com: {ticket_data}")
        response = requests.post(api_url, json=ticket_data, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        remote_ticket_id = response_data.get("data", {}).get("name")

        # Update the customer ticket with the support ticket ID
        doc.custom_support_ticket_id = remote_ticket_id
        doc.save(ignore_permissions=True)

        frappe.log(f"Created ticket {remote_ticket_id} on support.alphaxerp.com for source ticket {doc.name}")
    except requests.exceptions.RequestException as e:
        error_message = f"Failed to create ticket on support.alphaxerp.com for {doc.name}: Status {e.response.status_code if e.response else 'N/A'}, Response {e.response.text if e.response else str(e)}"[:120]
        frappe.log_error(error_message)