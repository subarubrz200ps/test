const button = document.getElementById("run");
const queryInput = document.getElementById("query");
const summary = document.getElementById("summary");
const details = document.getElementById("details");

function scoreBadge(score) {
  if (score >= 80) return "high";
  if (score >= 60) return "mid";
  return "low";
}

button.addEventListener("click", async () => {
  const q = queryInput.value.trim();
  if (!q) return;

  summary.classList.remove("hidden");
  summary.innerHTML = "評価中...";
  details.classList.add("hidden");

  const res = await fetch(`/api/evaluate?q=${encodeURIComponent(q)}`);
  const data = await res.json();

  if (!res.ok) {
    summary.innerHTML = `エラー: ${data.error}`;
    return;
  }

  summary.innerHTML = `
    <h2>総合評価: <span class="${scoreBadge(data.overall)}">${data.overall}</span></h2>
    <ul>
      <li>権威性: ${data.authority}</li>
      <li>複数ソース一致度: ${data.consensus}</li>
      <li>医学的エビデンスレベル: ${data.evidence}</li>
      <li>対象件数: ${data.count}</li>
    </ul>
  `;

  details.classList.remove("hidden");
  details.innerHTML = `
    <h3>ソース別評価（根拠つき）</h3>
    <table>
      <thead>
        <tr><th>タイトル</th><th>権威性</th><th>一致度</th><th>エビデンス</th><th>総合</th><th>根拠</th></tr>
      </thead>
      <tbody>
        ${data.details
          .map(
            (row) => `
            <tr>
              <td><a href="${row.url}" target="_blank" rel="noopener noreferrer">${row.title}</a></td>
              <td>${row.authority}</td>
              <td>${row.consensus}</td>
              <td>${row.evidence}</td>
              <td><b>${row.total}</b></td>
              <td>
                <small>
                authority: ${row.reasons.authority}<br/>
                consensus: ${row.reasons.consensus}<br/>
                evidence: ${row.reasons.evidence}
                </small>
              </td>
            </tr>
          `
          )
          .join("")}
      </tbody>
    </table>
  `;
});
