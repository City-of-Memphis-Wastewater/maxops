// Set default timestamp to the current time
window.addEventListener("DOMContentLoaded", () => {
    const timestampInput = document.getElementById("timestamp");

    // Get the current time in the "YYYY-MM-DDTHH:mm" format
    const now = new Date();
    const formattedTime = now.toISOString().slice(0, 16); // Format to "YYYY-MM-DDTHH:mm"
    
    // Set the default value of the timestamp input
    timestampInput.value = formattedTime;
});
