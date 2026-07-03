import json

def handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        email = body.get('email')
        calc_type = body.get('calc_type')
        url = body.get('url')

        # HERE IS WHERE YOU WILL LATER ADD SENDGRID/HUBSPOT API LOGIC
        print(f"NEW LEAD CAPTURED: {email} for {calc_type} from {url}")

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
