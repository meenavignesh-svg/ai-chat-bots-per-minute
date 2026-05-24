const messagesEl = document.querySelector('#messages');
const keyForm = document.querySelector('#keyForm');
const apiKeyInput = document.querySelector('#apiKeyInput');
const form = document.querySelector('#chatForm');
const input = document.querySelector('#userInput');
const button = document.querySelector('#sendButton');
const statusEl = document.querySelector('#status');

const history = [];
let apiKey = sessionStorage.getItem('openai_api_key') || '';

function addMessage(text, sender, extraClass = '') {
  const bubble = document.createElement('div');
  bubble.className = `message ${sender} ${extraClass}`.trim();
  bubble.textContent = text;
  messagesEl.appendChild(bubble);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function refreshKeyState() {
  statusEl.textContent = apiKey ? 'online' : 'needs key';
  input.disabled = !apiKey;
  button.disabled = !apiKey;
}

function setBusy(isBusy) {
  button.disabled = isBusy || !apiKey;
  input.disabled = isBusy || !apiKey;
  statusEl.textContent = isBusy ? 'planning' : apiKey ? 'online' : 'needs key';
  statusEl.classList.toggle('busy', isBusy);
}

keyForm.addEventListener('submit', (event) => {
  event.preventDefault();
  apiKey = apiKeyInput.value.trim();
  if (!apiKey) return;
  sessionStorage.setItem('openai_api_key', apiKey);
  apiKeyInput.value = '';
  refreshKeyState();
  addMessage('API key saved for this browser session. You can start chatting now.', 'bot');
  input.focus();
});

async function sendMessage(text) {
  history.push({ role: 'user', content: text });
  setBusy(true);

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify({ messages: history })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Request failed.');
    }

    history.push({ role: 'assistant', content: data.reply });
    addMessage(data.reply, 'bot');
  } catch (error) {
    addMessage(error.message, 'bot', 'error');
  } finally {
    setBusy(false);
    input.focus();
  }
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (!text || !apiKey) return;

  addMessage(text, 'user');
  input.value = '';
  sendMessage(text);
});

addMessage('Budget Mentor is ready. Enter your OpenAI API key above, then ask about budgets, saving plans, or money goals.', 'bot');
refreshKeyState();
