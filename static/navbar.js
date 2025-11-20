document.addEventListener("DOMContentLoaded", () => {

  fetch("static/navbar.html")
  .then(res => res.text())
  .then(html => {
    document.getElementById("navbar-container").innerHTML = html;

    const current = window.location.pathname;
    document.querySelectorAll(".nav-link").forEach(link => {
      if (link.getAttribute("href") === current) {
        link.classList.add("active");
      }
    });
      const authButtons = document.getElementById("auth-buttons");
      const userSection = document.getElementById("user-section");
    const token = localStorage.getItem("token");
    if (token) {
       if (authButtons) authButtons.style.display = "none";
       if (userSection) userSection.style.display = "block";
  } 
   document.addEventListener("click", (e) => {
        if (e.target.classList.contains("logout-btn")) {
          localStorage.removeItem("token");
          window.location.href = "/";
        }
      });
  });
});