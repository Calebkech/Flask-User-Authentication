// Array of valid usernames and passwords
const users = [
    { username: "falcon", password: "falcon1#" },
    { username: "storm", password: "storm2@" },
    { username: "digitflow", password: "tarrrychess" },
    { username: "wave", password: "wave4$" },
    { username: "blaze", password: "blaze5%" },
    { username: "shadow", password: "shadow6^" },
    { username: "fist", password: "fist7&" },
    { username: "fox", password: "fox8*" },
    { username: "ghost", password: "ghost9#" },
    { username: "wolf", password: "wolf0@" },
    { username: "dragon", password: "dragon1!" },
    { username: "crimson", password: "crimson2$" },
    { username: "crow", password: "crow3%" },
    { username: "owl", password: "owl4^" },
    { username: "frost", password: "frost5&" },
    { username: "cyber", password: "cyber6*" },
    { username: "gold", password: "gold7#" },
    { username: "knight", password: "knight8@" },
    { username: "tiger", password: "tiger9!" },
    { username: "moon", password: "moon0$" }
];

function login() {
    // Get user input
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();

    // Check if the credentials match any user in the array
    const isValid = users.some(user => user.username === username && user.password === password);

    if (isValid) {
        // Hide login page and show dashboard
        document.getElementById('loginPage').style.display = "none";
        document.getElementById('dashboard').style.display = "block";
        document.getElementById('loginError').style.display = "none"; // Hide error if previously shown
    } else {
        // Show error message
        document.getElementById('loginError').style.display = "block";
    }
}

function logout() {
    // Hide dashboard and show login page
    document.getElementById('dashboard').style.display = "none";
    document.getElementById('loginPage').style.display = "block";
    document.getElementById('loginError').style.display = "none"; // Reset error message
}
