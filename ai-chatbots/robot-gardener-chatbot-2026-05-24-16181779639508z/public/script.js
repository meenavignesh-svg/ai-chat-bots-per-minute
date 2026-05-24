const messagesEl = document.querySelector('#messages');
    const keyForm = document.querySelector('#keyForm');
    const apiKeyInput = document.querySelector('#apiKeyInput');
    const form = document.querySelector('#chatForm');
    const input = document.querySelector('#userInput');
    const button = document.querySelector('#sendButton');
    const statusEl = document.querySelector('#status');

    const history = [];
    let apiKey = sessionStorage.getItem('openai_api_key') || '';
    const demoReplies = [
  {
    "match": [
      "water"
    ],
    "text": "You need water."
  },
  {
    "match": [
      "prune"
    ],
    "text": "Time for pruning, little one!"
  },
  {
    "match": [
      "fertilize"
    ],
    "text": "Fertilizer is ready!"
  },
  {
    "match": [
      "plant_id"
    ],
    "text": "Plant ID: [insert plant ID here]"
  }
];

    function addMessage(text, sender, extraClass = '') {
      const bubble = document.createElement('div');
      bubble.className = `message ${sender} ${extraClass}`.trim();
      bubble.textContent = text;
      messagesEl.appendChild(bubble);
      messagesEl.scrollTop = messagesEl.scrollHeight;
    }

    function refreshKeyState() {
      statusEl.textContent = apiKey ? 'real AI ready' : 'demo ready';
      input.disabled = false;
      button.disabled = false;
    }

    function setBusy(isBusy) {
      button.disabled = isBusy;
      input.disabled = isBusy;
      statusEl.textContent = isBusy ? "growing" : apiKey ? 'real AI ready' : 'demo ready';
      statusEl.classList.toggle('busy', isBusy);
    }

    function getDemoReply(text) {
      const clean = text.toLowerCase();
      const hit = demoReplies.find((reply) => reply.match.some((word) => clean.includes(word)));
      if (hit) return hit.text;
      return `Demo mode: I would turn "${text}" into a practical next step in the Robot Gardener style.`;
    }

    keyForm.addEventListener('submit', (event) => {
      event.preventDefault();
      apiKey = apiKeyInput.value.trim();
      if (!apiKey) return;
      sessionStorage.setItem('openai_api_key', apiKey);
      apiKeyInput.value = '';
      refreshKeyState();
      addMessage('API key saved for this browser session. Real AI mode is ready after Vercel deployment; demo mode still works anytime.', 'bot');
      input.focus();
    });

    async function sendMessage(text) {
      history.push({ role: 'user', content: text });
      setBusy(true);

      if (!apiKey) {
        window.setTimeout(() => {
          const reply = getDemoReply(text);
          history.push({ role: 'assistant', content: reply });
          addMessage(reply, 'bot');
          setBusy(false);
          input.focus();
        }, 250);
        return;
      }

      try {
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`
          },
          body: JSON.stringify({ messages: history })
        });

        if (!response.ok) throw new Error('Demo fallback');
        const data = await response.json();
        const reply = data.reply || getDemoReply(text);
        history.push({ role: 'assistant', content: reply });
        addMessage(reply, 'bot');
      } catch {
        const reply = getDemoReply(text);
        history.push({ role: 'assistant', content: reply });
        addMessage(reply, 'bot');
      } finally {
        setBusy(false);
        input.focus();
      }
    }

    form.addEventListener('submit', (event) => {
      event.preventDefault();
      const text = input.value.trim();
      if (!text) return;
      addMessage(text, 'user');
      input.value = '';
      sendMessage(text);
    });

    addMessage({"text": "Welcome to the Robot Gardener! I'll help you tend to your plants.", "icon_url": ""}, 'bot');
    refreshKeyState();
