async function loadTransactions() {
  const tbody = document.getElementById("transactions-body");

  try {
    const response = await fetch("/api/dashboard/data");

    if (response.status === 401) {
      window.location.href = "/dashboard/login";
      return;
    }

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    renderTransactions(data.recent_transactions);
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="8" class="loading-row">Failed to load data. Please try again.</td></tr>`;
    console.error("Failed to fetch dashboard data:", err);
  }
}

function renderTransactions(transactions) {
  const tbody = document.getElementById("transactions-body");

  if (!transactions || transactions.length === 0) {
    tbody.innerHTML = `<tr><td colspan="8" class="loading-row">No transactions found.</td></tr>`;
    return;
  }

  tbody.innerHTML = transactions.map(tx => `
    <tr>
      <td>${tx.id}</td>
      <td>${escapeHtml(tx.account_id)}</td>
      <td>${Number(tx.amount).toLocaleString("en-US", { minimumFractionDigits: 2 })}</td>
      <td>${escapeHtml(tx.currency)}</td>
      <td><span class="badge badge-${tx.type}">${escapeHtml(tx.type)}</span></td>
      <td><span class="badge badge-${tx.status}">${escapeHtml(tx.status)}</span></td>
      <td>${tx.description ? escapeHtml(tx.description) : "—"}</td>
      <td>${formatDate(tx.created_at)}</td>
    </tr>
  `).join("");
}

function formatDate(dateStr) {
  if (!dateStr) return "—";
  const d = new Date(dateStr);
  return d.toLocaleString("en-AU", { dateStyle: "medium", timeStyle: "short" });
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

document.addEventListener("DOMContentLoaded", () => {
  loadTransactions();
  document.getElementById("refresh-btn").addEventListener("click", loadTransactions);
});
