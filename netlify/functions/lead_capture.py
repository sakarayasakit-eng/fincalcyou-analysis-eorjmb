import json
import os
import urllib.request
import urllib.error

def handler(event, context):
    try:
        # Parse the incoming JSON body
        body = json.loads(event.get('body', '{}'))
        email = body.get('email')
        calc_type = body.get('calc_type')
        url = body.get('url')

        # Get API key from environment variables
        api_key = os.environ.get("RESEND_API_KEY")
        if not api_key:
            raise ValueError("RESEND_API_KEY environment variable is missing in Netlify.")

        # Resend API Endpoint
        api_url = "https://api.resend.com/emails"

        # Email Payload
        payload = {
            "from": "FinCalc Leads <onboarding@resend.dev>",
            "to": ["sakarayasakit@gmail.com"],
            "subject": f"NEW LEAD: {calc_type}",
            "html": f"<strong>New Lead Captured!</strong><br>Email: {email}<br>Calculator: {calc_type}<br>Page: {url}"
        }

        data = json.dumps(payload).encode("utf-8")

        # Create the request
        req = urllib.request.Request(api_url, data=data, method='POST')
        req.add_header("Authorization", f"Bearer {api_key}")
        req.add_header("Content-Type", "application/json")

        # Execute the request
        try:
            with urllib.request.urlopen(req) as response:
                response_data = response.read().decode("utf-8")
                print(f"Resend API Success Response: {response_data}")
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            print(f"Resend API HTTPError {e.code}: {error_body}")
            raise Exception(f"Resend API Error: {error_body}")

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Lead captured and email sent successfully"}),
            "headers": {
                "Content-Type": "application/json"
            }
        }
    except Exception as e:
        print(f"Overall Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
