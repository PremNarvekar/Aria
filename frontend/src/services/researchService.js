// Use Vite env variable in production, fallback to direct Render backend to avoid Netlify proxy SSE buffering
const API_BASE = import.meta.env.VITE_API_URL || "https://aria-backend-n6kc.onrender.com/api";
const TEST_TOKEN = "test-user-123"; // Dummy token for Milestone 11 Auth

export const researchService = {
  
  // NOTE: getSessions() isn't implemented in the backend yet, 
  // so we will just return empty or you can mock it.
  async getSessions() {
    return [];
  },

  async getSession(id) {
    const response = await fetch(`${API_BASE}/research/${id}`, {
      headers: {
        "Authorization": `Bearer ${TEST_TOKEN}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`Failed to fetch session: ${response.statusText}`);
    }
    
    const data = await response.json();
    
    // Map backend response to UI structure
    const rawReport = data.report || {};
    return {
      id: data.research_id,
      question: data.question,
      status: data.status,
      summary: rawReport.executive_summary || "",
      findings: rawReport.key_findings || [],
      claims: [], 
      sources: rawReport.sources || [],
      report: rawReport.analysis || "",
      createdAt: data.created_at || new Date().toISOString()
    };
  },

  async startResearch(question, onProgress) {
    // 1. Trigger the research POST request
    const response = await fetch(`${API_BASE}/research`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${TEST_TOKEN}`
      },
      body: JSON.stringify({ question })
    });

    if (!response.ok) {
      throw new Error(`Failed to start research: ${response.statusText}`);
    }

    const data = await response.json();
    const sessionId = data.research_id;

    // 2. Connect to the SSE Stream to listen for live updates
    return new Promise((resolve, reject) => {
      const eventSource = new EventSource(`${API_BASE}/research/${sessionId}/stream?token=${TEST_TOKEN}`);

      eventSource.addEventListener("connected", (e) => {
        console.log("SSE connected:", JSON.parse(e.data));
      });

      eventSource.addEventListener("node_completed", (e) => {
        try {
          const parsed = JSON.parse(e.data);
          onProgress(parsed.label || `Completed: ${parsed.node}`);
        } catch (err) {
          console.error("Error parsing node_completed", err);
        }
      });

      eventSource.addEventListener("research_completed", (e) => {
        try {
          const parsed = JSON.parse(e.data);
          const rawReport = parsed.report || {};
          eventSource.close();
          resolve({
            id: sessionId,
            question: question,
            status: "completed",
            summary: rawReport.executive_summary || "Research completed successfully.",
            findings: rawReport.key_findings || [],
            claims: parsed.claims || [],
            sources: rawReport.sources || [],
            report: rawReport.analysis || "No detailed analysis provided.",
            createdAt: new Date().toISOString()
          });
        } catch (err) {
          console.error("Error parsing research_completed", err);
        }
      });

      eventSource.addEventListener("research_failed", (e) => {
        try {
          const parsed = JSON.parse(e.data);
          eventSource.close();
          reject(new Error(parsed.error || "Research failed"));
        } catch (err) {
          eventSource.close();
          reject(new Error("Research failed"));
        }
      });

      eventSource.onerror = (err) => {
        console.error("SSE connection error:", err);
      };
    });
  }
};
