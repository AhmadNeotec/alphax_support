import frappe

def execute():
    # Check if HD Ticket DocType exists
    if not frappe.db.exists("DocType", "HD Ticket"):
        print("HD Ticket DocType not found. Skipping custom field creation.")
        return

    # Add custom_site_name field
    if not frappe.db.exists("Custom Field", {"dt": "HD Ticket", "fieldname": "custom_site_name"}):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "HD Ticket",
            "fieldname": "custom_site_name",
            "fieldtype": "Data",
            "label": "Site Name",
            "insert_after": "subject",
            "module": "Alphax Support",
            "translatable": 1
        }).insert()

    # Add custom_plan field
    if not frappe.db.exists("Custom Field", {"dt": "HD Ticket", "fieldname": "custom_plan"}):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "HD Ticket",
            "fieldname": "custom_plan",
            "fieldtype": "Select",
            "label": "Plan",
            "options": "Basic\nPremium\nEnterprise",
            "insert_after": "custom_site_name",
            "module": "Alphax Support",
            "translatable": 1
        }).insert()

    # Add custom_remote_ticket_id field
    if not frappe.db.exists("Custom Field", {"dt": "HD Ticket", "fieldname": "custom_remote_ticket_id"}):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "HD Ticket",
            "fieldname": "custom_remote_ticket_id",
            "fieldtype": "Data",
            "label": "Remote Ticket ID",
            "insert_after": "custom_plan",
            "module": "Alphax Support",
            "read_only": 1,
            "translatable": 0
        }).insert()

    print("Custom fields custom_site_name, custom_plan, and custom_remote_ticket_id added to HD Ticket.")