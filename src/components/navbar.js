(function mountNavbar() {
  const slot = document.querySelector("[data-navbar]");
  if (!slot) {
    return;
  }

  const active = String(slot.dataset.active || "").toLowerCase();
  const collapseId = "appNavbarMenu";
  const isStaticPreview = window.location.port === "5500";
  const path = window.location.pathname.toLowerCase();
  const isAuthPage =
    active === "login" ||
    active === "register" ||
    path.includes("/login") ||
    path.includes("/register");

  const links = isStaticPreview
    ? [
        { key: "home", label: "Home", href: "/src/pages/Homepage/homepage.html" },
        { key: "forum", label: "Forum", href: "/src/pages/Forum/forum.html" },
        {
          key: "marketplace",
          label: "Marketplace",
          href: "/src/pages/Marketplace/marketplace.html",
        },
        { key: "login", label: "Login", href: "/src/pages/Login/login.html" },
      ]
    : [
        { key: "home", label: "Home", href: "/" },
        { key: "forum", label: "Forum", href: "/forum" },
        {
          key: "marketplace",
          label: "Marketplace",
          href: "/marketplace",
        },
        { key: "login", label: "Login", href: "/login" },
      ];

  const homeHref = links.find((link) => link.key === "home")?.href || "/";

  const navItems = isAuthPage
    ? ""
    : links
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
        <a class="navbar-brand fw-bold" href="${homeHref}">GuildSpace</a>
        ${
          isAuthPage
            ? ""
            : `
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#${collapseId}"
          aria-controls="${collapseId}" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="${collapseId}">
          <ul class="navbar-nav ms-auto">
            ${navItems}
          </ul>
        </div>
        `
        }
      </div>
    </nav>
  `;
})();
