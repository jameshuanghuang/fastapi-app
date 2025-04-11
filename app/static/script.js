const ws = new WebSocket(`${window.location.protocol === "https:" ? "wss" : "ws"}://${window.location.host}/ws`);
const form = document.getElementById("optionsForm");
const resultDiv = document.getElementById("result");
const samplePaths = document.getElementById("samplePaths");
const calculator = document.querySelector(".calculator");
const results = document.querySelector(".results");

document.getElementById("calculateButton").addEventListener("click", () => {
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    data.S0 = parseFloat(data.S0);
    data.K = parseFloat(data.K);
    data.rfr = parseFloat(data.rfr);
    data.sigma = parseFloat(data.sigma);
    data.T = parseFloat(data.T);
    data.q1 = parseFloat(data.q1);

    ws.send(JSON.stringify(data));

    // Trigger animation to show both result and table
    calculator.classList.add("active");
    results.classList.add("active");
});

ws.onmessage = (event) => {
    const response = JSON.parse(event.data);

    if (response.type === "error") {
        // Display validation errors
        alert(`Error: ${response.message}\nDetails: ${JSON.stringify(response.details)}`);
    } else if (response.type === "result") {
        // Display the result
        resultDiv.textContent = response.message;
        renderTable(response.data);
    }
};

function renderTable(data) {
    samplePaths.innerHTML = ""; // Clear existing table content

    // Create table headers
    const headers = Object.keys(data[0]);
    const headerRow = document.createElement("tr");
    headers.forEach(header => {
        const th = document.createElement("th");
        th.textContent = header;
        headerRow.appendChild(th);
    });
    samplePaths.appendChild(headerRow);

    // Create table rows
    data.forEach(row => {
        const tr = document.createElement("tr");
        headers.forEach(header => {
            const td = document.createElement("td");
            td.textContent = row[header];
            tr.appendChild(td);
        });
        samplePaths.appendChild(tr);
    });

    // Show the download button
    const downloadButton = document.getElementById("downloadButton");
    downloadButton.classList.remove("hidden");

    // Attach click event to download the table as CSV
    downloadButton.addEventListener("click", () => downloadCSV(data));
}

function downloadCSV(data) {
    const headers = Object.keys(data[0]);
    const rows = data.map(row => headers.map(header => row[header]).join(","));
    const csvContent = [headers.join(","), ...rows].join("\n");

    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "sample_paths.csv";
    a.click();

    URL.revokeObjectURL(url);
}