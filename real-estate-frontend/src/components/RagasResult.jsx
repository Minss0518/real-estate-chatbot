export default function RagasResult() {
  const results = [
    {
      question: "전세 계약 기간은 얼마나 되나요?",
      faithfulness: 1.0,
      relevancy: 1.0,
    },
    {
      question: "보증금 돌려받으려면 어떻게 해야 하나요?",
      faithfulness: 0.7,
      relevancy: 0.9,
    },
    {
      question: "임대료 증액 청구 한도는 얼마인가요?",
      faithfulness: 1.0,
      relevancy: 1.0,
    },
  ];

  const avg_f = (results.reduce((s, r) => s + r.faithfulness, 0) / results.length).toFixed(2);
  const avg_r = (results.reduce((s, r) => s + r.relevancy, 0) / results.length).toFixed(2);

  const getColor = (score) => {
    if (score >= 0.9) return "#6B8F47";
    if (score >= 0.7) return "#C4956A";
    return "#C0624A";
  };

  return (
    <div style={{ padding: "20px 0" }}>
      <h2 style={{ fontSize: "15px", fontWeight: "600", color: "var(--text-primary)", marginBottom: "16px" }}>
        📊 RAGAS 품질 평가 결과
      </h2>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px", marginBottom: "16px" }}>
        <div style={{ background: "var(--bg-card)", border: "1px solid var(--border)", borderRadius: "10px", padding: "14px", textAlign: "center" }}>
          <div style={{ fontSize: "12px", color: "var(--text-muted)", marginBottom: "6px" }}>평균 충실도</div>
          <div style={{ fontSize: "26px", fontWeight: "700", color: getColor(avg_f) }}>{avg_f}</div>
        </div>
        <div style={{ background: "var(--bg-card)", border: "1px solid var(--border)", borderRadius: "10px", padding: "14px", textAlign: "center" }}>
          <div style={{ fontSize: "12px", color: "var(--text-muted)", marginBottom: "6px" }}>평균 관련성</div>
          <div style={{ fontSize: "26px", fontWeight: "700", color: getColor(avg_r) }}>{avg_r}</div>
        </div>
      </div>

      {results.map((r, i) => (
        <div key={i} style={{ background: "var(--bg-card)", border: "1px solid var(--border)", borderRadius: "10px", padding: "14px", marginBottom: "10px" }}>
          <div style={{ fontSize: "13px", color: "var(--text-secondary)", marginBottom: "10px", fontWeight: "500" }}>
            Q. {r.question}
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: "12px", color: "var(--text-muted)", marginBottom: "4px" }}>
                <span>충실도</span>
                <span style={{ color: getColor(r.faithfulness), fontWeight: "600" }}>{r.faithfulness.toFixed(1)}</span>
              </div>
              <div style={{ background: "var(--border)", borderRadius: "4px", height: "6px" }}>
                <div style={{ width: `${r.faithfulness * 100}%`, background: getColor(r.faithfulness), borderRadius: "4px", height: "6px", transition: "width 0.5s" }} />
              </div>
            </div>
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: "12px", color: "var(--text-muted)", marginBottom: "4px" }}>
                <span>관련성</span>
                <span style={{ color: getColor(r.relevancy), fontWeight: "600" }}>{r.relevancy.toFixed(1)}</span>
              </div>
              <div style={{ background: "var(--border)", borderRadius: "4px", height: "6px" }}>
                <div style={{ width: `${r.relevancy * 100}%`, background: getColor(r.relevancy), borderRadius: "4px", height: "6px", transition: "width 0.5s" }} />
              </div>
            </div>
          </div>
        </div>
      ))}

      <div style={{ fontSize: "11px", color: "var(--text-subtle)", textAlign: "center", marginTop: "8px" }}>
        chunk_size 1024 기준 측정값
      </div>
    </div>
  );
}