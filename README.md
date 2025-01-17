# Text Transformer

Transform unstructured text documents into structured JSON formats using GPT-4 with structured prompting. This framework is domain-agnostic, leveraging cutting-edge natural language processing techniques to provide flexible and scalable solutions for text data transformation.

---

## Abstract

The Text Transformer framework converts unstructured text into structured JSON representations using GPT-4. It employs structured prompting techniques, specifically In-Context Learning with Zero-Shot Learning, to guide the model. This approach eliminates the need for domain-specific fine-tuning or pre-labeled datasets. As a case study, recipes were used to demonstrate the framework's efficacy, converting unstructured texts into structured JSON datasets. The solution is generalizable across domains, enabling robust data extraction for diverse applications.

---

## Features

- **Dynamic Schema Support**: Allows users to define custom JSON schemas for diverse data extraction needs.
- **Domain-Agnostic**: Handles unstructured text from any field, including scientific, legal, and culinary domains.
- **Zero-Shot Learning**: Achieves high performance without requiring labeled training data.
- **Integrated Metadata**: Supports optional metadata attributes such as `description` and `nullable` for enhanced accuracy.
- **Strict Schema Adherence**: Ensures output JSON matches the provided schema exactly.
- **Dockerized Deployment**: Facilitates easy setup and scalability using Docker.

---

## Methodology

The framework utilizes GPT-4 with the following components:

- **In-Context Learning**: Provides explicit instructions for extracting and structuring data without examples.
- **Structured Prompting**: Constructs precise prompts that define task roles, input structures, and output requirements.
- **Metadata Integration**: Enhances field understanding using optional attributes, improving model reliability.

The structured prompting ensures that outputs are tailored to user-defined JSON schemas while adhering to strict formatting and type constraints.

---

## Configurations

The following configurations are used for GPT-4 to ensure deterministic and accurate outputs:

- **Model**: `gpt-4o-2024-08-06`
- **Temperature**: `0` (low randomness for deterministic results)
- **Top P**: `0` (focused sampling for precise responses)

Environment variables are managed in a `.env` file:
```plaintext
LLM_API_KEY=your_openai_api_key
LOG_LEVEL=DEBUG
JSON_DEPTH=5
```

---

## Input File Requirements

The framework accepts two input files:

### 1. Text File
- **Format**: `.txt`
- **Content**: Contains unstructured text for processing.
- **Example**:
```plaintext
Recipe for Pancakes:
Ingredients:
- 2 cups of flour
- 2 eggs
- 1 cup of milk
Steps:
1. Mix all ingredients.
2. Pour batter onto a hot griddle.
3. Flip when bubbles form.
```

### 2. JSON File
- **Format**: `.json`
- **Required Keys**:
  - **`response_schema`**: Defines the desired structure of the output JSON.
  - **`metadata`** (optional): Adds attributes like `description` and `nullable` to guide the model.

#### Example JSON Schema:
```json
{
    "response_schema": {
        "Recipe": {
            "recipe_id": "string",
            "title": "string",
            "ingredients": [
                {
                    "ingredient_id": "string",
                    "ingredient": "string",
                    "quantity": "number",
                    "unit": "string"
                }
            ],
            "steps": [
                {
                    "step_id": "string",
                    "instruction": "string"
                }
            ]
        }
    },
    "metadata": {
        "recipe_id": {
            "description": "A unique identifier for the recipe.",
            "nullable": true
        },
        "title": {
            "description": "The title of the recipe, or null if unavailable.",
            "nullable": true
        }
    }
}
```

---

## Prompt Structure

The framework uses a structured prompt to guide GPT-4 in processing unstructured text. Key elements of the prompt include:

1. **Role Definition**: "You are a data extraction assistant specializing in transforming unstructured text into structured JSON formats."
2. **Task Instructions**: Define the task clearly, specifying input and output expectations.
3. **Techniques**:
   - Named Entity Recognition (NER): Identify relevant entities in the text.
   - Relationship Extraction: Map relationships between identified entities.
4. **Handling Missing Data**: Ensure missing or ambiguous fields are returned as `null`.

#### Full Prompt Example:
```plaintext
You are a data extraction assistant specializing in transforming unstructured text into structured JSON formats.
Your task is to extract information from the provided text and organize it into a structured JSON format following the provided JSON schema.
Ensure all extracted information matches the structure and data types defined in the schema.

If a value for any key in the schema is not present in the text or cannot be confidently inferred, return null for that key.

Input:
- Text: A block of unstructured text.
- Schema: A JSON schema defining the expected keys and data types.

Output:
- A JSON object populated with data extracted from the text.
```

---

## Installation

### Prerequisites
- Python 3.9+
- Docker (optional for containerized deployment)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/TextTransformer.git
   cd TextTransformer
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the `.env` file:
   ```plaintext
   LLM_API_KEY=""
   JSON_DEPTH = 5 (According to OpenAI Documentation must be max 5 or lower)
   APP_NAME= Text Transformer
   APP_VERSION=1.0.0
   LOG_LEVEL=DEBUG
   ```

---

## Running the Project

### Using Docker
1. Build and start the Docker container:
   ```bash
   docker-compose up --build
   ```
2. Access the application at [http://localhost:8000](http://localhost:8000).

### Without Docker
1. Start the application:
   ```bash
   uvicorn app.main:app --reload
   ```
2. Access the API at [http://localhost:8000](http://localhost:8000).

---

## API Endpoints

### `POST /`
- **Description**: Converts unstructured text into structured JSON based on the provided schema.
- **Inputs**:
  - `text_file`: Unstructured text file (.txt).
  - `json_file`: JSON schema file (.json).
- **Output**: JSON object adhering to the provided schema.

### `POST /download`
- **Description**: Allows users to download the processed JSON as a file.

---

## Evaluation

The framework was evaluated against the RecipeNLP dataset using precision, recall, F1 score, and coverage rate:

- **Precision**: 0.712
- **Recall**: 0.964
- **F1 Score**: 0.797
- **Coverage Rate**: 0.989

The evaluation demonstrates the framework's effectiveness in extracting and structuring information.

---

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push to your fork.
4. Submit a pull request for review.

---

