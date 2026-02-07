// Live search suggestions + genre selection + recommendations fetch

document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("searchInput");
  const suggestions = document.getElementById("suggestions");
  const submitBtn = document.getElementById("submitBtn");
  const genreContainer = document.getElementById("genreContainer");
  const recommendations = document.getElementById("recommendations");
  const noResultsMsg = document.getElementById("noResultsMsg");

  // simple debounce
  function debounce(fn, delay = 220) {
    let t;
    return (...args) => {
      clearTimeout(t);
      t = setTimeout(() => fn(...args), delay);
    };
  }

  // perform search query
  const doSearch = debounce(async function (q) {
    if (!q) {
      suggestions.classList.add("hidden");
      suggestions.innerHTML = "";
      return;
    }
    try {
      const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
      const items = await res.json();
      if (!items || items.length === 0) {
        suggestions.innerHTML = `<div class="p-3 text-sm text-gray-500">No results</div>`;
      } else {
        suggestions.innerHTML = items.map(it => {
          return `<div class="suggestion-item border-b border-gray-100" data-id="${it.movie_id}">${it.title}</div>`;
        }).join("");
      }
      suggestions.classList.remove("hidden");
    } catch (e) {
      console.error(e);
    }
  }, 180);

  searchInput.addEventListener("input", (e) => {
    const q = e.target.value.trim();
    doSearch(q);
  });

  // click on suggestion -> open movie details by injecting into recommendation area
  suggestions.addEventListener("click", async (e) => {
    const item = e.target.closest(".suggestion-item");
    if (!item) return;
    const movieId = item.dataset.id;
    suggestions.classList.add("hidden");
    searchInput.value = item.innerText;
    // fetch details
    try {
      const res = await fetch(`/api/movie/${movieId}`);
      if (!res.ok) return;
      const detail = await res.json();
      renderSingleMovie(detail);
    } catch (err) {
      console.error(err);
    }
  });

  document.addEventListener("click", (e) => {
    if (!e.target.closest("#suggestions") && e.target !== searchInput) {
      suggestions.classList.add("hidden");
    }
  });

  // genre chips toggle
  genreContainer.addEventListener("click", (e) => {
    const btn = e.target.closest(".genre-chip");
    if (!btn) return;
    btn.classList.toggle("active");
    const checkbox = btn.querySelector("input[type='checkbox']");
    if (checkbox) checkbox.checked = !checkbox.checked;
  });

  // submit -> gather selected genres and call /api/recommend
  submitBtn.addEventListener("click", async () => {
    const selected = Array.from(genreContainer.querySelectorAll(".genre-chip.active"))
      .map(b => b.dataset.genre)
      .filter(Boolean);

    // fetch recommendations (POST)
    try {
      const res = await fetch("/api/recommend", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({genres: selected})
      });
      const recs = await res.json();
      renderRecommendations(recs);
    } catch (err) {
      console.error(err);
    }
  });

  function renderSingleMovie(m) {
    noResultsMsg.style.display = "none";
    recommendations.innerHTML = `
      <div class="p-4 bg-white rounded-xl border border-gray-100 shadow-sm flex gap-4">
        <div class="w-12 flex items-start">
          <div class="text-3xl">🎬</div>
        </div>
        <div>
          <h3 class="text-lg font-semibold">${escapeHtml(m.title)}</h3>
          <div class="text-sm text-orange-500 mt-1">Genres: ${escapeHtml((m.predicted_genres||[]).join(", "))}</div>
          <div class="mt-2 text-gray-700">${escapeHtml(m.summary||"No summary available.")}</div>
          ${m.score ? `<div class="mt-3 text-sm text-gray-600">Score: ${escapeHtml(String(m.score))}</div>` : ''}
        </div>
      </div>
    `;
  }

  function renderRecommendations(list) {
    if (!list || list.length === 0) {
      noResultsMsg.style.display = "block";
      recommendations.innerHTML = "";
      return;
    }
    noResultsMsg.style.display = "none";
    recommendations.innerHTML = list.map(item => {
      const genres = (item.predicted_genres || []).join(", ");
      const score = item.score ? `<span class="text-yellow-500 font-semibold">★ ${item.score}/5</span>` : "";
      return `
        <div class="p-4 bg-white rounded-xl border border-gray-100 shadow-sm flex gap-4">
          <div class="w-12 flex items-start">
            <div class="text-3xl">🎬</div>
          </div>
          <div>
            <h3 class="text-lg font-semibold">${escapeHtml(item.title)}</h3>
            <div class="text-sm text-gray-500 mt-1">${escapeHtml(genres)}</div>
            <div class="mt-2 text-gray-700">${escapeHtml(item.summary || "")}</div>
            <div class="mt-3">${score}</div>
          </div>
        </div>
      `;
    }).join("");
  }

  // quick HTML escape
  function escapeHtml(str) {
    if (!str && str !== 0) return "";
    return String(str)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  // optionally, load default top-k to show a starter set
  async function loadDefaultRecs() {
    try {
      const res = await fetch("/api/recommend");
      const recs = await res.json();
      if (Array.isArray(recs) && recs.length > 0) {
        renderRecommendations(recs.slice(0, 6));
      }
    } catch (e) {
      console.warn("Couldn't load default recommendations", e);
    }
  }

  loadDefaultRecs();
});
