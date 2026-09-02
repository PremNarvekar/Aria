export const followupService = {
  async askQuestion(sessionId, question) {
    const response = await fetch(`/api/research/${sessionId}/followup?token=test-user-123`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question })
    });

    if (!response.ok) {
      throw new Error(`Follow-up failed: ${response.statusText}`);
    }

    const data = await response.json();
    
    return {
      id: `msg_${Date.now()}`,
      role: "assistant",
      text: data.answer,
      sources: data.sources || []
    };
  }
};
