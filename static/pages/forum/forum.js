(function initForumPage() {
  const postsContainer = document.getElementById("postsContainer");
  const forumStats = document.getElementById("forumStats");
  const sortChips = document.getElementById("sortChips");
  const categoryChips = document.getElementById("categoryChips");

  if (!postsContainer || !forumStats || !sortChips || !categoryChips) {
    return;
  }

  let currentSort = "latest";
  let currentCategory = "all";

  function getPostCards() {
    return Array.from(postsContainer.querySelectorAll(".post-item"));
  }

  function setActiveButton(group, activeButton, dataName) {
    group.querySelectorAll(`[${dataName}]`).forEach((button) => {
      button.classList.toggle("active", button === activeButton);
    });
  }

  function updateStats(visibleCards) {
    const commentTotal = visibleCards.reduce((total, card) => {
      return total + Number(card.dataset.comments || 0);
    }, 0);

    forumStats.textContent = `${visibleCards.length} posts | ${commentTotal} comments`;
  }

  function applyFilterAndSort() {
    const cards = getPostCards();

    if (!cards.length) {
      forumStats.textContent = "0 posts | 0 comments";
      return;
    }

    const visibleCards = cards.filter((card) => {
      const category = String(card.dataset.category || "");
      return currentCategory === "all" || category === currentCategory;
    });

    visibleCards.sort((a, b) => {
      const aTime = Number(a.dataset.createdAtTs || 0);
      const bTime = Number(b.dataset.createdAtTs || 0);
      const aScore = Number(a.dataset.score || 0);
      const bScore = Number(b.dataset.score || 0);

      if (currentSort === "oldest") {
        return aTime - bTime;
      }

      if (currentSort === "popular") {
        if (bScore !== aScore) {
          return bScore - aScore;
        }
        return bTime - aTime;
      }

      return bTime - aTime;
    });

    cards.forEach((card) => {
      card.hidden = true;
    });

    visibleCards.forEach((card) => {
      card.hidden = false;
      postsContainer.appendChild(card);
    });

    updateStats(visibleCards);
  }

  sortChips.addEventListener("click", (event) => {
    const button = event.target.closest("[data-sort]");
    if (!button) return;

    currentSort = button.dataset.sort || "latest";
    setActiveButton(sortChips, button, "data-sort");
    applyFilterAndSort();
  });

  categoryChips.addEventListener("click", (event) => {
    const button = event.target.closest("[data-category]");
    if (!button) return;

    currentCategory = button.dataset.category || "all";
    setActiveButton(categoryChips, button, "data-category");
    applyFilterAndSort();
  });

  postsContainer.addEventListener("click", (event) => {
    const button = event.target.closest("[data-action='toggle-comments']");
    if (!button) return;

    const postId = button.dataset.postId;
    const commentsPanel = document.getElementById(`comments-${postId}`);

    if (!commentsPanel) return;

    const isHidden = commentsPanel.hasAttribute("hidden");

    if (isHidden) {
      commentsPanel.removeAttribute("hidden");
      button.classList.add("active");
      button.setAttribute("aria-expanded", "true");
    } else {
      commentsPanel.setAttribute("hidden", "hidden");
      button.classList.remove("active");
      button.setAttribute("aria-expanded", "false");
    }
  });

  applyFilterAndSort();
})();
