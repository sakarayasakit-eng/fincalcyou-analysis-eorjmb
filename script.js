function calculateDSCR() {
    const income = parseFloat(document.getElementById('rentalIncome').value) || 0;
    const expenses = parseFloat(document.getElementById('operatingExpenses').value) || 0;
    const debt = parseFloat(document.getElementById('annualDebtService').value) || 0;

    if (income === 0 || debt === 0) {
        alert("Please enter valid income and debt service numbers.");
        return;
    }

    const noi = income - expenses;
    const dscr = noi / debt;

    const resultBox = document.getElementById('resultBox');
    const dscrValue = document.getElementById('dscrValue');
    const dscrMessage = document.getElementById('dscrMessage');
    const leadGate = document.getElementById('leadGate');

    dscrValue.textContent = dscr.toFixed(2);

    let message = "";
    if (dscr >= 1.25) {
        message = "Excellent! Your property cash flows well. You likely qualify for a DSCR loan.";
        dscrValue.style.color = "green";
    } else if (dscr >= 1.0) {
        message = "Warning: Your property breaks even, but may not meet the 1.25 minimum lender requirement.";
        dscrValue.style.color = "orange";
    } else {
        message = "Danger: Negative cash flow. The property does not generate enough income to cover its debt.";
        dscrValue.style.color = "red";
    }

    dscrMessage.innerText = message;
    resultBox.style.display = 'block';

    leadGate.style.display = 'block';
    leadGate.scrollIntoView({ behavior: 'smooth' });
}

async function submitLead() {
    const email = document.getElementById('userEmail').value;
    if (!email || !email.includes('@')) {
        alert("Please enter a valid email address.");
        return;
    }

    try {
        const response = await fetch('/.netlify/functions/lead_capture', {
            method: 'POST',
            body: JSON.stringify({
                email: email,
                calc_type: 'DSCR Short-Term Rental',
                url: window.location.href
            })
        });

        if (response.ok) {
            alert("Success! Check your email for your full analysis.");
            document.getElementById('leadGate').innerHTML = "<h3>Thank you! Your analysis is on the way.</h3>";
        } else {
            alert("There was an error. Please try again.");
        }
    } catch (error) {
        console.error('Error:', error);
        alert("There was a network error.");
    }
}
