# Socratic: A Context-Aware AI Reasoning Framework

Socratic is a sophisticated AI reasoning system that combines advanced language models with memory management and Socratic dialogue techniques to create more thoughtful and context-aware AI interactions.

## Features

- 🧠 **Context-Aware Reasoning**: Maintains conversation history and leverages past interactions
- 🤔 **Socratic Dialogue**: Generates insightful questions to probe deeper understanding
- 📝 **Advanced Judgment**: Evaluates reasoning quality and compares different approaches
- 🎨 **Creative Generation**: Produces creative outputs while maintaining coherence
- 💾 **Memory Integration**: Persistent memory storage and retrieval using Mem0

## Installation

```bash
pip install socratic
```

## Quick Start

```python
from socratic import ReasoningGame, ReasoningJudge

# Initialize components
game = ReasoningGame()
judge = ReasoningJudge()

# Ask a question
question = "What is artificial intelligence?"
response = game.forward(question)

# Evaluate the response
evaluation = judge.forward(response.answer)
print(f"Response quality: {evaluation.score}")
```

## Configuration

Create a `.env` file based on `.env.example`:

```env
OPENAI_API_KEY=your_openai_api_key_here
MEM0_API_KEY=your_mem0_api_key_here
```

## Documentation

For detailed documentation, visit [docs/](docs/).

## Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/socratic.git
cd socratic
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.
