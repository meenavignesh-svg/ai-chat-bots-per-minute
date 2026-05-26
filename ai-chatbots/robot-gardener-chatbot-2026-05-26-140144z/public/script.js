const messagesEl = document.querySelector('#messages');
    const keyForm = document.querySelector('#keyForm');
    const apiKeyInput = document.querySelector('#apiKeyInput');
    const form = document.querySelector('#chatForm');
    const input = document.querySelector('#userInput');
    const button = document.querySelector('#sendButton');
    const statusEl = document.querySelector('#status');
    const history = [];
    const demoReplies = [
  {
    "match": [
      "water"
    ],
    "text": "Demo mode: check soil moisture first, water deeply when dry, and adjust for sunlight and pot size."
  },
  {
    "match": [
      "soil"
    ],
    "text": "Demo mode: healthy soil needs drainage, organic matter, and the right texture for the plant."
  },
  {
    "match": [
      "pest"
    ],
    "text": "Demo mode: isolate the plant, inspect leaves, rinse gently, and avoid harsh treatments at first."
  }
];
    let apiKey = sessionStorage.getItem('openai_api_key') || '';

    function addMessage(text, sender) {
      const bubble = document.createElement('div');
      bubble.className = `message ${sender}`;
      bubble.textContent = text;
      messagesEl.appendChild(bubble);
      messagesEl.scrollTop = messagesEl.scrollHeight;
    }
    function setBusy(isBusy) { button.disabled = isBusy; input.disabled = isBusy; statusEl.textContent = isBusy ? "growing" : apiKey ? 'real AI ready' : 'demo ready'; }
    function demoReply(text) {
      const clean = text.toLowerCase();
      const hit = demoReplies.find((reply) => reply.match.some((word) => clean.includes(word)));
      return hit ? hit.text : `Demo mode: I would turn "${text}" into a practical next step in the Robot Gardener style.`;
    }
    keyForm.addEventListener('submit', (event) => {
      event.preventDefault();
      apiKey = apiKeyInput.value.trim();
      if (!apiKey) return;
      sessionStorage.setItem('openai_api_key', apiKey);
      apiKeyInput.value = '';
      statusEl.textContent = 'real AI ready';
      addMessage('API key saved for this browser session. Real AI mode is ready after Vercel deployment.', 'bot');
    });
    async function sendMessage(text) {
      history.push({ role: 'user', content: text });
      setBusy(true);
      if (!apiKey) {
        setTimeout(() => { const reply = demoReply(text); history.push({ role: 'assistant', content: reply }); addMessage(reply, 'bot'); setBusy(false); }, 250);
        return;
      }
      try {
        const response = await fetch('/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${apiKey}` }, body: JSON.stringify({ messages: history }) });
        if (!response.ok) throw new Error('fallback');
        const data = await response.json();
        const reply = data.reply || demoReply(text);
        history.push({ role: 'assistant', content: reply });
        addMessage(reply, 'bot');
      } catch {
        const reply = demoReply(text);
        history.push({ role: 'assistant', content: reply });
        addMessage(reply, 'bot');
      } finally { setBusy(false); }
    }
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      const text = input.value.trim();
      if (!text) return;
      addMessage(text, 'user');
      input.value = '';
      sendMessage(text);
    });
    addMessage("Robot Gardener is ready in browser demo mode. Ask about plants, watering, soil, or garden planning.", 'bot');
