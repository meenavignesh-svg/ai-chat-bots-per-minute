# Premium Chatbot Factory

This factory creates two high-value AI chatbot products per day through GitHub Actions.

## Rule

No filler demos. Each run must produce a product-grade AI assistant with:

- real user problem
- paid-product positioning
- polished browser demo
- API route using the OpenAI SDK
- AI-generated product strategy when keys are present
- sample data
- screenshot asset
- product specification
- deployment instructions
- validation gate

Run manually:

```bash
python tools/chatbot_factory/generate.py
python tools/chatbot_factory/validate_premium.py generated-product.txt
```

Manual trigger note: start the clean premium product pipeline.
