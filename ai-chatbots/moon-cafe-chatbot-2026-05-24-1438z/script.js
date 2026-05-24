const messages = document.querySelector('#messages');
const form = document.querySelector('#chatForm');
const input = document.querySelector('#userInput');

const replies = [
  {
    match: ['hello', 'hi', 'hey'],
    text: 'Welcome to Moon Cafe. Your table has a window view of Earthrise.'
  },
  {
    match: ['menu', 'drink', 'coffee'],
    text: 'Today we have crater cocoa, orbit espresso, and vanilla comet tea.'
  },
  {
    match: ['recommend', 'suggest'],
    text: 'I recommend orbit espresso: bright, bold, and approved for low-gravity mornings.'
  },
  {
    match: ['space', 'moon', 'lunar'],
    text: 'Moon Cafe note: drinks need sealed lids here. Floating foam is charming until cleanup time.'
  },
  {
    match: ['relax', 'tired', 'help'],
    text: 'Take one slow breath, warm your hands around the cup, and let the station hum do the rest.'
  }
];

function addMessage(text, sender) {
  const bubble = document.createElement('div');
  bubble.className = `message ${sender}`;
  bubble.textContent = text;
  messages.appendChild(bubble);
  messages.scrollTop = messages.scrollHeight;
}

function getBotReply(text) {
  const clean = text.toLowerCase();
  const hit = replies.find((reply) => reply.match.some((word) => clean.includes(word)));

  if (hit) return hit.text;

  return `I wrote "${text}" on a napkin and slid it to the chef. The Moon Cafe will think on it.`;
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, 'user');
  input.value = '';

  window.setTimeout(() => {
    addMessage(getBotReply(text), 'bot');
  }, 350);
});

addMessage('Moon Cafe is open. What can I get started for you?', 'bot');
