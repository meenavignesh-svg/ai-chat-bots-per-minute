# Beat Producer Chatbot

A browser-demo chatbot with an optional real AI mode for Vercel. The demo works immediately in the browser with built-in themed replies. Real AI mode asks each visitor for their own OpenAI API key, stores it only in `sessionStorage`, and sends it to the Vercel serverless route for each request.

## Browser Demo

Open `public/index.html` from the repository file view or download the folder and open it in a browser. The demo replies are built in, so no setup is required for preview.

## Optional Real AI Mode

Real AI mode needs a deployed Vercel public URL. Localhost is not used for sharing. After deployment, visitors can enter their own OpenAI API key in the page.

## Deploy To Vercel

1. Import `meenavignesh-svg/ai-chat-bots-per-minute` into Vercel.
2. Set the root directory to `ai-chatbots/beat-producer-chatbot-2026-05-24-1541z`.
3. Deploy.
4. Share the Vercel URL.

## Files

- `package.json`
- `vercel.json`
- `api/chat.js`
- `public/index.html`
- `public/style.css`
- `public/script.js`
