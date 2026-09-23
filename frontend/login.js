const API_URL = "http://127.0.0.1:5000";

const loginForm = document.getElementById("login-form");
const loginMessage = document.getElementById("login-message");

loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const username =
        document.getElementById("login-username").value;

    const password =
        document.getElementById("login-password").value;

    try {
        const response = await fetch(`${API_URL}/api/login`, {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            loginMessage.textContent =
                data.error || "Login failed.";

            return;
        }

        localStorage.setItem(
            "user_id",
            data.user_id
        );

        localStorage.setItem(
            "username",
            data.username
        );

        window.location.href = "index.html";

    } catch (error) {
        console.error(error);

        loginMessage.textContent =
            "Unable to connect to the server.";
    }
});