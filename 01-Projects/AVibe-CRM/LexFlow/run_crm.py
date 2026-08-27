# CRM ENTRY POINT - use this file to run the CRM app.
# DO NOT use app.py for CRM work. app.py runs the legacy intake app only.

from crm import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
