exports.handler = async (event) => {
    try {
        // Parse the incoming JSON body
        const body = JSON.parse(event.body || '{}');
        const email = body.email;
        const calc_type = body.calc_type;
        const url = body.url;

        // Get API key from environment variables
        const apiKey = process.env.RESEND_API_KEY;
        if (!apiKey) {
            throw new Error("RESEND_API_KEY environment variable is missing in Netlify.");
        }

        // Resend API Endpoint
        const apiUrl = "https://api.resend.com/emails";

        // Email Payload
        const payload = {
            from: "FinCalc Leads <onboarding@resend.dev>",
            to: ["sakarayasakit@gmail.com"],
            subject: `NEW LEAD: ${calc_type}`,
            html: `<strong>New Lead Captured!</strong><br>Email: ${email}<br>Calculator: ${calc_type}<br>Page: ${url}`
        };

        // Execute the request using native fetch (Node 18+)
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.text();
            console.error("Resend API Error:", errorData);
            throw new Error(`Resend API Error: ${errorData}`);
        }

        const data = await response.json();
        console.log("Resend API Success Response:", data);

        return {
            statusCode: 200,
            body: JSON.stringify({ message: "Lead captured and email sent successfully" }),
            headers: {
                "Content-Type": "application/json"
            }
        };
    } catch (error) {
        console.error("Overall Error:", error.message);
        return {
            statusCode: 500,
            body: JSON.stringify({ error: error.message })
        };
    }
};
# diagnostic: confirming auto-deploy trigger 2026-07-03T23:21:57Z
