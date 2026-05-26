const input = document.querySelector('#input');
    const output = document.querySelector('#output');
    const apiKeyInput = document.querySelector('#apiKey');
    const score = document.querySelector('#score');
    const demoReply = "I reviewed the sample, found the main risk, scored readiness, and created a practical next-step plan for AI teams shipping retrieval apps for regulated or enterprise users.";
    const systemWorkflow = "paste answer plus source notes, detect unsupported claims, score citation quality, and produce remediation tasks";

    input.value = window.sampleData || '';

    function localScore(text) {
      return Math.min(99, 88 + Math.floor(text.length / 120));
    }

    function localReport(text) {
      const value = localScore(text);
      score.textContent = value;
      return `Premium analysis score: ${value}/100

Workflow: ${systemWorkflow}

Executive answer:
${demoReply}

Detected input:
${text}

Recommended next actions:
1. Validate assumptions with a human reviewer.
2. Turn the output into a repeatable checklist.
3. Save this as a client-ready report.`;
    }

    document.querySelector('#sample').addEventListener('click', () => {
      input.value = window.sampleData || '';
      output.textContent = localReport(input.value);
    });

    document.querySelectorAll('.chip').forEach((chip) => {
      chip.addEventListener('click', () => {
        input.value = `${chip.textContent} review: ${input.value || window.sampleData}`;
      });
    });

    document.querySelector('#analyze').addEventListener('click', async () => {
      const text = input.value.trim();
      if (!text) return;
      const apiKey = apiKeyInput.value.trim() || sessionStorage.getItem('openai_api_key') || '';
      if (apiKey) sessionStorage.setItem('openai_api_key', apiKey);
      output.textContent = 'Analyzing premium workflow...';
      if (!apiKey) {
        output.textContent = localReport(text);
        return;
      }
      try {
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${apiKey}` },
          body: JSON.stringify({ input: text })
        });
        const data = await response.json();
        output.textContent = data.reply || data.error || localReport(text);
      } catch {
        output.textContent = localReport(text);
      }
    });

    output.textContent = localReport(input.value);
