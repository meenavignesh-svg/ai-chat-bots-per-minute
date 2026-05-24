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
      "quest"
    ],
    "text": "Demo mode: a missing map points to a locked observatory where the stars have been rearranged overnight."
  },
  {
    "match": [
      "npc"
    ],
    "text": "Demo mode: create one desire, one secret, one habit, and one thing the NPC refuses to say first."
  },
  {
    "match": [
      "puzzle"
    ],
    "text": "Demo mode: make the answer visible in the room, but require players to connect two clues."
  },
  {
    "match": [
      "encounter"
    ],
    "text": "Demo mode: add a goal besides fighting, a terrain twist, and a reason to negotiate."
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
      statusEl.textContent = isBusy ? "rolling" : apiKey ? 'real AI ready' : 'demo ready';
      statusEl.classList.toggle('busy', isBusy);
    }

    function getDemoReply(text) {
      const clean = text.toLowerCase();
      const hit = demoReplies.find((reply) => reply.match.some((word) => clean.includes(word)));
      if (hit) return hit.text;
      return `Demo mode: I would turn "${text}" into a practical next step in the Game Master style.`;
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

    addMessage("Game Master is ready in browser demo mode. Ask for quests, NPCs, puzzles, or encounter ideas.", 'bot');
    refreshKeyState();
