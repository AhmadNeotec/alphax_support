# alphax_support/setup/create_web_form.py
import frappe

def create_support_web_form():
    """Create a Web Form for raising support tickets."""
    if not frappe.db.exists("Web Form", "Raise Support Ticket"):
        web_form = frappe.get_doc({
            "doctype": "Web Form",
            "title": "Raise Support Ticket",
            "route": "support-ticket",
            "doc_type": "Support Ticket",
            "is_standard": 0,
            "login_required": 1,
            "allow_edit": 1,
            "allow_multiple": 0,
            "allow_delete": 0,
            "show_attachments": 1,
            "max_attachment_size": 10,
            "web_form_fields": [
                {"fieldname": "ticket_id", "fieldtype": "Data", "label": "Ticket ID", "read_only": 1, "hidden": 1},
                {"fieldname": "site_name", "fieldtype": "Data", "label": "Site Name", "read_only": 1, "hidden": 1},
                {"fieldname": "from_user", "fieldtype": "Link", "label": "From User", "read_only": 1, "hidden": 1},
                {"fieldname": "raised_by_email", "fieldtype": "Data", "label": "Raised By Email", "read_only": 1, "hidden": 1},
                {"fieldname": "ticket_type", "fieldtype": "Select", "label": "Ticket Type", "reqd": 1},
                {"fieldname": "plan", "fieldtype": "Select", "label": "Subscription Plan", "reqd": 1},
                {"fieldname": "priority", "fieldtype": "Select", "label": "Priority", "reqd": 1},
                {"fieldname": "status", "fieldtype": "Select", "label": "Status", "read_only": 1, "default": "Open"},
                {"fieldname": "description", "fieldtype": "Text Editor", "label": "Description", "reqd": 1},
                {"fieldname": "attachment", "fieldtype": "Attach", "label": "Attachment"}
            ]
        })
        web_form.insert(ignore_permissions=True)