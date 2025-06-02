document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("city");
  const suggestions = document.getElementById("suggestions");
  let abortController = null;
  let lastRequestTime = 0;
  const DEBOUNCE_DELAY = 300;

  input.addEventListener("input", function () {
    const query = input.value.trim();

    if (query.length < 2) {
      suggestions.style.display = "none";
      return;
    }

    if (abortController) {
      abortController.abort();
    }

    const now = Date.now();
    if (now - lastRequestTime < DEBOUNCE_DELAY) {
      return;
    }
    lastRequestTime = now;

    abortController = new AbortController();

    fetch(`/api/autocomplete?q=${encodeURIComponent(query)}`, {
      signal: abortController.signal,
    })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return res.json();
      })
      .then((data) => {
        suggestions.innerHTML = "";

        if (data.length === 0) {
          const noResults = document.createElement("div");
          noResults.className = "no-results";
          noResults.textContent = "Ничего не найдено";
          suggestions.appendChild(noResults);
        } else {
          data.forEach((city) => {
            const item = document.createElement("div");
            item.className = "suggestion-item";
            item.textContent = city;
            item.addEventListener("click", () => {
              input.value = city;
              suggestions.style.display = "none";
            });
            suggestions.appendChild(item);
          });
        }

        suggestions.style.display = "block";
      })
      .catch((error) => {
        if (error.name !== "AbortError") {
          console.error("Ошибка автодополнения:", error);
        }
      });
  });

  // Закрытие подсказок при клике вне поля
  document.addEventListener("click", function (e) {
    if (e.target !== input) {
      suggestions.style.display = "none";
    }
  });

  // Навигация с клавиатуры
  input.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      suggestions.style.display = "none";
      return;
    }

    const items = suggestions.querySelectorAll(".suggestion-item");
    if (!items.length) return;

    let currentIndex = -1;
    items.forEach((item, index) => {
      if (item.classList.contains("active")) {
        currentIndex = index;
        item.classList.remove("active");
      }
    });

    if (e.key === "ArrowDown") {
      e.preventDefault();
      const newIndex = (currentIndex + 1) % items.length;
      items[newIndex].classList.add("active");
      input.value = items[newIndex].textContent;
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      const newIndex = (currentIndex - 1 + items.length) % items.length;
      items[newIndex].classList.add("active");
      input.value = items[newIndex].textContent;
    } else if (e.key === "Enter" && currentIndex >= 0) {
      e.preventDefault();
      input.value = items[currentIndex].textContent;
      suggestions.style.display = "none";
    }
  });
});
