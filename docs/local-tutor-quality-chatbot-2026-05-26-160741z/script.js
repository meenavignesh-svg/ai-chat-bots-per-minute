const messages = document.querySelector('#messages');
const text = document.querySelector('#text');
const apiInput = document.querySelector('#apiKey');
const statusEl = document.querySelector('#status');
const qualityEl = document.querySelector('#quality');
const sendButton = document.querySelector('#chatForm button');
const quickActions = ["Options", "Tradeoffs", "Recommendation"];
let apiKey = sessionStorage.getItem('openai_api_key') || '';
const history = [];

function add(content, role = 'bot') {
  const node = document.createElement('div');
  node.className = `msg ${role}`;
  node.textContent = content;
  messages.appendChild(node);
  messages.scrollTop = messages.scrollHeight;
}

function setBusy(isBusy) {
  sendButton.disabled = isBusy;
  statusEl.textContent = isBusy ? 'thinking' : apiKey ? 'real AI ready' : 'demo ready';
}

function demoReply(value) {
  const chosen = quickActions.find((item) => value.toLowerCase().includes(item.toLowerCase())) || 'Decision Lens';
  return `${chosen} mode: I can help with local model testing and prompt-result notes; practical quality check support; clear next-step guidance. Ask one specific question and I will turn it into a useful action. Requested focus: "${value}".`;
}

document.querySelectorAll('.chip').forEach((button) => {
  button.addEventListener('click', () => {
    text.value = `${button.textContent}: `;
    text.focus();
    qualityEl.textContent = `Premium variant: research-desk / ${button.textContent}`;
  });
});

document.querySelector('#keyForm').addEventListener('submit', (event) => {
  event.preventDefault();
  apiKey = apiInput.value.trim();
  if (!apiKey) return;
  sessionStorage.setItem('openai_api_key', apiKey);
  apiInput.value = '';
  statusEl.textContent = 'real AI ready';
  add('API key saved for this browser session. Real AI mode is ready after deployment.');
});

document.querySelector('#chatForm').addEventListener('submit', async (event) => {
  event.preventDefault();
  const value = text.value.trim();
  if (!value) return;
  text.value = '';
  add(value, 'user');
  history.push({ role: 'user', content: value });
  setBusy(true);
  if (!apiKey) {
    const reply = demoReply(value);
    history.push({ role: 'assistant', content: reply });
    setTimeout(() => { add(reply); setBusy(false); }, 220);
    return;
  }
  try {
    const response = await fetch('/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${apiKey}` }, body: JSON.stringify({ messages: history }) });
    const data = await response.json();
    const reply = data.reply || data.error || 'No reply received.';
    history.push({ role: 'assistant', content: reply });
    add(reply);
  } catch {
    add(demoReply(value));
  } finally {
    setBusy(false);
  }
});

add("I can help with local model testing and prompt-result notes; practical quality check support; clear next-step guidance. Ask one specific question and I will turn it into a useful action.");
