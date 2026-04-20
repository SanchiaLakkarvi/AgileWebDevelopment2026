(function mountNavbar() {
  const slot = document.querySelector("[data-navbar]");
  if (!slot) {
    return;
  }

  const active = String(slot.dataset.active || "").toLowerCase();
  const base = String(slot.dataset.base || "../");
  const collapseId = String(slot.dataset.collapseId || "appNavbarMenu");

  const links = [
    { key: "home", label: "Home", href: `${base}Homepage/homepage.html` },
    { key: "forum", label: "Forum", href: `${base}Forum/forum.html` },
    {
      key: "marketplace",
      label: "Marketplace",
      href: `${base}Marketplace/marketplace.html`,
    },
    { key: "login", label: "Login", href: `${base}Login/login.html` },
  ];

  const navItems = links
    .map((link) => {
      const isActive = active === link.key;
      return `
        <li class="nav-item">
          <a class="nav-link${isActive ? " active" : ""}" ${isActive ? 'aria-current="page"' : ""} href="${link.href}">${link.label}</a>
        </li>
      `;
    })
    .join("");

  slot.innerHTML = `
    <nav class="navbar navbar-expand-lg navbar-dark app-navbar shadow-sm">
      <div class="container">
        <a class="navbar-brand fw-bold" href="${base}Homepage/homepage.html">GuildSpace</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#${collapseId}"
          aria-controls="${collapseId}" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="${collapseId}">
          <ul class="navbar-nav ms-auto">
            ${navItems}
          </ul>
        </div>
      </div>
    </nav>
  `;
})();
