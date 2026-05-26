import OpenAI from 'openai';

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });
  const visitorKey = req.headers.authorization?.replace(/^Bearer\s+/i, '') || req.body?.apiKey;
  const apiKey = process.env.OPENAI_API_KEY || visitorKey;
  if (!apiKey) return res.status(400).json({ error: 'OpenAI API key required for real AI mode.' });
  const input = String(req.body?.input || '').slice(0, 8000);
  const client = new OpenAI({ apiKey });
  const response = await client.responses.create({
    model: process.env.OPENAI_MODEL || 'gpt-4.1-mini',
    instructions: "You are SourceProof AI RAG Answer Auditor, a premium AI product for AI teams shipping retrieval apps for regulated or enterprise users. Workflow: paste answer plus source notes, detect unsupported claims, score citation quality, and produce remediation tasks. Provide structured analysis, score, risks, and next actions. Include safety caveats when needed.",
    input
  });
  res.status(200).json({ reply: response.output_text || 'No analysis returned.' });
}
