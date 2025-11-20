document.addEventListener("DOMContentLoaded", async () => {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Please log in to view your dashboard.");
    window.location.href = "/login";
    return;
  }
  
  const totalEl = document.getElementById("total-videos");
  const fakeEl = document.getElementById("fake-count");
  const realEl = document.getElementById("real-count");
  const accEl = document.getElementById("accuracy");

  try {
    const res = await fetch("/api/scans/dashboard/data", {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    totalEl.textContent = data.total;
    fakeEl.textContent = data.fake;
    realEl.textContent = data.real;
    accEl.textContent = data.avg_confidence + "%";

    console.log(" Dashboard data:", data);

    const pieCtx = document.getElementById("pieChart").getContext("2d");
    new Chart(pieCtx, {
      type: "pie",
      data: {
        labels: ["Fake", "Real"],
        datasets: [
          {
            data: [data.fake, data.real],
            backgroundColor: ["#ef4444", "#22c55e"],
          },
        ],
      },
    });

    const lineCtx = document.getElementById("lineChart").getContext("2d");
    
      const dates = data.history.map(item =>
      new Date(item.date).toLocaleDateString()
    );

    const counts = data.history.map(item => item.count);

    new Chart(lineCtx, {
      type: "line",
      data: {
        labels: dates,
        datasets: [
          {
            label: "Videos Analyzed",
            data: counts,
            borderColor: "#3b82f6",
            backgroundColor: "rgba(59,130,246,0.3)",
            tension: 0.2,
            borderWidth: 2,
          },
        ],
      },
    });

  } catch (err) {
    console.error(" Failed to load dashboard data:", err);
  }
});
