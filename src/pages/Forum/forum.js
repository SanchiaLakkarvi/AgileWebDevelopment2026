const STORAGE_KEY = "guildspace_forum_posts_v1";
const MAX_UPLOAD_IMAGE_BYTES = 2 * 1024 * 1024;
const ALLOWED_UPLOAD_IMAGE_TYPES = new Set([
  "image/png",
  "image/jpeg",
  "image/webp",
  "image/gif",
  "image/avif",
  "image/bmp"
]);

const defaultPosts = [
  {
    id: 1,
    author: "Mia",
    title: "Best quiet study spots near Reid Library?",
    content: "I need somewhere calm after 6pm. Any hidden places with power sockets?",
    imageUrl: "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?auto=format&fit=crop&w=1200&q=80",
    category: "Study",
    createdAt: "2026-04-19T12:00:00.000Z",
    likes: 9,
    dislikes: 1,
    userReaction: 0,
    comments: [
      {
        id: 101,
        author: "Leo",
        text: "Try the second floor corner in Barry J Marshall. Usually very quiet.",
        createdAt: "2026-04-19T13:30:00.000Z"
      }
    ]
  },
  {
    id: 2,
    author: "Arjun",
    title: "Anyone joining tomorrow's coding club meetup?",
    content: "I am new this semester and would love to meet people before the session starts.",
    imageUrl: "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=1200&q=80",
    category: "Events",
    createdAt: "2026-04-18T08:15:00.000Z",
    likes: 6,
    dislikes: 0,
    userReaction: 0,
    comments: [
      {
        id: 201,
        author: "Nina",
        text: "I will be there around 4:45pm. Happy to grab coffee first!",
        createdAt: "2026-04-18T09:00:00.000Z"
      }
    ]
  },
  {
    id: 3,
    author: "Chloe",
    title: "Affordable lunch options under $10 on campus",
    content: "Trying to cut costs this month. Any places with decent portions?",
    imageUrl: "https://images.unsplash.com/photo-1547573854-74d2a71d0826?auto=format&fit=crop&w=1200&q=80",
    category: "Life",
    createdAt: "2026-04-16T04:30:00.000Z",
    likes: 12,
    dislikes: 2,
    userReaction: 0,
    comments: []
  },
  {
    id: 4,
    author: "Sophie",
    title: "Lost black water bottle near EZONE",
    content: "I left a black Frank Green bottle on level 2 around 2:30pm. Name sticker says Sophie L.",
    imageUrl: "https://images.unsplash.com/photo-1602143407151-cce8c8f6a451?auto=format&fit=crop&w=1200&q=80",
    category: "LostFound",
    createdAt: "2026-04-20T02:05:00.000Z",
    likes: 4,
    dislikes: 0,
    userReaction: 0,
    comments: [
      {
        id: 401,
        author: "Daniel",
        text: "I saw one at the EZONE front desk around 4pm, maybe check there.",
        createdAt: "2026-04-20T03:12:00.000Z"
      }
    ]
  },
  {
    id: 5,
    author: "Noah",
    title: "Data structures study group this Thursday",
    content: "Planning a revision group for CITS2200, Thursday 5pm at Barry J Marshall library.",
    imageUrl: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?auto=format&fit=crop&w=1200&q=80",
    category: "Study",
    createdAt: "2026-04-19T06:00:00.000Z",
    likes: 17,
    dislikes: 1,
    userReaction: 0,
    comments: [
      {
        id: 501,
        author: "Ava",
        text: "Can first years join? I need help with recursion.",
        createdAt: "2026-04-19T07:24:00.000Z"
      }
    ]
  },
  {
    id: 6,
    author: "Liam",
    title: "Any gym buddy for early morning sessions?",
    content: "Trying to stay consistent this semester. Looking for someone for Mon/Wed/Fri 7am sessions.",
    imageUrl: "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=1200&q=80",
    category: "Life",
    createdAt: "2026-04-18T22:10:00.000Z",
    likes: 8,
    dislikes: 0,
    userReaction: 0,
    comments: []
  },
  {
    id: 7,
    author: "Grace",
    title: "Found AirPods case near Business School",
    content: "Found a white AirPods case outside the Business School entrance. Describe sticker to claim.",
    imageUrl: "https://images.unsplash.com/photo-1606220588913-b3aacb4d2f46?auto=format&fit=crop&w=1200&q=80",
    category: "LostFound",
    createdAt: "2026-04-18T02:40:00.000Z",
    likes: 11,
    dislikes: 0,
    userReaction: 0,
    comments: [
      {
        id: 701,
        author: "Ethan",
        text: "Might be mine, does it have a blue cartoon sticker?",
        createdAt: "2026-04-18T03:20:00.000Z"
      }
    ]
  },
  {
    id: 8,
    author: "Isabella",
    title: "Cheapest coffee options around campus?",
    content: "Trying to cap coffee spending this month. Any place under $4 after 2pm?",
    imageUrl: "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=1200&q=80",
    category: "Life",
    createdAt: "2026-04-17T10:25:00.000Z",
    likes: 20,
    dislikes: 2,
    userReaction: 0,
    comments: [
      {
        id: 801,
        author: "Mia",
        text: "Try the small cafe near the law building, they do student discount after 3pm.",
        createdAt: "2026-04-17T11:03:00.000Z"
      }
    ]
  },
  {
    id: 9,
    author: "Benjamin",
    title: "Hackathon team members wanted",
    content: "Building a timetable helper app for the April hackathon. Need one frontend and one backend teammate.",
    imageUrl: "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1200&q=80",
    category: "Events",
    createdAt: "2026-04-17T02:15:00.000Z",
    likes: 14,
    dislikes: 0,
    userReaction: 0,
    comments: []
  },
  {
    id: 10,
    author: "Harper",
    title: "Exam prep tips for CITS2401?",
    content: "I am revising old labs and lecture slides. Any high impact topics to prioritize this week?",
    imageUrl: "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=1200&q=80",
    category: "Study",
    createdAt: "2026-04-16T22:55:00.000Z",
    likes: 10,
    dislikes: 0,
    userReaction: 0,
    comments: [
      {
        id: 1001,
        author: "Arjun",
        text: "Past paper timing practice helped me most last semester.",
        createdAt: "2026-04-16T23:20:00.000Z"
      }
    ]
  },
  {
    id: 11,
    author: "Lucas",
    title: "Board game night at Guild village",
    content: "Hosting a casual board game evening Friday 7pm. Bring your favorite game if you like.",
    imageUrl: "https://images.unsplash.com/photo-1610890716171-6b1bb98ffd09?auto=format&fit=crop&w=1200&q=80",
    category: "Events",
    createdAt: "2026-04-15T09:30:00.000Z",
    likes: 15,
    dislikes: 1,
    userReaction: 0,
    comments: []
  },
  {
    id: 12,
    author: "Ella",
    title: "Found student card near Oak Lawn",
    content: "Found a student card on the path to Oak Lawn. Initials are E.K. I can return it today.",
    imageUrl: "https://images.unsplash.com/photo-1513128034602-7814ccaddd4e?auto=format&fit=crop&w=1200&q=80",
    category: "LostFound",
    createdAt: "2026-04-14T05:45:00.000Z",
    likes: 7,
    dislikes: 0,
    userReaction: 0,
    comments: []
  }
];

let posts = loadPosts();
const expandedComments = new Set();

const postsContainer = document.getElementById("postsContainer");
const forumStats = document.getElementById("forumStats");
const createPostToggle = document.getElementById("createPostToggle");
const createPostContent = document.getElementById("createPostContent");
const createPostForm = document.getElementById("createPostForm");
const createPostError = document.getElementById("createPostError");
const imageFileInput = document.getElementById("imageFileInput");
const imagePickerBtn = document.getElementById("imagePickerBtn");
const clearImageBtn = document.getElementById("clearImageBtn");
const imageFileName = document.getElementById("imageFileName");
const imagePreviewWrap = document.getElementById("imagePreviewWrap");
const imagePreview = document.getElementById("imagePreview");
const searchInput = document.getElementById("searchInput");
const sortSelect = document.getElementById("sortSelect");
const categoryFilter = document.getElementById("categoryFilter");
const sortChips = document.getElementById("sortChips");
const categoryChips = document.getElementById("categoryChips");
let imagePreviewObjectUrl = "";

init();

function init() {
  if (createPostToggle && createPostContent) {
    createPostToggle.addEventListener("click", toggleCreatePanel);
  }

  createPostForm.addEventListener("submit", handleCreatePost);

  if (imagePickerBtn && imageFileInput) {
    imagePickerBtn.addEventListener("click", () => {
      imageFileInput.click();
    });
    imageFileInput.addEventListener("change", handleImageSelection);
  }

  if (clearImageBtn) {
    clearImageBtn.addEventListener("click", clearSelectedImage);
  }

  postsContainer.addEventListener("click", (event) => {
    const likeBtn = event.target.closest("[data-action='like']");
    const dislikeBtn = event.target.closest("[data-action='dislike']");
    const commentToggle = event.target.closest("[data-action='toggle-comments']");

    if (likeBtn) {
      toggleReaction(Number(likeBtn.dataset.postId), "like");
      return;
    }

    if (dislikeBtn) {
      toggleReaction(Number(dislikeBtn.dataset.postId), "dislike");
      return;
    }

    if (commentToggle) {
      toggleComments(Number(commentToggle.dataset.postId));
    }
  });

  postsContainer.addEventListener("submit", (event) => {
    const form = event.target.closest(".comment-form");
    if (!form) {
      return;
    }

    event.preventDefault();
    const postId = Number(form.dataset.postId);
    const input = form.querySelector(".comment-input");
    const text = input.value.trim();

    if (!text) {
      input.focus();
      return;
    }

    addComment(postId, text);
    expandedComments.add(postId);
    form.reset();
  });

  postsContainer.addEventListener("error", (event) => {
    const image = event.target;
    if (!(image instanceof HTMLImageElement)) {
      return;
    }

    if (!image.classList.contains("post-image")) {
      return;
    }

    const fallback = image.dataset.fallback || "";
    const hasRetried = image.dataset.retryFallback === "1";

    if (!hasRetried && fallback && image.src !== fallback) {
      image.dataset.retryFallback = "1";
      image.src = fallback;
      return;
    }

    image.remove();
  }, true);

  searchInput.addEventListener("input", renderPosts);
  sortSelect.addEventListener("change", renderPosts);
  categoryFilter.addEventListener("change", renderPosts);

  sortChips.addEventListener("click", (event) => {
    const button = event.target.closest("[data-sort]");
    if (!button) {
      return;
    }

    sortSelect.value = button.dataset.sort;
    setActiveChip(sortChips, button, "data-sort");
    renderPosts();
  });

  categoryChips.addEventListener("click", (event) => {
    const button = event.target.closest("[data-category]");
    if (!button) {
      return;
    }

    categoryFilter.value = button.dataset.category;
    setActiveChip(categoryChips, button, "data-category");
    renderPosts();
  });

  syncChipsWithFilters();
  renderPosts();
}

function toggleCreatePanel() {
  const isHidden = createPostContent.hidden;
  createPostContent.hidden = !isHidden;
  createPostToggle.setAttribute("aria-expanded", String(isHidden));
  createPostToggle.textContent = isHidden ? "Close Composer" : "Publish Post";
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

function syncChipsWithFilters() {
  const sortActive = sortChips.querySelector(`[data-sort='${sortSelect.value}']`) || sortChips.querySelector("[data-sort='latest']");
  if (sortActive) {
    setActiveChip(sortChips, sortActive, "data-sort");
  }

  const categoryActive = categoryChips.querySelector(`[data-category='${categoryFilter.value}']`) || categoryChips.querySelector("[data-category='all']");
  if (categoryActive) {
    setActiveChip(categoryChips, categoryActive, "data-category");
  }
}

function normalizePost(post) {
  const source = post && typeof post === "object" ? post : {};
  const rawComments = Array.isArray(source.comments) ? source.comments : [];
  const rawCategory = String(source.category || "Life").trim();
  const normalizedCategory = rawCategory === "Marketplace" ? "LostFound" : rawCategory || "Life";

  return {
    id: Number(source.id) || Date.now() + Math.floor(Math.random() * 1000),
    author: String(source.author || "Anonymous").trim() || "Anonymous",
    title: String(source.title || "Untitled Post").trim() || "Untitled Post",
    content: String(source.content || "").trim(),
    imageUrl: normalizeImageUrl(source.imageUrl),
    category: normalizedCategory,
    createdAt: isValidDateString(source.createdAt) ? source.createdAt : new Date().toISOString(),
    likes: Math.max(0, Number(source.likes) || 0),
    dislikes: Math.max(0, Number(source.dislikes) || 0),
    userReaction: Number(source.userReaction) === 1 ? 1 : Number(source.userReaction) === -1 ? -1 : 0,
    comments: rawComments.map((comment) => {
      const commentSource = comment && typeof comment === "object" ? comment : {};
      return {
        id: Number(commentSource.id) || Date.now() + Math.floor(Math.random() * 1000),
        author: String(commentSource.author || "Anonymous").trim() || "Anonymous",
        text: String(commentSource.text || "").trim(),
        createdAt: isValidDateString(commentSource.createdAt) ? commentSource.createdAt : new Date().toISOString()
      };
    })
  };
}

function loadPosts() {
  const seedPosts = structuredClone(defaultPosts).map(normalizePost);

  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      return seedPosts;
    }

    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) {
      return seedPosts;
    }

    const storedPosts = parsed.map(normalizePost);
    const mergedPosts = mergeSeedPosts(storedPosts, seedPosts);

    if (mergedPosts.length !== storedPosts.length) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(mergedPosts));
    }

    return mergedPosts;
  } catch (_error) {
    return seedPosts;
  }
}

function mergeSeedPosts(existingPosts, seedPosts) {
  const existingIds = new Set(existingPosts.map((post) => post.id));
  const missingSeedPosts = seedPosts.filter((post) => !existingIds.has(post.id));
  const merged = [...existingPosts, ...missingSeedPosts];

  return merged.sort((a, b) => {
    return new Date(b.createdAt) - new Date(a.createdAt);
  });
}

function savePosts() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(posts));
    return true;
  } catch (_error) {
    return false;
  }
}

async function handleCreatePost(event) {
  event.preventDefault();
  createPostError.textContent = "";

  const formData = new FormData(createPostForm);
  const author = String(formData.get("author") || "").trim();
  const title = String(formData.get("title") || "").trim();
  const category = String(formData.get("category") || "").trim();
  const content = String(formData.get("content") || "").trim();
  let imageUrl = "";

  if (!author || !title || !category || !content) {
    createPostError.textContent = "Please fill out all fields before publishing.";
    return;
  }

  try {
    imageUrl = await getSelectedImageDataUrl();
  } catch (error) {
    createPostError.textContent = error instanceof Error ? error.message : "Failed to read selected image.";
    return;
  }

  const newPost = {
    id: Date.now(),
    author,
    title,
    category,
    content,
    imageUrl,
    createdAt: new Date().toISOString(),
    likes: 0,
    dislikes: 0,
    userReaction: 0,
    comments: []
  };

  posts.unshift(normalizePost(newPost));
  if (!savePosts()) {
    posts.shift();
    createPostError.textContent = "Storage is full. Please use a smaller photo or remove some old posts.";
    return;
  }
  createPostForm.reset();
  clearSelectedImage();
  createPostContent.hidden = true;
  createPostToggle.setAttribute("aria-expanded", "false");
  createPostToggle.textContent = "Publish Post";
  renderPosts();
}

function handleImageSelection() {
  createPostError.textContent = "";
  const file = getSelectedImageFile();

  if (!file) {
    clearSelectedImageUi();
    return;
  }

  const validationMessage = validateImageFile(file);
  if (validationMessage) {
    createPostError.textContent = validationMessage;
    clearSelectedImage();
    return;
  }

  imageFileName.textContent = file.name;
  clearImageBtn.hidden = false;
  setImagePreviewFromFile(file);
}

function getSelectedImageFile() {
  if (!imageFileInput || !imageFileInput.files || !imageFileInput.files.length) {
    return null;
  }

  return imageFileInput.files[0];
}

function validateImageFile(file) {
  if (!ALLOWED_UPLOAD_IMAGE_TYPES.has(file.type)) {
    return "Please upload PNG, JPG, WEBP, GIF, AVIF, or BMP images.";
  }

  if (file.size > MAX_UPLOAD_IMAGE_BYTES) {
    return "Image is too large. Please keep it under 2MB.";
  }

  return "";
}

function setImagePreviewFromFile(file) {
  if (imagePreviewObjectUrl) {
    URL.revokeObjectURL(imagePreviewObjectUrl);
  }

  imagePreviewObjectUrl = URL.createObjectURL(file);
  imagePreview.src = imagePreviewObjectUrl;
  imagePreviewWrap.hidden = false;
}

function clearSelectedImageUi() {
  if (imagePreviewObjectUrl) {
    URL.revokeObjectURL(imagePreviewObjectUrl);
    imagePreviewObjectUrl = "";
  }

  imageFileName.textContent = "No photo selected";
  clearImageBtn.hidden = true;
  imagePreview.removeAttribute("src");
  imagePreviewWrap.hidden = true;
}

function clearSelectedImage() {
  if (imageFileInput) {
    imageFileInput.value = "";
  }
  clearSelectedImageUi();
}

async function getSelectedImageDataUrl() {
  const file = getSelectedImageFile();
  if (!file) {
    return "";
  }

  const validationMessage = validateImageFile(file);
  if (validationMessage) {
    throw new Error(validationMessage);
  }

  const dataUrl = await readFileAsDataUrl(file);
  const normalized = normalizeImageUrl(dataUrl);
  if (!normalized) {
    throw new Error("Unsupported image format. Please try another photo.");
  }
  return normalized;
}

function readFileAsDataUrl(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result || ""));
    reader.onerror = () => reject(new Error("Failed to read selected image."));
    reader.readAsDataURL(file);
  });
}

function toggleReaction(postId, action) {
  posts = posts.map((post) => {
    if (post.id !== postId) {
      return post;
    }

    const next = { ...post };
    const current = Number(next.userReaction || 0);

    if (action === "like") {
      if (current === 1) {
        next.likes = Math.max(0, next.likes - 1);
        next.userReaction = 0;
      } else if (current === -1) {
        next.dislikes = Math.max(0, next.dislikes - 1);
        next.likes += 1;
        next.userReaction = 1;
      } else {
        next.likes += 1;
        next.userReaction = 1;
      }
    }

    if (action === "dislike") {
      if (current === -1) {
        next.dislikes = Math.max(0, next.dislikes - 1);
        next.userReaction = 0;
      } else if (current === 1) {
        next.likes = Math.max(0, next.likes - 1);
        next.dislikes += 1;
        next.userReaction = -1;
      } else {
        next.dislikes += 1;
        next.userReaction = -1;
      }
    }

    return next;
  });

  savePosts();
  renderPosts();
}

function toggleComments(postId) {
  if (expandedComments.has(postId)) {
    expandedComments.delete(postId);
  } else {
    expandedComments.add(postId);
  }
  renderPosts();
}

function addComment(postId, text) {
  posts = posts.map((post) => {
    if (post.id !== postId) {
      return post;
    }

    const comments = Array.isArray(post.comments) ? [...post.comments] : [];
    comments.push({
      id: Date.now(),
      author: "You",
      text,
      createdAt: new Date().toISOString()
    });

    return {
      ...post,
      comments
    };
  });

  savePosts();
  renderPosts();
}

function getVisiblePosts() {
  const keyword = searchInput.value.trim().toLowerCase();
  const category = categoryFilter.value;
  const sortBy = sortSelect.value;

  let visible = posts.filter((post) => {
    const matchCategory = category === "all" || post.category === category;
    if (!matchCategory) {
      return false;
    }

    if (!keyword) {
      return true;
    }

    const sourceText = [
      post.title,
      post.content,
      post.author,
      post.category,
      ...(post.comments || []).map((comment) => comment.text)
    ]
      .join(" ")
      .toLowerCase();

    return sourceText.includes(keyword);
  });

  visible = visible.sort((a, b) => {
    if (sortBy === "oldest") {
      return new Date(a.createdAt) - new Date(b.createdAt);
    }

    if (sortBy === "popular") {
      const scoreA = (a.likes || 0) - (a.dislikes || 0);
      const scoreB = (b.likes || 0) - (b.dislikes || 0);
      if (scoreB !== scoreA) {
        return scoreB - scoreA;
      }
    }

    return new Date(b.createdAt) - new Date(a.createdAt);
  });

  return visible;
}

function renderPosts() {
  const visiblePosts = getVisiblePosts();

  const totalComments = visiblePosts.reduce((sum, post) => {
    return sum + (Array.isArray(post.comments) ? post.comments.length : 0);
  }, 0);

  forumStats.textContent = `${visiblePosts.length} posts | ${totalComments} comments`;

  if (!visiblePosts.length) {
    postsContainer.innerHTML = `
      <div class="empty-state alert alert-light border text-secondary mb-0" role="status">
        <div class="fw-semibold mb-1">No matching posts yet.</div>
        <div>Try another keyword or publish a new question.</div>
      </div>
    `;
    return;
  }

  postsContainer.innerHTML = visiblePosts.map(renderPostCard).join("");
}

function renderPostCard(post) {
  const comments = Array.isArray(post.comments) ? post.comments : [];
  const userReaction = Number(post.userReaction || 0);
  const commentsOpen = expandedComments.has(post.id);
  const likeClass = userReaction === 1 ? "btn-success active" : "btn-outline-success";
  const dislikeClass = userReaction === -1 ? "btn-danger active" : "btn-outline-danger";
  const commentClass = commentsOpen ? "btn-primary active" : "btn-outline-primary";

  const commentsMarkup = comments.length
    ? comments
        .map((comment) => {
          return `
            <li class="list-group-item px-0">
              <div class="small text-secondary mb-1">${escapeHTML(comment.author)} | ${formatRelativeTime(comment.createdAt)}</div>
              <p class="mb-0">${escapeHTML(comment.text)}</p>
            </li>
          `;
        })
        .join("")
    : `
      <li class="list-group-item px-0">
        <div class="small text-secondary mb-1">No comments yet</div>
        <p class="mb-0">Be the first to add a helpful reply.</p>
      </li>
    `;

  return `
    <div class="post-item">
    <article class="card border-0 shadow-sm">
      <img
        class="card-img-top post-image"
        src="${escapeHTML(post.imageUrl || fallbackImage(post.category))}"
        data-fallback="${escapeHTML(fallbackImage(post.category))}"
        alt="Post image for ${escapeHTML(post.title)}"
        loading="lazy"
      />

      <div class="card-body d-flex flex-column">
        <div class="d-flex justify-content-between align-items-start gap-2 mb-2">
          <div class="d-flex align-items-center gap-2 flex-grow-1">
            <div class="post-avatar rounded-circle bg-primary-subtle text-primary fw-bold d-flex align-items-center justify-content-center" aria-hidden="true">${escapeHTML(getInitial(post.author))}</div>
            <div>
              <div class="fw-semibold small text-truncate">${escapeHTML(post.author)}</div>
              <div class="small text-secondary">${formatRelativeTime(post.createdAt)}</div>
            </div>
          </div>
          <span class="badge rounded-pill text-bg-light border">${escapeHTML(getCategoryLabel(post.category))}</span>
        </div>

        <h3 class="h5 mb-2">${escapeHTML(post.title)}</h3>
        <p class="text-secondary post-content mb-3">${escapeHTML(post.content)}</p>

        <div class="row g-2 mt-auto">
          <div class="col-4 d-grid">
            <button
              type="button"
              class="btn btn-sm ${likeClass}"
              data-action="like"
              data-post-id="${post.id}"
              aria-label="Like post"
            >
              Like ${post.likes || 0}
            </button>
          </div>

          <div class="col-4 d-grid">
            <button
              type="button"
              class="btn btn-sm ${dislikeClass}"
              data-action="dislike"
              data-post-id="${post.id}"
              aria-label="Dislike post"
            >
              Dislike ${post.dislikes || 0}
            </button>
          </div>

          <div class="col-4 d-grid">
            <button
              type="button"
              class="btn btn-sm ${commentClass}"
              data-action="toggle-comments"
              data-post-id="${post.id}"
              aria-expanded="${commentsOpen ? "true" : "false"}"
            >
              ${commentsOpen ? "Hide" : "Comments"} ${comments.length}
            </button>
          </div>
        </div>

        <div class="mt-3 pt-3 border-top" ${commentsOpen ? "" : "hidden"}>
          <ul class="list-group list-group-flush mb-3">${commentsMarkup}</ul>
          <form class="comment-form" data-post-id="${post.id}">
            <div class="input-group input-group-sm">
              <input
                class="form-control comment-input"
                name="comment"
                type="text"
                maxlength="240"
                placeholder="Write a comment..."
                aria-label="Write a comment"
                required
              />
              <button type="submit" class="btn btn-primary">Comment</button>
            </div>
          </form>
        </div>
      </div>
    </article>
    </div>
  `;
}

function fallbackImage(category) {
  const map = {
    Study: "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=1200&q=80",
    Events: "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=1200&q=80",
    Life: "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?auto=format&fit=crop&w=1200&q=80",
    LostFound: "https://images.unsplash.com/photo-1595152772835-219674b2a8a6?auto=format&fit=crop&w=1200&q=80"
  };

  return map[category] || map.Life;
}

function getCategoryLabel(category) {
  return category === "LostFound" ? "Lost & Found" : category;
}

function normalizeImageUrl(value) {
  const urlText = String(value || "").trim();
  if (!urlText) {
    return "";
  }

  if (isAllowedDataImageUrl(urlText)) {
    return urlText;
  }

  try {
    const url = new URL(urlText);
    if (url.protocol !== "http:" && url.protocol !== "https:") {
      return "";
    }
    return url.href;
  } catch (_error) {
    return "";
  }
}

function isAllowedDataImageUrl(urlText) {
  if (!urlText.startsWith("data:image/")) {
    return false;
  }

  const commaIndex = urlText.indexOf(",");
  if (commaIndex < 0) {
    return false;
  }

  const header = urlText.slice(0, commaIndex).toLowerCase();
  return header === "data:image/png;base64" ||
    header === "data:image/jpeg;base64" ||
    header === "data:image/jpg;base64" ||
    header === "data:image/webp;base64" ||
    header === "data:image/gif;base64" ||
    header === "data:image/avif;base64" ||
    header === "data:image/bmp;base64";
}

function isValidDateString(value) {
  return !Number.isNaN(new Date(value).getTime());
}

function getInitial(name) {
  const text = String(name || "?").trim();
  return text ? text.charAt(0).toUpperCase() : "?";
}

function formatRelativeTime(isoDate) {
  const date = new Date(isoDate);
  const diffMs = Date.now() - date.getTime();

  if (Number.isNaN(diffMs)) {
    return "just now";
  }

  const minute = 60 * 1000;
  const hour = 60 * minute;
  const day = 24 * hour;

  if (diffMs < minute) {
    return "just now";
  }

  if (diffMs < hour) {
    return `${Math.floor(diffMs / minute)}m ago`;
  }

  if (diffMs < day) {
    return `${Math.floor(diffMs / hour)}h ago`;
  }

  if (diffMs < day * 7) {
    return `${Math.floor(diffMs / day)}d ago`;
  }

  return date.toLocaleDateString("en-AU", {
    year: "numeric",
    month: "short",
    day: "numeric"
  });
}

function escapeHTML(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;")
    .replace(/'/g, "&#39;");
}
