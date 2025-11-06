# DSPy Reference Examples

Real-world examples demonstrating DSPy's unique capabilities in pharma/medtech applications.

## Example 1: Ozempic Complaint Classification

Automatically classify incoming reports about Novo Nordisk's Ozempic (semaglutide) as either:
- **Adverse Events** (patient safety issues, medical reactions)
- **Product Complaints** (device defects, quality issues)

### Why DSPy?

Unlike traditional prompt engineering (LangChain, manual prompting), DSPy **automatically optimizes** your classifier by:
- Learning the best few-shot examples from your training data
- Optimizing prompt instructions for your specific task
- Improving accuracy without manual prompt tweaking

### Requirements

- Python 3.8+
- OpenAI API key (for gpt-4o-mini)

### Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set your OpenAI API key:**

Option A - Environment variable:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

Option B - Create `.env` file:
```bash
cp .env.example .env
# Edit .env and add your API key
```

### Running the Example

```bash
python ozempic_classifier.py
```

This will:
1. Load 20 training examples and 20 test examples
2. Evaluate baseline (unoptimized) classifier
3. Run DSPy optimization (~2-3 minutes)
4. Evaluate optimized classifier
5. Show before/after comparison
6. Save optimized model to `ozempic_classifier_optimized.json`

### Example Output

```
🔵 BASELINE PERFORMANCE (No Optimization)
Accuracy: 14/20 = 70.0%

🔄 OPTIMIZING WITH DSPy...
✓ Optimization complete!

🟢 OPTIMIZED PERFORMANCE
Accuracy: 18/20 = 90.0%

FINAL RESULTS SUMMARY
Baseline Accuracy:   70.0%
Optimized Accuracy:  90.0%
Improvement:         +20.0%
```

### Project Structure

```
dspy-reference-examples/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .env.example                       # API key template
├── data_generator.py                  # Synthetic Ozempic complaint data
├── ozempic_classifier.py              # Main DSPy classifier
└── ozempic_classifier_optimized.json  # Saved optimized model (after running)
```

### What Makes This Example Realistic?

The training data includes actual scenarios pharma companies face:

**Adverse Events:**
- Serious reactions (pancreatitis, thyroid issues)
- GI side effects (nausea, vomiting)
- Allergic reactions
- Injection site reactions

**Product Complaints:**
- Pen mechanism failures
- Dose counter defects
- Packaging damage
- Cold chain failures
- Labeling errors

### How DSPy Optimization Works

1. **Baseline:** Uses zero-shot prompting with just the signature description
2. **Optimization:** DSPy tries different combinations of:
   - Few-shot examples (which training examples work best?)
   - Prompt instructions (how to describe the task?)
3. **Result:** Automatically finds the best configuration for your specific classification task

### Cost Estimate

- Training: ~$0.10-0.20 (one-time optimization)
- Inference: ~$0.001 per classification

### Next Steps

This example demonstrates classification only. Future examples will add:
- Extraction of structured data from adverse events
- Multi-stage pipelines (classify → extract → assess severity)
- Model portability (switching between OpenAI, Anthropic, local models)

### License

MIT License - See LICENSE file for details
