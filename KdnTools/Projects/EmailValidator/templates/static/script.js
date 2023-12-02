document.getElementById("email-form").addEventListener("submit", function (event) {
    event.preventDefault();
    const email = document.getElementById("email").value;
    const resultDiv = document.getElementById("result");
    fetch("http://localhost:5000/validate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({email: email}),
    })
        .then(response => response.json())
        .then(data => {
            resultDiv.classList.add(data.result ? "alert-success" : "alert-danger");
            resultDiv.textContent = data.result ? "The email is valid." : "The email is invalid.";
        })
        .catch((error) => {
            console.error("Error:", error);
        });
});