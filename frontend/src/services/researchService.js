import { MOCK_SESSIONS } from './mockData';

// Delay helper to simulate network latency
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

export const researchService = {
  async getSessions() {
    await delay(600);
    return MOCK_SESSIONS;
  },

  async getSession(id) {
    await delay(400);
    return MOCK_SESSIONS.find(s => s.id === id);
  },

  async startResearch(question, onProgress) {
    // Simulate the research pipeline
    const sessionId = `session_${Date.now()}`;
    
    const steps = [
      "Understanding research question...",
      "Planning research angles...",
      "Searching the web...",
      "Fetching relevant web pages...",
      "Analyzing sources...",
      "Checking research completeness...",
      "Extracting factual claims...",
      "Building evidence...",
      "Preparing report..."
    ];

    for (const step of steps) {
      onProgress(step);
      // Random delay between 800ms and 2000ms for realism
      await delay(Math.floor(Math.random() * 1200) + 800); 
    }

    // Return a new mock session
    const newSession = {
      id: sessionId,
      question,
      createdAt: new Date().toISOString(),
      status: "complete",
      summary: "This is a dynamically generated mock summary for the query. In a real environment, the backend would synthesize the research report and key findings from the vector database.",
      findings: [
        "First key finding extracted from the research context.",
        "Second major point of evidence discovered during analysis.",
        "A counter-perspective or market risk associated with the query."
      ],
      claims: [
        {
          id: "c_new_1",
          text: "The subject possesses significant market potential based on recent growth vectors.",
          evidence: "Market analysis indicates a 40% YoY expansion in the primary target sector.",
          sourceId: "src_new_1"
        }
      ],
      sources: [
        {
          id: "src_new_1",
          title: "Global Market Analysis Report",
          domain: "research.net",
          url: "https://research.net/analysis",
          relevance: 0.95,
          description: "Detailed overview of sector growth and technological trends.",
          type: "Industry Report"
        },
        {
          id: "src_new_2",
          title: "Technical Review of Current Capabilities",
          domain: "techinsights.com",
          url: "https://techinsights.com/review",
          relevance: 0.88,
          description: "Deep dive into the architectural and strategic advantages.",
          type: "Technical Analysis"
        }
      ],
      report: `
## Executive Summary
This report was generated in response to the query: "${question}". It outlines the primary considerations, technological developments, and strategic market positioning related to the topic.

## Key Insights
The investigation reveals a rapidly evolving landscape characterized by intense competition and significant capital investment. The core technologies are reaching maturity, enabling broader enterprise adoption.

## Market Dynamics
Current trajectories indicate a consolidation phase, where established players are leveraging their existing ecosystems to create high switching costs. Emerging competitors are primarily focusing on specialized niches or offering disruptive pricing models.

## Conclusion
The strategic importance of this sector cannot be overstated. Future developments will likely hinge on software-defined capabilities and the integration of next-generation processing architectures.
      `,
      followUpHistory: []
    };

    // Add to mock db
    MOCK_SESSIONS.unshift(newSession);

    return newSession;
  }
};
