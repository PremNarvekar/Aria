import { MOCK_SESSIONS } from './mockData';

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

export const followupService = {
  async askQuestion(sessionId, question) {
    await delay(1500); // Simulate thinking time
    
    const session = MOCK_SESSIONS.find(s => s.id === sessionId);
    if (!session) throw new Error("Session not found");

    const answer = {
      id: `msg_${Date.now()}`,
      role: "assistant",
      text: `Based on the research context, here is an analysis of your question: "${question}".\n\nThe ecosystem is characterized by rapid innovation. The current data strongly suggests that integrated architectures are providing significant performance advantages over traditional disjointed systems. Furthermore, market adoption metrics indicate a growing preference for solutions that offer both hardware and software synergies.`,
      sources: session.sources.length > 0 ? [session.sources[0].id] : []
    };

    session.followUpHistory.push({
      id: `msg_u_${Date.now()}`,
      role: "user",
      text: question
    });
    session.followUpHistory.push(answer);

    return answer;
  }
};
