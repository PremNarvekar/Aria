// Use Vite env variable in production, fallback to localhost for dev
const API_BASE = import.meta.env.VITE_API_URL || "/api";
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
      // EventSource doesn't support Authorization header, so we pass it in query
      const eventSource = new EventSource(`${API_BASE}/research/${sessionId}/stream?token=${TEST_TOKEN}`);

      let finalReport = null;
      let finalStatus = "running";
      let error = null;

      eventSource.onmessage = (event) => {
        try {
          const parsed = JSON.parse(event.data);
          
          if (parsed.type === "node_completed") {
            onProgress(parsed.label || `Completed: ${parsed.node}`);
          } 
          else if (parsed.type === "research_completed") {
            finalStatus = "completed";
            const rawReport = parsed.report || {};
            
            eventSource.close();
            
            // Resolve the promise mapping backend model to frontend UI props
            resolve({
              id: sessionId,
              question: question,
              status: finalStatus,
              summary: rawReport.executive_summary || "Research completed successfully.",
              findings: rawReport.key_findings || [],
              claims: parsed.claims || [], // Provided if we want to pass them later
              sources: rawReport.sources || [],
              report: rawReport.analysis || "No detailed analysis provided.",
              createdAt: new Date().toISOString()
            });
          }
          else if (parsed.type === "research_failed") {
            finalStatus = "failed";
            error = parsed.error;
            eventSource.close();
            reject(new Error(error || "Research failed"));
          }
        } catch (e) {
          console.error("Error parsing SSE data", e);
        }
      };

      eventSource.onerror = (err) => {
        console.error("SSE Error:", err);
        // Only close if it's a fatal error, browsers often auto-reconnect SSE
      };
    });
  }
};
