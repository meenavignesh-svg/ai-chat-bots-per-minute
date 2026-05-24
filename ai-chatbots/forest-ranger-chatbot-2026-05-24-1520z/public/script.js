const messagesEl = document.querySelector('#messages');
const form = document.querySelector('#chatForm');
const input = document.querySelector('#userInput');
const button = document.querySelector('#sendButton');
const statusEl = document.querySelector('#status');

const history = [];

const demoReplies = [
  { match: ['trail', 'hike', 'route'], text: 'Demo mode: pick a route that matches the slowest hiker, check daylight, pack water, and tell someone your plan.' },
  { match: ['camp', 'tent'], text: 'Demo mode: choose durable ground, keep food sealed, respect quiet hours, and leave the site cleaner than you found it.' },
  { match: ['weather', 'storm'], text: 'Demo mode: if weather turns, move away from exposed ridges, avoid tall isolated trees, and shorten the route.' },
  { match: ['safety', 'lost'], text: 'Demo mode: stop, stay visible, conserve phone battery, and use landmarks instead of wandering.' }
];

function addMessage(text, sender, extraClass = '') {
  const bubble = document.createElement('div');
  bubble.className = `message ${sender} ${extraClass}`.trim();
  bubble.textContent = text;
  messagesEl.appendChild(bubble);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function setBusy(isBusy) {
  button.disabled = isBusy;
  input.disabled = isBusy;
  statusEl.textContent = isBusy ? 'thinking' : 'demo ready';
  statusEl.classList.toggle('busy', isBusy);
}

function getDemoReply(text) {
  const clean = text.toLowerCase();
  const hit = demoReplies.find((reply) => reply.match.some((word) => clean.includes(word)));
  if (hit) return hit.text;
  return `Demo mode: I would handle "${text}" by checking safety, location, weather, and the simplest next trail decision.`;
}

async function sendMessage(text) {
  history.push({ role: 'user', content: text });
  setBusy(true);

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages: history })
    });

    if (!response.ok) throw new Error('Demo fallback');
    const data = await response.json();
    const reply = data.reply || getDemoReply(text);
    history.push({ role: 'assistant', content: reply });
    addMessage(reply, 'bot');
  } catch {
    window.setTimeout(() => {
      const reply = getDemoReply(text);
      history.push({ role: 'assistant', content: reply });
      addMessage(reply, 'bot');
    }, 250);
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

statusEl.textContent = 'demo ready';
addMessage('Forest Ranger is ready in browser demo mode. Ask about trails, campsite planning, nature facts, or safety basics.', 'bot');
