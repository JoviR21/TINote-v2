(function () {
  const root = document.documentElement;
  const saved = localStorage.getItem("tinote-theme");
  if (saved === "dark" || saved === "light") root.setAttribute("data-theme", saved);
  const btn = document.getElementById("themeToggle");
  if (btn) btn.addEventListener("click", () => {
    const cur = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", cur);
    localStorage.setItem("tinote-theme", cur);
  });
})();
