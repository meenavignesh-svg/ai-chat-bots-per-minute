import 'dotenv/config';
import express from 'express';
import OpenAI from '@openai/openai';

const app = express();
const port = process.env.PORT || 3000;
const model = process.env.OPENAI_MODEL || 'gpt-5.2';
const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

app.use(express.json({ limit: '1mb' }));
app.use(express.static('public'));

app.post('/api/chat', async (req, res) => {
  try {
    if (!process.env.OPENAI_API_KEY) {
      return res.status(500).json({ error: 'OPENAI_API_KEY is missing. Add it to your .env file.' });
    }

    const messages = Array.isArray(req.body.messages) ? req.body.messages : [];
    const cleanMessages = messages
      .filter((message) => message && typeof message.content === 'string')
      .slice(-12)
      .map((message) => ({
        role: message.role === 'assistant' ? 'assistant' : 'user',
        content: message.content.slice(0, 2000)
      }));

    if (cleanMessages.length === 0) {
      return res.status(400).json({ error: 'Send at least one message.' });
    }

    const response = await client.responses.create({
      model,
      instructions: 'You are Lab Mentor, a careful AI assistant for students and makers. Give practical explanations, ask clarifying questions when needed, avoid unsafe lab instructions, and keep answers concise and encouraging.',
      input: cleanMessages
    });

    res.json({ reply: response.output_text || 'I could not produce a reply. Try again with more detail.' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'The AI request failed. Check your API key, model, and server logs.' });
  }
});

app.listen(port, () => {
  console.log(`Lab Mentor Chatbot is running at http://localhost:${port}`);
});
