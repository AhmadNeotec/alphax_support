# alphax_support/setup/create_support_role.py
import frappe

@frappe.whitelist()
def create_support_role():
    """Create a Support Agent role."""
    if not frappe.db.exists("Role", "Support Agent"):
        frappe.get_doc({
            "doctype": "Role",
            "role_name": "Support Agent",
            "desk_access": 1
        }).insert(ignore_permissions=True)
        frappe.db.commit()