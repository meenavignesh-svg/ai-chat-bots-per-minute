import OpenAI from 'openai';

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed.' });
  const apiKey = req.headers.authorization?.replace(/^Bearer\s+/i, '') || req.body?.apiKey;
  if (!apiKey) return res.status(400).json({ error: 'Enter an OpenAI API key for real AI mode.' });
  const messages = Array.isArray(req.body?.messages) ? req.body.messages.slice(-12) : [];
  const input = messages.map((message) => ({
    role: message.role === 'assistant' ? 'assistant' : 'user',
    content: String(message.content || '').slice(0, 2000)
  })).filter((message) => message.content);
  if (!input.length) return res.status(400).json({ error: 'Send at least one message.' });
  try {
    const client = new OpenAI({ apiKey });
    const response = await client.responses.create({
      model: 'gpt-4.1-mini',
      instructions: "You are Robot Gardener, a practical assistant for plant care, watering schedules, soil notes, and beginner garden plans.",
      input
    });
    return res.status(200).json({ reply: response.output_text || 'Please try again.' });
  } catch {
    return res.status(500).json({ error: 'The AI request failed. Check the API key and deployment.' });
  }
}
