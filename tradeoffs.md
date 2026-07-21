# Design Tradeoffs and Reasoning

## Model Choice: GPT-5-mini
I chose **GPT-5-mini** as the brain for this agent. It provides an excellent balance between speed, cost, and intelligence. For a resume screening task, it is more than capable of understanding the nuances of skills and experience without the latency and cost of a larger model like GPT-5.5.

## Scoring Method: LLM-as-a-Judge
Instead of using traditional keyword matching or simple vector similarity (like Cosine Similarity on embeddings), I opted for **LLM-as-a-Judge**.
- **Pros:** It understands the *context* of experience. For example, it knows that "Built RAG pipelines" is highly relevant to "AI Research," even if the JD doesn't explicitly use the word "pipeline."
- **Cons:** It is slightly slower than pure mathematical similarity and depends on the model's internal reasoning.

## Data Parsing
The agent supports PDF, DOCX, and TXT files using `pypdf` and `python-docx`.
- **Tradeoff:** I used basic text extraction. For production, I would add a more robust OCR layer (like Tesseract or Azure Form Recognizer) to handle scanned resumes or complex multi-column layouts.

## Limitations and Future Improvements
1. **Context Window:** While GPT-5-mini has a large window, processing 100+ resumes at once would require a more sophisticated batching or RAG approach to avoid hitting token limits.
2. **Bias Mitigation:** LLMs can inherit biases from their training data. In a real-world scenario, I would implement anonymization (removing names, gender, etc.) before screening to ensure fairness.
3. **Structured Extraction:** Currently, the agent extracts data into a JSON format. Adding a validation layer (like Pydantic) would make the output even more reliable for downstream systems.
