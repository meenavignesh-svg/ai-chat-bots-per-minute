import OpenAI from 'openai';

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed.' });
  const visitorKey = req.headers.authorization?.replace(/^Bearer\s+/i, '') || req.body?.apiKey;
  const apiKey = process.env.OPENAI_API_KEY || visitorKey;
  if (!apiKey) return res.status(400).json({ error: 'OpenAI API key required for real AI mode.' });
  const messages = Array.isArray(req.body?.messages) ? req.body.messages.slice(-12) : [];
  const input = messages.map((m) => ({ role: m.role === 'assistant' ? 'assistant' : 'user', content: String(m.content || '').slice(0, 2400) }));
  const client = new OpenAI({ apiKey });
  const response = await client.responses.create({ model: process.env.OPENAI_MODEL || 'gpt-4.1-mini', instructions: "You are Local LLM Coach Idea Sprint, a premium practical chatbot for local model testing and prompt-result notes; practical idea sprint support; clear next-step guidance. Use the Practice Coach interaction style and keep answers crisp, specific, and action-oriented.", input });
  return res.status(200).json({ reply: response.output_text || 'Please try again.' });
}
