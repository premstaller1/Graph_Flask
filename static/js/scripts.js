document.getElementById("fetch-data").addEventListener("click", async () => {
    const profile = document.getElementById("profile").value;
    const metrics = document.getElementById("metrics").value;

    const response = await fetch("/fetch-metrics", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ profile, metrics })
    });

    const data = await response.json();
    document.getElementById("results").innerText = JSON.stringify(data, null, 2);
});
