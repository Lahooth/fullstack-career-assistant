import { useState } from "react";

export default function Home() {
  const [targetRole, setTargetRole] = useState("Backend Developer");
  const [skillsInput, setSkillsInput] = useState("");
  const [skillGap, setSkillGap] = useState(null);
  const [roadmap, setRoadmap] = useState(null);
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  // For local dev – change this to your Render URL after deployment
  const BACKEND_BASE_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";




  const handleAnalyze = async (e) => {
    e.preventDefault();
    setErrorMsg("");
    setLoading(true);

    const skills = skillsInput
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);

    if (!targetRole || skills.length === 0) {
      setErrorMsg("Please enter a target role and at least one skill.");
      setLoading(false);
      return;
    }

    try {
      // Skill Gap
      const skillGapRes = await fetch(`${BACKEND_BASE_URL}/api/skill-gap`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          target_role: targetRole,
          current_skills: skills,
        }),
      });

      if (!skillGapRes.ok) {
        const err = await skillGapRes.json();
        throw new Error(err.detail || "Failed to fetch skill gap");
      }

      const skillGapData = await skillGapRes.json();
      setSkillGap(skillGapData);

      // Roadmap
      const roadmapRes = await fetch(`${BACKEND_BASE_URL}/api/roadmap`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          target_role: targetRole,
        }),
      });

      if (!roadmapRes.ok) {
        const err = await roadmapRes.json();
        throw new Error(err.detail || "Failed to fetch roadmap");
      }

      const roadmapData = await roadmapRes.json();
      setRoadmap(roadmapData);

      // Tech News
      const newsRes = await fetch(`${BACKEND_BASE_URL}/api/tech-news`);
      if (!newsRes.ok) {
        throw new Error("Failed to fetch tech news");
      }
      const newsData = await newsRes.json();
      setNews(newsData.stories || []);
    } catch (err) {
      console.error(err);
      setErrorMsg(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container fade-in">
      {/* PAGE HEADER */}
      <header style={{ marginBottom: "1.75rem" }}>
        <h1>Career Skill Gap &amp; Roadmap Assistant</h1>
        <p style={{ marginTop: "0.4rem" }}>
          Enter your target role and current skills to analyze your skill gap,
          generate a learning roadmap, and explore the latest tech news.
        </p>
      </header>

      {/* FORM CARD */}
      <section className="card" style={{ marginBottom: "1.5rem" }}>
        <form onSubmit={handleAnalyze}>
          <div style={{ marginBottom: "1rem" }}>
            <label>
              Target Role
              <input
                type="text"
                value={targetRole}
                onChange={(e) => setTargetRole(e.target.value)}
                placeholder='e.g. "Backend Developer"'
              />
            </label>
          </div>

          <div style={{ marginBottom: "0.75rem" }}>
            <label>
              Current Skills (comma-separated)
              <input
                type="text"
                value={skillsInput}
                onChange={(e) => setSkillsInput(e.target.value)}
                placeholder='e.g. "Java, SQL, Git"'
              />
            </label>
            <small style={{ color: "#6b7280" }}>
              Example roles: Frontend Developer, Backend Developer, Data Analyst
            </small>
          </div>

          {errorMsg && (
            <p style={{ color: "red", marginTop: "0.5rem" }}>{errorMsg}</p>
          )}

          <button type="submit" disabled={loading}>
            {loading ? "Analyzing..." : "Analyze My Career Path"}
          </button>
        </form>
      </section>

      {/* DASHBOARD */}
      {(skillGap || roadmap || news.length > 0) && (
        <>
          {/* TOP GRID: SKILL GAP + ROADMAP */}
          <section className="dashboard-grid">
            {/* Skill Gap Card */}
            <div className="card">
              <h2>Skill Gap Results</h2>
              {!skillGap && <p>Run an analysis to see your skill gap.</p>}

              {skillGap && (
                <>
                  <p style={{ marginTop: "0.5rem" }}>
                    <strong>Target Role:</strong> {skillGap.target_role}
                  </p>
                  <p>
                    <strong>Required Skills:</strong>{" "}
                    {skillGap.required_skills.join(", ")}
                  </p>
                  <p>
                    <strong>Matched Skills:</strong>{" "}
                    {skillGap.matched_skills.length > 0
                      ? skillGap.matched_skills.join(", ")
                      : "None yet"}
                  </p>
                  <p>
                    <strong>Missing Skills:</strong>{" "}
                    {skillGap.missing_skills.length > 0
                      ? skillGap.missing_skills.join(", ")
                      : "No gaps — great job!"}
                  </p>

                  {skillGap.recommendations.length > 0 && (
                    <>
                      <h4>Recommendations</h4>
                      <ul>
                        {skillGap.recommendations.map((rec, idx) => (
                          <li key={idx}>{rec}</li>
                        ))}
                      </ul>
                    </>
                  )}

                  {skillGap.suggested_learning_order.length > 0 && (
                    <>
                      <h4>Suggested Learning Order</h4>
                      <ol>
                        {skillGap.suggested_learning_order.map((s, idx) => (
                          <li key={idx}>{s}</li>
                        ))}
                      </ol>
                    </>
                  )}
                </>
              )}
            </div>

            {/* Roadmap Card */}
            <div className="card">
              <h2>Career Roadmap</h2>
              {!roadmap && <p>Run an analysis to see a roadmap.</p>}

              {roadmap && (
                <>
                  <p style={{ marginTop: "0.5rem" }}>
                    <strong>Target Role:</strong> {roadmap.target_role}
                  </p>
                  <div style={{ marginTop: "0.75rem" }}>
                    {roadmap.phases.map((phase, idx) => (
                      <div
                        key={idx}
                        style={{
                          borderLeft: "3px solid #2563eb",
                          paddingLeft: "0.75rem",
                          marginBottom: "0.9rem",
                        }}
                      >
                        <strong>{phase.phase}</strong>
                        <p style={{ margin: "0.15rem 0", color: "#4b5563" }}>
                          Focus: {phase.focus}
                        </p>
                        <ul style={{ marginTop: "0.25rem" }}>
                          {phase.items.map((item, i) => (
                            <li key={i}>{item}</li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                </>
              )}
            </div>
          </section>

          {/* BOTTOM: TECH NEWS */}
          <section className="card" style={{ marginBottom: "2rem" }}>
            <h2>Latest Tech News (HackerNews)</h2>
            {news.length === 0 && (
              <p style={{ marginTop: "0.5rem" }}>
                No stories loaded yet. Run an analysis to fetch the latest news.
              </p>
            )}

            {news.length > 0 && (
              <ul
                style={{
                  listStyle: "none",
                  paddingLeft: 0,
                  marginTop: "0.75rem",
                }}
              >
                {news.map((story) => (
                  <li key={story.id} className="news-item">
                    <a
                      href={
                        story.url ||
                        `https://news.ycombinator.com/item?id=${story.id}`
                      }
                      target="_blank"
                      rel="noreferrer"
                    >
                      {story.title}
                    </a>
                    <div className="news-meta">
                      <span>Score: {story.score ?? "N/A"}</span> {" · "}
                      <span>By: {story.by}</span> {" · "}
                      <span>Type: {story.type}</span> {" · "}
                      <span>{story.time}</span>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </section>
        </>
      )}
    </div>
  );
}
