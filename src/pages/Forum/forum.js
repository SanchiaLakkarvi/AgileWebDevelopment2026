(function initForumUi() {
  const postsContainer = document.getElementById("postsContainer");
  const forumStats = document.getElementById("forumStats");
  const sortChips = document.getElementById("sortChips");
  const categoryChips = document.getElementById("categoryChips");

  if (!postsContainer || !forumStats || !sortChips || !categoryChips) {
    return;
  }

  let sortBy = "latest";
  let category = "all";
  let resizeTimer = 0;

  function getCards() {
    return Array.from(postsContainer.querySelectorAll(".post-item"));
  }

  function getColumnCount() {
    if (window.matchMedia("(max-width: 575.98px)").matches) {
      return 1;
    }
    if (window.matchMedia("(max-width: 991.98px)").matches) {
      return 2;
    }
    return 3;
  }

  function ensureColumns(columnCount) {
    let columns = Array.from(postsContainer.querySelectorAll(".posts-column"));
    if (columns.length === columnCount) {
      return columns;
    }

    const cards = getCards();
    postsContainer.innerHTML = "";
    columns = [];

    for (let i = 0; i < columnCount; i += 1) {
      const col = document.createElement("div");
      col.className = "posts-column";
      col.dataset.col = String(i);
      postsContainer.appendChild(col);
      columns.push(col);
    }

    cards.forEach((card, index) => {
      columns[index % columnCount].appendChild(card);
    });

    return columns;
  }

  function layoutCards(visibleCards, hiddenCards) {
    const columnCount = getColumnCount();
    const columns = ensureColumns(columnCount);
    columns.forEach((col) => {
      col.innerHTML = "";
    });

    visibleCards.forEach((card, index) => {
      columns[index % columnCount].appendChild(card);
    });

    hiddenCards.forEach((card) => {
      columns[0].appendChild(card);
    });
  }

  function setActiveChip(group, activeButton, attrName) {
    const selector = `[${attrName}]`;
    group.querySelectorAll(selector).forEach((button) => {
      const isActive = button === activeButton;
      button.classList.toggle("active", isActive);
      button.classList.toggle("btn-primary", isActive);
      button.classList.toggle("btn-outline-secondary", !isActive);
    });
  }

  function applyFiltersAndSort() {
    const cards = getCards();
    if (!cards.length) {
      forumStats.textContent = "0 posts | 0 comments";
      return;
    }

    cards.forEach((card) => {
      const cardCategory = String(card.dataset.category || "");
      const matchesCategory = category === "all" || cardCategory === category;
      card.hidden = !matchesCategory;
    });

    const visibleCards = cards.filter((card) => !card.hidden);
    visibleCards.sort((a, b) => {
      const aTime = Number(a.dataset.createdAtTs || 0);
      const bTime = Number(b.dataset.createdAtTs || 0);

      if (sortBy === "oldest") {
        return aTime - bTime;
      }

      if (sortBy === "popular") {
        const aScore = Number(a.dataset.score || 0);
        const bScore = Number(b.dataset.score || 0);
        if (bScore !== aScore) {
          return bScore - aScore;
        }
      }

      return bTime - aTime;
    });

    const hiddenCards = cards.filter((card) => card.hidden);
    layoutCards(visibleCards, hiddenCards);

    const totalComments = visibleCards.reduce((sum, card) => {
      return sum + Number(card.dataset.comments || 0);
    }, 0);

    forumStats.textContent = `${visibleCards.length} posts | ${totalComments} comments`;
  }

  sortChips.addEventListener("click", (event) => {
    const button = event.target.closest("[data-sort]");
    if (!button) {
      return;
    }

    sortBy = String(button.dataset.sort || "latest");
    setActiveChip(sortChips, button, "data-sort");
    applyFiltersAndSort();
  });

  categoryChips.addEventListener("click", (event) => {
    const button = event.target.closest("[data-category]");
    if (!button) {
      return;
    }

    category = String(button.dataset.category || "all");
    setActiveChip(categoryChips, button, "data-category");
    applyFiltersAndSort();
  });

  postsContainer.addEventListener("click", (event) => {
    const button = event.target.closest("[data-action='toggle-comments']");
    if (!button) {
      return;
    }

    const postId = Number(button.dataset.postId || 0);
    if (!postId) {
      return;
    }

    const panel = document.getElementById(`comments-${postId}`);
    if (!panel) {
      return;
    }

    if (!button.dataset.defaultLabel) {
      button.dataset.defaultLabel = button.innerHTML;
    }

    const isHidden = panel.hasAttribute("hidden");
    if (isHidden) {
      panel.removeAttribute("hidden");
      button.setAttribute("aria-expanded", "true");
      button.classList.remove("btn-outline-primary");
      button.classList.add("btn-primary", "active");
      button.textContent = "Hide";
      return;
    }

    panel.setAttribute("hidden", "hidden");
    button.setAttribute("aria-expanded", "false");
    button.classList.remove("btn-primary", "active");
    button.classList.add("btn-outline-primary");
    button.innerHTML = button.dataset.defaultLabel;
  });

  window.addEventListener("resize", () => {
    window.clearTimeout(resizeTimer);
    resizeTimer = window.setTimeout(() => {
      applyFiltersAndSort();
    }, 120);
  });

  applyFiltersAndSort();
})();
