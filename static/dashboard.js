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
    const res = await fetch("/api/dashboard/data", {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    totalEl.textContent = data.total;
    fakeEl.textContent = data.fake;
    realEl.textContent = data.real;
    accEl.textContent = data.avg_confidence + "%";

    console.log(" Dashboard data:", data);
  } catch (err) {
    console.error(" Failed to load dashboard data:", err);
  }
});
