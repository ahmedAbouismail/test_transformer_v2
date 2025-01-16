# Text Transformer

The Text Transformer framework is designed to convert unstructured text into structured JSON using advanced prompting techniques with GPT-4. This domain-agnostic solution provides an API endpoint to transform any text into structured data based on user-defined schemas.

---

## Table of Contents
- [Text Transformer](#text-transformer)
- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Evaluation](#evaluation)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Key Features

- **Structured Prompting**: Utilizes In-Context Learning and Zero-Shot Learning for text transformation.
- **Domain-Agnostic**: Can handle any type of unstructured text input.
- **JSON Schema Integration**: Allows users to define the desired output structure in JSON format.
- **API-Driven**: Exposes a simple API for seamless integration.
- **Recipe Dataset Creation**: Generates fully structured datasets from semi-structured ones, such as the RecipeNLP dataset.

---

## How It Works

### Workflow
1. **Input**:
   - **Text File**: Contains unstructured text data.
   - **JSON Schema**: Defines the desired structure of the output.
2. **Processing Pipeline**:
   - `InputFileParser()`: Parses input files and converts them into Python-friendly formats.
   - `ResponseSchemaGenerator()`: Prepares a GPT-compatible schema.
   - `PromptGenerator()`: Creates a structured prompt for GPT.
   - `GPTService()`: Sends the prompt to GPT-4 for text transformation.
   - `CompletionParser()`: Extracts and parses the GPT response into JSON.
   - `JSONValidator()`: Ensures the output matches the defined schema.
3. **Output**:
   - A JSON object containing structured information from the input text.

---

## Installation

### Prerequisites
- Python 3.10+
- Docker (optional for containerized deployment)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/text-transformer.git
   cd text-transformer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file and provide your configurations:
     ```dotenv
     LLM_API_KEY=your_api_key_here
     LOG_LEVEL=DEBUG
     JSON_DEPTH=5
     ```

4. Run the application:
   ```bash
   uvicorn app.text_structuring:router --reload --host 0.0.0.0 --port 8000
   ```

Alternatively, use Docker:
   ```bash
   docker-compose up --build
   ```

---

## Usage

### API Endpoint
Send a POST request to `/` with the following:
- **Input Files**:
  - `text_file`: A `.txt` file containing unstructured text.
  - `json_file`: A `.json` file defining the response schema.

#### Example Request (using `curl`):
```bash
curl -X POST "http://localhost:8000/" \
  -F "text_file=@sample.txt" \
  -F "json_file=@schema.json"
```

#### Example Response:
```json
{
  "title": "Chocolate Cake",
  "ingredients": ["flour", "sugar", "cocoa powder"],
  "instructions": "Mix ingredients and bake."
}
```

---

## Evaluation

The framework was evaluated by comparing its outputs with a gold-standard dataset derived from the RecipeNLP dataset. The evaluation pipeline involves:

1. `RecipeScraper()`: Extracts raw recipe texts from RecipeNLP links.
2. `PrepareGoldStandardDataset()`: Converts semi-structured RecipeNLP data into fully structured datasets.
3. `TextTransformer()`: Processes unstructured text using the framework's API.
4. `Evaluate()`: Compares the results against the gold-standard dataset.

---

## Contributing

We welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes and commit: `git commit -m "Add feature-name"`.
4. Push to your branch: `git push origin feature-name`.
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contact

For questions or feedback, please reach out to [your email/contact].

