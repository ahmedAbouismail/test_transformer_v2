# Text Transformer v2

Transform unstructured text documents into structured JSON formats using GPT-4 with few-shot prompting. This framework is domain-agnostic, leveraging cutting-edge natural language processing techniques to provide flexible and scalable solutions for text data transformation.

---

## Abstract

The Text Transformer framework converts unstructured text into structured JSON representations using GPT-4. In this second version, the framework employs few-shot prompting techniques instead of the previous zero-shot approach, providing even better accuracy and reliability. This approach eliminates the need for domain-specific fine-tuning or pre-labeled datasets while improving output quality through examples. As demonstrated in our case study, recipes were successfully converted from unstructured texts into structured JSON datasets. The solution is generalizable across domains, enabling robust data extraction for diverse applications.

---

## Features

- **Dynamic Schema Support**: Allows users to define custom JSON schemas for diverse data extraction needs.
- **Few-Shot Learning**: Achieves higher performance by providing examples that guide the model.
- **Domain-Agnostic**: Handles unstructured text from any field, including scientific, legal, and culinary domains.
- **Strict Schema Adherence**: Ensures output JSON matches the provided schema exactly.
- **Schema Validation**: Validates output against a specified validation schema.
- **Dockerized Deployment**: Facilitates easy setup and scalability using Docker.

---

## Methodology

The framework utilizes GPT-4 with the following components:

- **Few-Shot Learning**: Provides explicit examples of input-output pairs to guide the model in processing new texts.
- **Structured Prompting**: Constructs precise prompts that define task roles, input structures, and output requirements.

The few-shot approach significantly improves performance by showing the model concrete examples of the expected transformation, reducing errors and improving consistency across different inputs.

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
EXAMPLES_SEPARATOR====  # Separator used in examples file
```

---

## Input File Requirements

The framework now accepts four input files:

### 1. Examples File (NEW)
- **Format**: `.txt`
- **Content**: Contains examples of unstructured text and their corresponding structured JSON outputs.
- **Structure**: Examples are separated by the separator specified in the environment variable `EXAMPLES_SEPARATOR` (default: `===`).
- **Purpose**: Provides few-shot examples to guide the model's extraction process.
- **Example**
```plaintext
Recipe Title: artichoke dip

2  cans or jars artichoke hearts1  c. mayonnaise1  c. Parmesan cheese
Drain artichokes and chop.  Mix with mayonnaise and Parmesan cheese.  After well mixed, bake, uncovered, for 20 to 30 minutes at 350°.  Serve with crackers.

{
    "Recipe": {
        "recipe_id": "2",
        "title": "Artichoke Dip",
        "ingredients": [ {... }],
        "steps": [ { ... } ]
    }
}

===

Recipe Title: broccoli dip for crackers

16  oz. sour cream1  pkg. dry vegetable soup mix10  oz. pkg. frozen chopped broccoli, thawed and drained4 to 6  oz. Cheddar cheese, grated
Mix together sour cream, soup mix, broccoli and half of cheese.  Sprinkle remaining cheese on top.  Bake at 350° for 30 minutes, uncovered.  Serve hot with vegetable crackers.


{
    "Recipe": {
        "recipe_id": "3",
        "title": "Broccoli Dip For Crackers",
        "ingredients": [{ ... }],
        "steps": [{ ... }]
    }
}

```

### 2. Text File
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

### 3. JSON Schema File
- **Format**: `.json`
- **Creation Method**: Generated using the [GPT Schema Builder](https://github.com/your-username/gpt-schema-builder) tool
- **Purpose**: Defines the structure that extracted data should follow

### 4. Validation Schema File (NEW)
- **Format**: `.json`
- **Purpose**: Provides a schema for validating the output JSON structure.
- **Content**: Standard JSON Schema format (not the OpenAI-specific format used in the json_file).
- **Note**: This file contains the same schema structure as the JSON schema file but in standard JSON Schema format rather than OpenAI's response format structure.
---

## Prompt Structure
The framework uses a structured prompt with examples to guide GPT-4, as implemented in the `prompt_generator.py` file:

1. **System Message**: Defines the assistant's role as a data extraction specialist and provides detailed instructions:
   ```
   "You are a data extraction assistant specializing in transforming unstructured text into structured JSON formats. 
   Your task is to extract information from the provided text and organize it into a structured JSON format following 
   the provided JSON schema. Ensure all extracted information matches the structure and data types defined in the schema.

   Before extracting information, apply named entity recognition to identify relevant entities and relationship extraction 
   techniques to map connections between entities. Use these insights to populate the JSON schema fields accurately.

   If a value for any key in the schema is not present in the text or cannot be confidently inferred, return null for that key."
   ```

2. **Assistant Message**: Contains examples of text inputs and their corresponding JSON outputs, helping the model understand the expected transformation patterns.

3. **User Message**: Contains the new unstructured text that needs to be processed.
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
   EXAMPLES_SEPARATOR====
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
  - `examples_file`: File containing few-shot examples (.txt).
  - `text_file`: Unstructured text file (.txt).
  - `json_file`: JSON schema file (.json) created with the GPT Schema Builder.
  - `validation_schema_file`: Schema for validating the output (.json).
- **Output**: JSON object adhering to the provided schema.

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