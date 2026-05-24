import 'dotenv/config';
import express from 'express';
import OpenAI from 'openai';

const app = express();
const port = process.env.PORT || 3000;
const model = process.env.OPENAI_MODEL || 'gpt-4.1-mini';
const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

app.use(express.json({ limit: '1mb' }));
app.use(express.static('public'));

app.post('/api/chat', async (req, res) => {
  try {
    if (!process.env.OPENAI_API_KEY) {
      return res.status(500).json({ error: 'OPENAI_API_KEY is missing. Add it to your .env file.' });
    }

    const messages = Array.isArray(req.body.messages) ? req.body.messages : [];
    const input = messages
      .filter((message) => message && typeof message.content === 'string')
      .slice(-12)
      .map((message) => ({
        role: message.role === 'assistant' ? 'assistant' : 'user',
        content: message.content.slice(0, 2000)
      }));

    if (input.length === 0) {
      return res.status(400).json({ error: 'Send at least one message.' });
    }

    const response = await client.responses.create({
      model,
      instructions: 'You are City Chef, a practical AI cooking assistant for quick meals, budget cooking, substitutions, and kitchen planning. Ask about allergies when relevant, avoid unsafe food advice, and keep answers clear and useful.',
      input
    });

    res.json({ reply: response.output_text || 'I could not produce a reply. Please try again.' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'The AI request failed. Check your API key, model, and server logs.' });
  }
});

app.listen(port, () => {
  console.log(`City Chef Chatbot is running at http://localhost:${port}`);
});
