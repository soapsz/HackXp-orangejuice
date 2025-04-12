// leaderboard.js

const LOCAL_STORAGE_KEY = 'leaderboardEntries';

// Stores data in localStorage
function storeData(key, data) {
    try {
        const serializedData = JSON.stringify(data);
        localStorage.setItem(key, serializedData);
    } catch (err) {
        console.error('Error storing data in localStorage:', err);
    }
}

// Retrieves data from localStorage
function retrieveData(key) {
    try {
        const serializedData = localStorage.getItem(key);
        if (serializedData === null) {
            return null;
        }
        return JSON.parse(serializedData);
    } catch (err) {
        console.error('Error retrieving data from localStorage:', err);
        return null;
    }
}

// Example default data
const defaultData = [
    ["Alex", "Jordan", 180],
    ["Jordan", "Alex", 20],
    ["Taylor", "Casey", 200],
    ["Casey", "Taylor", 190],
    ["Drew", "Morgan", 5]
];

// Main function to run on page load
window.onload = function () {
    let leaderboardData = retrieveData(LOCAL_STORAGE_KEY);

    // If no existing data, use default and store it
    if (!leaderboardData) {
        leaderboardData = defaultData;
        storeData(LOCAL_STORAGE_KEY, leaderboardData);
    }

    // Sort data by descending score
    leaderboardData.sort((a, b) => b[2] - a[2]);

    // Set leaderboard titles
    document.getElementById("leaderboardTitle").innerText = "💝 Friendship Leaderboard";
    document.getElementById("leaderboardTitle2").innerText = "Top 5 Dynamic Duos";

    // Fill leaderboard rows
    leaderboardData.slice(0, 5).forEach(([gifter, giftee, points], index) => {
        const rank = index + 1;
        document.getElementById(`rank${rank}gifter`).innerText = gifter;
        document.getElementById(`rank${rank}giftee`).innerText = giftee;
        document.getElementById(`rank${rank}points`).innerText = points;
    });

    // Fill remaining rows with placeholders if fewer than 5 entries
    for (let i = leaderboardData.length + 1; i <= 5; i++) {
        document.getElementById(`rank${i}gifter`).innerText = "-";
        document.getElementById(`rank${i}giftee`).innerText = "-";
        document.getElementById(`rank${i}points`).innerText = "-";
    }
};
