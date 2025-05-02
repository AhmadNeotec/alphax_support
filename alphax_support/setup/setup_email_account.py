# alphax_support/setup/setup_email_account.py
import frappe
import os

@frappe.whitelist(allow_guest=True)
def configure_email_account():
    """Configure Email Account for the current site."""
    email_id = "ahmadpashashaiks@gmail.com"
    account_name = "Alphax Support"

    # Check for existing Email Account by email_id
    existing_account = frappe.db.get_value("Email Account", 
                                         filters={"email_id": email_id}, 
                                         fieldname="name",
                                         as_dict=True)

    smtp_password = os.getenv("SMTP_PASSWORD")
    email_settings = {
        "doctype": "Email Account",
        "email_id": email_id,
        "email_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        "smtp_port": int(os.getenv("SMTP_PORT", 587)),
        "use_ssl": 0,
        "use_tls": 1,
        "login_id": os.getenv("SMTP_USER", email_id),
        "enable_outgoing": 1,
        "default_outgoing": 1,
        "enable_incoming": 0
    }
    if smtp_password:
        email_settings["password"] = smtp_password
    else:
        email_settings["awaiting_password"] = 1
        frappe.log("SMTP_PASSWORD not set; Email Account set to Awaiting Password")

    try:
        if existing_account:
            # Update existing Email Account
            email_account = frappe.get_doc("Email Account", existing_account.name)
            email_account.update(email_settings)
            email_account.save(ignore_permissions=True)
            frappe.log(f"Email Account with email_id '{email_id}' updated successfully")
        else:
            # Create new Email Account
            email_account = frappe.get_doc(email_settings)
            email_account.insert(ignore_permissions=True)
            frappe.log(f"Email Account with email_id '{email_id}' created successfully")

        frappe.db.commit()
        return {"status": "success", "message": f"Email Account '{email_id}' configured"}
    except Exception as e:
        frappe.log_error(f"Email Account setup failed: {str(e)[:100]}")
        frappe.throw(f"Failed to configure Email Account: {str(e)[:100]}")