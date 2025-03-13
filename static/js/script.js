// Base URL of your FastAPI backend
const BASE_URL = "http://localhost:8000"; // Replace with actual URL of FastAPI Backend

// Function to handle hourly data submission
async function submitHourlyData(event) {
    event.preventDefault(); // Prevent the default form submission behavior

    // Get form input values
    const timestamp = document.getElementById("timestamp").value;
    const flowRate = document.getElementById("flowRate").value;
    const cod = document.getElementById("cod").value;
    const waterQuality = document.getElementById("waterQuality").value;

    try {
        // Send POST request to FastAPI
        const response = await fetch(`${BASE_URL}/submit-hourly`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({
                timestamp: timestamp,
                flow_rate: flowRate,
                cod: cod,
                water_quality: waterQuality,
            }),
        });

        const result = await response.json();
        if (response.ok) {
            alert("Hourly data submitted successfully!");
        } else {
            alert(`Error: ${result.detail || "Failed to submit data"}`);
        }
    } catch (error) {
        console.error("Error submitting hourly data:", error);
        alert("Failed to submit hourly data.");
    }
}

// Function to handle daily summary submission
async function submitDailySummary(event) {
    event.preventDefault(); // Prevent the default form submission behavior

    // Get form input values
    const date = document.getElementById("date").value;
    const clarifierStatus = document.getElementById("clarifierStatus").value;
    const observations = document.getElementById("observations").value;

    try {
        // Send POST request to FastAPI
        const response = await fetch(`${BASE_URL}/submit-daily`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({
                date: date,
                clarifier_status: clarifierStatus,
                observations: observations,
            }),
        });

        const result = await response.json();
        if (response.ok) {
            alert("Daily summary submitted successfully!");
        } else {
            alert(`Error: ${result.detail || "Failed to submit data"}`);
        }
    } catch (error) {
        console.error("Error submitting daily summary:", error);
        alert("Failed to submit daily summary.");
    }
}



// Function to list exported files
async function listExports() {
    try {
        // Send GET request to FastAPI
        const response = await fetch(`${BASE_URL}/list-exports`, {
            method: "GET",
        });

        const files = await response.json();
        if (response.ok) {
            const fileListElement = document.getElementById("fileList");
            fileListElement.innerHTML = ""; // Clear the list

            if (files.length > 0) {
                files.forEach((file) => {
                    const listItem = document.createElement("li");
                    listItem.textContent = file;
                    fileListElement.appendChild(listItem);
                });
            } else {
                fileListElement.textContent = "No files found.";
            }
        } else {
            alert("Failed to list export files.");
        }
    } catch (error) {
        console.error("Error listing exports:", error);
        alert("Failed to fetch export files.");
    }
}


// Toggle between light mode and dark mode
document.addEventListener("DOMContentLoaded", () => {
    setTimeout(() => {
        const toggleButton = document.getElementById("modeToggle");

        toggleButton.addEventListener("click", () => {
            document.body.classList.toggle("dark-mode");

            // Update the button text based on the current mode
            if (document.body.classList.contains("dark-mode")) {
                toggleButton.textContent = "Switch to Light Mode";
            } else {
                toggleButton.textContent = "Switch to Dark Mode";
            }cstOffset
        });
        // Auto-populate datetime-local fields with the current time
        const datetimeFields = document.querySelectorAll('input[type="datetime-local"]');
        const now = new Date();
        //const formattedTime = now.toISOString().slice(0, 16); // Format as YYYY-MM-DDTHH:mm
                
        // Convert to Central Time (UTC - 6:00)
        //const cstOffset = -6; // CST offset from UTC in hours
        const cstOffset = 0; // CST offset from UTC in hours
        const cstTime = new Date(now.getTime() + cstOffset * 60 * 60 * 1000);

        // Format as ISO time (YYYY-MM-DDTHH:mm)
        const year = cstTime.getFullYear();
        const month = String(cstTime.getMonth() + 1).padStart(2, "0");
        const day = String(cstTime.getDate()).padStart(2, "0");
        const hours = String(cstTime.getHours()).padStart(2, "0");
        const minutes = String(cstTime.getMinutes()).padStart(2, "0");
        //const seconds = String(cstTime.getSeconds()).padStart(2, "0");

        //const formattedTime = `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
        const formattedTime = `${year}-${month}-${day}T${hours}:${minutes}`;
        datetimeFields.forEach((field) => {
            field.value = formattedTime;
        });
        },100);
	
});

// Function to handle outfall data submission
async function submitOutfallData(event) {
    event.preventDefault(); // Prevent the default form submission behavior

    // Get form input values
    //const timestampEntry = document.getElementById("timestamp_entry_ISO").value;
    const timestampIntended = document.getElementById("timestamp_intended_ISO").value;
    const safeToObserve = document.getElementById("safe_to_make_observation").value;
    const floatable = document.getElementById("floatable_present").value;
    const scum = document.getElementById("scum_present").value;
    const foam = document.getElementById("foam_present").value;
    const oil = document.getElementById("oil_present").value;
    const operator = document.getElementById("operator").value;

    try {
        // Send POST request to FastAPI
        const response = await fetch(`${BASE_URL}/submit-outfall`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({
                timestamp_intended_ISO: timestampIntended,
                safe_to_make_observation: safeToObserve,
                floatable_present: floatable,
                scum_present: scum,
                foam_present: foam,
                oil_present: oil,
                operator: operator,
            }),
        });

        const result = await response.json();
        if (response.ok) {
            alert("Outfall data submitted successfully!");
        } else {
            alert(`Error: ${result.error || "Failed to submit data"}`);
        }
    } catch (error) {
        console.error("Error submitting outfall data:", error);
        alert("Failed to submit outfall data.");
    }
}

// Function to handle hourly basin and clarifier submission
async function submitHourlyBasinAndClariferSummary(event) {
    event.preventDefault(); // Prevent the default form submission behavior

    // Get form input values
    const timestampIntended = document.getElementById("timestamp_intended_ISO").value;
    const operator = document.getElementById("operator").value;
    const north_basin_1_MGD = document.getElementById("north_basin_1_MGD").value;
    const north_basin_3_MGD = document.getElementById("north_basin_3_MGD").value;
    const north_basin_5_MGD = document.getElementById("north_basin_5_MGD").value;
    const north_basin_7_MGD = document.getElementById("north_basin_7_MGD").value;
    const north_basin_9_MGD = document.getElementById("north_basin_9_MGD").value;
    const north_basin_11_MGD = document.getElementById("north_basin_11_MGD").value;
    const north_basin_13_MGD = document.getElementById("north_basin_13_MGD").value;

    const south_basin_1_MGD = document.getElementById("south_basin_1_MGD").value;
    const south_basin_3_MGD = document.getElementById("south_basin_3_MGD").value;
    const south_basin_5_MGD = document.getElementById("south_basin_5_MGD").value;
    const south_basin_7_MGD = document.getElementById("south_basin_7_MGD").value;
    const south_basin_9_MGD = document.getElementById("south_basin_9_MGD").value;
    const south_basin_11_MGD = document.getElementById("south_basin_11_MGD").value;
    const south_basin_13_MGD = document.getElementById("south_basin_13_MGD").value;

    const north_clarifier_1_MGD = document.getElementById("north_clarifier_1_MGD").value;
    const north_clarifier_2_MGD = document.getElementById("north_clarifier_2_MGD").value;
    const north_clarifier_3_MGD = document.getElementById("north_clarifier_3_MGD").value;
    const north_clarifier_4_MGD = document.getElementById("north_clarifier_4_MGD").value;

    const south_clarifier_1_MGD = document.getElementById("south_clarifier_1_MGD").value;
    const south_clarifier_2_MGD = document.getElementById("south_clarifier_2_MGD").value;
    const south_clarifier_3_MGD = document.getElementById("south_clarifier_3_MGD").value;
    const south_clarifier_4_MGD = document.getElementById("south_clarifier_4_MGD").value;

    const north_ras_1_MGD = document.getElementById("north_ras_1_MGD").value;
    const north_ras_2_MGD = document.getElementById("north_ras_2_MGD").value;
    const north_ras_3_MGD = document.getElementById("north_ras_3_MGD").value;
    const north_ras_4_MGD = document.getElementById("north_ras_4_MGD").value;

    const south_ras_1_MGD = document.getElementById("south_ras_1_MGD").value;
    const south_ras_2_MGD = document.getElementById("south_ras_2_MGD").value;
    const south_ras_3_MGD = document.getElementById("south_ras_3_MGD").value;
    const south_ras_4_MGD = document.getElementById("south_ras_4_MGD").value;

    try {
        // Send POST request to FastAPI
        const response = await fetch(`${BASE_URL}/submit-basin-clarifier-hourly`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({
                timestamp_intended_ISO: timestampIntended,
                operator: operator,
                north_basin_1_MGD:north_basin_1_MGD,
                north_basin_3_MGD:north_basin_3_MGD,
                north_basin_5_MGD:north_basin_5_MGD,
                north_basin_7_MGD:north_basin_7_MGD,
                north_basin_9_MGD:north_basin_9_MGD,
                north_basin_11_MGD:north_basin_11_MGD,
                north_basin_13_MGD:north_basin_13_MGD,

                south_basin_1_MGD:south_basin_1_MGD,
                south_basin_3_MGD:south_basin_3_MGD,
                south_basin_5_MGD:south_basin_5_MGD,
                south_basin_7_MGD:south_basin_7_MGD,
                south_basin_9_MGD:south_basin_9_MGD,
                south_basin_11_MGD:south_basin_11_MGD,
                south_basin_13_MGD:south_basin_13_MGD,

                north_clarifier_1_MGD:north_clarifier_1_MGD,
                north_clarifier_2_MGD:north_clarifier_2_MGD,
                north_clarifier_3_MGD:north_clarifier_3_MGD,
                north_clarifier_4_MGD:north_clarifier_4_MGD,

                south_clarifier_1_MGD:south_clarifier_1_MGD,
                south_clarifier_2_MGD:south_clarifier_2_MGD,
                south_clarifier_3_MGD:south_clarifier_3_MGD,
                south_clarifier_4_MGD:south_clarifier_4_MGD,

                north_ras_1_MGD:north_ras_1_MGD,
                north_ras_2_MGD:north_ras_2_MGD,
                north_ras_3_MGD:north_ras_3_MGD,
                north_ras_4_MGD:north_ras_4_MGD,

                south_ras_1_MGD:south_ras_1_MGD,
                south_ras_2_MGD:south_ras_2_MGD,
                south_ras_3_MGD:south_ras_3_MGD,
                south_ras_4_MGD:south_ras_4_MGD
            }),
        });

        const result = await response.json();
        if (response.ok) {
            alert("Daily summary submitted successfully!");
        } else {
            alert(`Error: ${result.detail || "Failed to submit data"}`);
        }
    } catch (error) {
        console.error("Error submitting daily summary:", error);
        alert("Failed to submit daily summary.");
    }
}


// Attach event listeners to forms and buttons
//document.getElementById("hourlyForm").addEventListener("submit", submitHourlyData);
//document.getElementById("dailyForm").addEventListener("submit", submitDailySummary);
// document.getElementById("listExportsButton").addEventListener("click", listExports);
