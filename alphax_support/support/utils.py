# alphax_support/support/utils.py
import frappe

@frappe.whitelist()
def get_current_site():
    """Return the current site name."""
    return frappe.local.site or "Not specified"