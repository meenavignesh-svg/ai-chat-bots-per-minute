const messagesEl = document.querySelector('#messages');
const form = document.querySelector('#chatForm');
const input = document.querySelector('#userInput');
const button = document.querySelector('#sendButton');
const statusEl = document.querySelector('#status');

const history = [];

const demoReplies = [
  { match: ['beach', 'safe', 'safety'], text: 'Demo mode: check flags, stay near lifeguards, watch currents, and keep a clear meeting point for your group.' },
  { match: ['rip', 'current'], text: 'Demo mode: for a rip current, do not fight straight back. Float, signal for help, and move parallel to shore when possible.' },
  { match: ['first aid', 'injury', 'hurt'], text: 'Demo mode: for serious symptoms or danger, call local emergency services. For minor issues, move to shade, rinse, and monitor closely.' },
  { match: ['plan', 'rescue'], text: 'Demo mode: assign one caller, one spotter, and one person to guide responders. Keep yourself safe first.' }
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
  return `Demo mode: I would treat "${text}" as an ocean-safety question and start by checking urgency, location, and available help.`;
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
addMessage('Ocean Medic is ready in browser demo mode. Ask about beach safety, rescue planning, or ocean first aid basics.', 'bot');
