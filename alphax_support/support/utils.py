# alphax_support/support/utils.py
import frappe

@frappe.whitelist()
def get_current_site():
    """Return the current site name."""
    return frappe.local.site or "Not specified"

def sync_ticket_status(doc, method=None):
    """Sync HD Ticket status changes to the support site."""
    if not doc.has_value_changed("status"):
        return  # No status change, exit

    settings = frappe.get_single("Alphax Support Settings")
    if not settings.enable_notifications:
        frappe.log("Notifications disabled in Alphax Support Settings")
        return

    # Get remote ticket ID
    remote_ticket_id = doc.get("custom_remote_ticket_id")
    if not remote_ticket_id:
        frappe.log_error(f"No remote ticket ID found for source ticket {doc.name}")
        return

    # Fetch API credentials
    api_key = "fadbab726a5c4f4"
    api_secret = "23826bb0fa1096d"

    # Prepare data for status update
    ticket_data = {
        "status": doc.status
    }

    api_url = f"https://support.alphaxerp.com/api/resource/HD Ticket/{remote_ticket_id}"
    headers = {
        "Authorization": f"token {api_key}:{api_secret}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.put(api_url, json=ticket_data, headers=headers)
        response.raise_for_status()
        frappe.log(f"Updated status of remote ticket {remote_ticket_id} to {doc.status}")
    except Exception as e:
        error_message = f"Failed to update status of remote ticket {remote_ticket_id}: {str(e)}"[:120]
        frappe.log_error(error_message)