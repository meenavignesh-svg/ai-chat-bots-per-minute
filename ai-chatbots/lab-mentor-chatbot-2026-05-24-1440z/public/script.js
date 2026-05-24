const messagesEl = document.querySelector('#messages');
const form = document.querySelector('#chatForm');
const input = document.querySelector('#userInput');
const button = document.querySelector('#sendButton');
const statusEl = document.querySelector('#status');

const history = [];

const demoReplies = [
  { match: ['experiment', 'plan', 'project'], text: 'Demo mode: start with one clear question, list the materials, define a control, and decide what result would count as success.' },
  { match: ['debug', 'error', 'problem'], text: 'Demo mode: isolate one variable, reproduce the issue, record what changed, then test the smallest possible fix.' },
  { match: ['study', 'learn', 'explain'], text: 'Demo mode: break the topic into three parts: what it is, why it matters, and one example you can test.' },
  { match: ['safety', 'safe'], text: 'Demo mode: check labels, use protective gear, keep notes, and ask a qualified person before doing anything risky.' }
];

function addMessage(text, sender, extraClass = '') {
  const bubble = document.createElement('div');
  bubble.className = `message ${sender} ${extraClass}`.trim();
  bubble.textContent = text;
  messagesEl.appendChild(bubble);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function setBusy(isBusy, label = 'thinking') {
  button.disabled = isBusy;
  input.disabled = isBusy;
  statusEl.textContent = isBusy ? label : 'demo ready';
  statusEl.classList.toggle('busy', isBusy);
}

function getDemoReply(text) {
  const clean = text.toLowerCase();
  const hit = demoReplies.find((reply) => reply.match.some((word) => clean.includes(word)));
  if (hit) return hit.text;
  return `Demo mode: I would turn "${text}" into a simple testable question, then suggest the next safe step.`;
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
addMessage('Lab Mentor is ready in browser demo mode. Ask about a project idea, experiment plan, debugging step, or study question.', 'bot');
