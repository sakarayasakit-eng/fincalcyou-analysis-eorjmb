import json

def handler(event, context):
    try:
        # Parse the incoming JSON body from the JS fetch
        body = json.loads(event.get('body', '{}'))
        email = body.get('email')
        calc_type = body.get('calc_type')
        url = body.get('url')

        # Log the lead (we will replace this with an email API later)
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
