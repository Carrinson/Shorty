const form = document.getElementById("shorten-form");
const urlInput = document.getElementById("url-input");
const aliasInput = document.getElementById("alias-input");
const errorEl = document.getElementById("error");
const resultEl = document.getElementById("result");
const linksBody = document.getElementById("links-body");

function showError(message) {
  errorEl.textContent = message;
  errorEl.classList.remove("hidden");
  resultEl.classList.add("hidden");
}

function showResult(shortUrl) {
  const fullUrl = `${window.location.origin}${shortUrl}`;
  resultEl.innerHTML = `Short link: <a href="${shortUrl}" target="_blank">${fullUrl}</a>`;
  resultEl.classList.remove("hidden");
  errorEl.classList.add("hidden");
}

async function loadLinks() {
  const res = await fetch("/api/urls");
  const links = await res.json();
  linksBody.innerHTML = "";
  for (const link of links) {
    const row = document.createElement("tr");
    const fullShortUrl = `${window.location.origin}${link.short_url}`;
    row.innerHTML = `
      <td><a href="${link.short_url}" target="_blank">${fullShortUrl}</a></td>
      <td>${link.url}</td>
      <td>${link.clicks}</td>
      <td><button class="delete-btn" data-code="${link.code}">Delete</button></td>
    `;
    linksBody.appendChild(row);
  }
}

linksBody.addEventListener("click", async (e) => {
  if (!e.target.classList.contains("delete-btn")) return;
  const code = e.target.dataset.code;
  await fetch(`/api/r/${code}`, { method: "DELETE" });
  loadLinks();
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const body = { url: urlInput.value };
  if (aliasInput.value.trim()) {
    body.alias = aliasInput.value.trim();
  }

  const res = await fetch("/api/shorten", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  const data = await res.json();

  if (!res.ok) {
    showError(data.detail || "Something went wrong");
    return;
  }

  showResult(data.short_url);
  urlInput.value = "";
  aliasInput.value = "";
  loadLinks();
});

loadLinks();
