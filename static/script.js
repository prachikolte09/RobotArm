document.getElementById("packageForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const widthInput = document.getElementById("width");
    const heightInput = document.getElementById("height");
    const lengthInput = document.getElementById("length");
    const massInput = document.getElementById("mass");

    const width = widthInput.value.trim();
    const height = heightInput.value.trim();
    const length = lengthInput.value.trim();
    const mass = massInput.value.trim();

    // Validate input values
    const numberRegex = /^-?\d*\.?\d+$/; // Updated regex to match numbers (positive or negative)
    if (!numberRegex.test(width) || !numberRegex.test(height) || !numberRegex.test(length) || !numberRegex.test(mass)) {
        alert("Width, height, length, and mass must be valid numbers.");
        return;
    }

    // Convert input values to numbers
    const parsedWidth = parseFloat(width);
    const parsedHeight = parseFloat(height);
    const parsedLength = parseFloat(length);
    const parsedMass = parseFloat(mass);

    // Check if parsed values are positive (optional)
    if (parsedWidth <= 0 || parsedHeight <= 0 || parsedLength <= 0 || parsedMass <= 0) {
        alert("Width, height, length, and mass must be positive numbers.");
        return;
    }

    const response = await fetch("/sort_package/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({width: parsedWidth, height: parsedHeight, length: parsedLength, mass: parsedMass})
    });

    if (response.ok) {
        const data = await response.json();
        console.log(data); // Log response object
        console.log(data.result); // Log the value
        document.getElementById("result").innerHTML = `<div class="alert alert-${data.result === 'STANDARD' ? 'success' : 'danger'}">${data.result}</div>`;
    } else if (response.status === 422) {
        try {
            const errorData = await response.json();
            const errorMessage = typeof errorData === "string" ? errorData : JSON.stringify(errorData);
            // Show a pop-up message for 422 error
            alert(errorMessage);
        } catch (error) {
            alert("An error occurred. Please try again later.");
        }
    } else {
        // Handle other status codes
    }
});
