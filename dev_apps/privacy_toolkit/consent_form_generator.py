# 3. Tools to Generate Consent Forms Dynamically
# ----------------------------------------------
# A dynamic tool using string.Template to generate custom consent forms for clients

from string import Template

def generate_consent_form(name, service, organization):
    form_template = Template("""
    CONSENT FORM
    -------------
    I, $name, hereby give $organization the permission to collect and use my personal information
    for the purpose of $service, in accordance with data protection regulations.

    Signature: ____________________
    Date: _________________________
    """)
    return form_template.substitute(name=name, service=service, organization=organization)

print(generate_consent_form("Jane Doe", "email marketing", "Acme Corp"))

