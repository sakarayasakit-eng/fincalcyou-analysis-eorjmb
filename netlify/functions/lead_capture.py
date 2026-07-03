import json
import os
import resend

resend.api_key = os.environ.get("RESEND_API_KEY")

def handler(event, context):
    try:
        # Parse the incoming JSON body from the JS fetch
        body = json.loads(event.get('body', '{}'))
        email = body.get('email')
        calc_type = body.get('calc_type')
        url = body.get('url')

        # Log the lead
        print(f"NEW LEAD CAPTURED: {email} for {calc_type} from {url}")

        # Notify via Resend
        resend.Emails.send({
            "from": "fin·calc <onboarding@resend.dev>",
            "to": ["sakarayasakit@gmail.com"],
            "subject": f"New Lead: {calc_type}",
            "html": f"<p>New lead captured on fin·calc.</p><p><b>Email:</b> {email}</p><p><b>Calculator:</b> {calc_type}</p><p><b>Page:</b> {url}</p>"
        })

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Lead captured successfully"}),
            "headers": {
                "Content-Type": "application/json"
            }
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
