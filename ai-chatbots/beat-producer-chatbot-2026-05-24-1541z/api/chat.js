import OpenAI from 'openai';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed.' });
  }

  try {
    const apiKey = req.headers.authorization?.replace(/^Bearer\s+/i, '') || req.body?.apiKey;
    if (!apiKey || typeof apiKey !== 'string') {
      return res.status(400).json({ error: 'Enter your OpenAI API key before using real AI mode.' });
    }

    const messages = Array.isArray(req.body?.messages) ? req.body.messages : [];
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

    const client = new OpenAI({ apiKey });
    const response = await client.responses.create({
      model: 'gpt-4.1-mini',
      instructions: 'You are Beat Producer, a practical AI music production assistant for beat ideas, song structure, drums, basslines, melodies, and mix notes. Give creative but actionable suggestions, avoid copyrighted lyric imitation, and keep responses concise.',
      input
    });

    return res.status(200).json({ reply: response.output_text || 'I could not produce a reply. Please try again.' });
  } catch (error) {
    console.error(error);
    return res.status(500).json({ error: 'The AI request failed. Check the API key and deployment.' });
  }
}
