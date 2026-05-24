# Museum Guide Chatbot

A ready-to-run AI chatbot web app with a museum guide theme. The browser UI talks to a Node.js backend, and the backend calls the OpenAI Responses API with your server-side API key.

## Includes

- Express backend
- Official OpenAI Node SDK
- Server-side `OPENAI_API_KEY` handling
- Browser chat UI
- Themed museum guide assistant instructions

## Setup

1. Install Node.js 18 or newer.
2. Copy `.env.example` to `.env`.
3. Add your OpenAI API key to `.env`.
4. Install dependencies:

```bash
npm install
```

5. Start the app:

```bash
npm start
```

6. Open `http://localhost:3000`.

## Files

- `package.json`
- `.env.example`
- `server.js`
- `public/index.html`
- `public/style.css`
- `public/script.js`
