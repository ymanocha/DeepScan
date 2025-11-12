document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");
  const tableBody = document.getElementById("history-body");
  const noData = document.getElementById("no-data");

  if (!token) {
    alert("Please login to view your scan history");
    window.location.href = "/login";
    return;
  }

  async function loadHistory() {
    try {
      const res = await fetch("/api/history", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) throw new Error(`Failed: ${res.status}`);
      const scans = await res.json();

      if (!Array.isArray(scans) || !scans.length) {
        noData.style.display = "block";
        tableBody.innerHTML = "";
        return;
      }

      noData.style.display = "none";
      tableBody.innerHTML = "";

      scans.forEach((scan) => {
        const row = document.createElement("tr");
        row.innerHTML = `
        <td>${new Date(scan.created_at).toLocaleString()}</td>
          <td>${scan.video_name}</td>
          <td>${scan.result}</td>
          <td>${scan.confidence ? scan.confidence.toFixed(2) + "%" : "N/A"}</td>
          <td>
            <button class="btn view" data-lime="${scan.lime_image || ""}">View</button>
            <button class="btn delete" data-id="${scan.id}">Delete</button>
          </td>
        `;
        tableBody.appendChild(row);
      });
    } catch (err) {
      console.error("⚠️ Error loading history:", err);
    }
  }

  document.addEventListener("click", async (e) => {
    if (e.target.classList.contains("view-btn")) {
      const lime = e.target.dataset.lime;
      if (!lime) return alert("No image available for this scan.");
      window.open(lime, "_blank");
    }

    if (e.target.classList.contains("delete-btn")) {
      const id = e.target.dataset.id;
      if (!confirm("Are you sure you want to delete this scan?")) return;

      try {
        const res = await fetch(`/api/history/${id}`, {
          method: "DELETE",
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) throw new Error(`Delete failed: ${res.status}`);
        loadHistory();
      } catch (err) {
        console.error("⚠️ Error deleting scan:", err);
      }
    }
  });

  loadHistory();
});
