const API_BASE_URL = "http://127.0.0.1:8000/api";

// The Master Switch (Triggered by the button)
function fetchAllData() {
    // 1. Grab whatever the user typed into the text boxes
    const githubUser = document.getElementById("github-input").value;
    const leetcodeUser = document.getElementById("leetcode-input").value;
    const codechefUser = document.getElementById("codechef-input").value;

    // 2. Change the screen to say "Loading..." while we wait
    document.getElementById("github-repos").innerText = "...";
    document.getElementById("github-followers").innerText = "...";
    document.getElementById("leetcode-rank").innerText = "...";
    document.getElementById("leetcode-solved").innerText = "...";
    document.getElementById("codechef-rating").innerText = "...";

    // 3. Fire the API calls!
    if (githubUser) getGithubData(githubUser);
    if (leetcodeUser) getLeetCodeData(leetcodeUser);
    if (codechefUser) getCodeChefData(codechefUser);
}

// Fetch GitHub Stats dynamically
async function getGithubData(username) {
    try {
        // We use backticks ` and ${username} to inject the variable into the URL!
        const response = await fetch(`${API_BASE_URL}/github/${username}`);
        const data = await response.json();
        document.getElementById("github-repos").innerText = data.public_repos;
        document.getElementById("github-followers").innerText = data.followers;
    } catch (error) {
        document.getElementById("github-repos").innerText = "Error";
    }
}

// Fetch LeetCode Stats dynamically
async function getLeetCodeData(username) {
    try {
        const response = await fetch(`${API_BASE_URL}/leetcode/${username}`);
        const data = await response.json();
        document.getElementById("leetcode-rank").innerText = data.ranking;
        document.getElementById("leetcode-solved").innerText = data.total_solved;
    } catch (error) {
        document.getElementById("leetcode-solved").innerText = "Error";
    }
}

// Fetch CodeChef Stats dynamically
async function getCodeChefData(username) {
    try {
        const response = await fetch(`${API_BASE_URL}/codechef/${username}`);
        const data = await response.json();
        document.getElementById("codechef-rating").innerText = data.current_rating;
    } catch (error) {
        document.getElementById("codechef-rating").innerText = "Error";
    }
}

// Automatically fetch your stats when the page first loads
fetchAllData();