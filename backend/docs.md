# API Documentation

## Overview

This document provides detailed documentation for the Trivia API. The API is designed to manage and retrieve trivia questions, categories and enable users to play quizzes. It follows RESTful principles and is built using Flask.

## Base URL

The base URL for the Trivia API is http://localhost:5000.

## Authentication

The Trivia API does not require authentication.

## Endpoints

### Get Categories

Endpoint
`GET '/categories'`

Description
Fetches a dictionary of categories where the keys are category ids and the values are category names.

Request Parameters
None

Response
An object with a single key, categories, containing key-value pairs of id: category_name.

Example Response
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

### Get Questions

Endpoint
`GET '/questions'`

Description
Fetches a list of trivia questions with pagination support. Each page contains up to 10 questions.

Request Parameters
- `page (optional)`: The page number for pagination (default is 1).
- `category_id (optional)` : Filter questions by category ID.

Response
- `questions`: A list of formatted questions.
- `total_questions`: The total number of questions.
- `categories`: A dictionary of all available categories.
- `current_category`: The current category (if filtered).

Example Response
```json
{
  "questions": [
    {
      "id": 1,
      "question": "What is the capital of France?",
      "answer": "Paris",
      "category": 3,
      "difficulty": 2
    },
    // Additional questions...
  ],
  "total_questions": 20,
  "categories": {
    "1": "Science",
    "2": "Art",
    // Other categories...
  },
  "current_category": "Geography"
}
```

### Delete Question

Endpoint
`DELETE '/questions/<question_id>'`

Description
Deletes a trivia question by it's ID.

Request Parameters
- `question_id`: The ID of the question to be deleted.

Response
- `success`: Boolean indicating if the deletion was successful.
- `deleted`: The ID of the deleted question.


Example Response
```json
{
  "success": true,
  "deleted": 1
}
```


### Search Questions

Endpoint
`POST '/questions/search'`

Description
Searches for trivia questions containing a specific term.

Request Parameters
- `searchTerm`: The search term to match against question texts.

Response
- `questions`: A list of formatted questions matching the search term.
- `total_questions`: The total number of matching questions.

Example Response
```json
{
  "questions": [
    {
      "id": 3,
      "question": "Who discovered penicillin?",
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3
    },
    // Other matching questions...
  ],
  "total_questions": 2,
  "current_category": null
}
```

### Get Questions by Category

Endpoint
`GET '/categories/<category_id>/questions'`

Description
Fetches trivia questions filtered by a specific category.

Request Parameters
- `category_id`: The ID of the category to filter questions.

Response

- `questions`: A list of formatted questions for the specified category.
- `total_questions`: The total number of questions for the category.
- `current_category`: The name of the filtered category.

Example Response

```json
{
  "questions": [
    {
      "id": 4,
      "question": "Who painted the Mona Lisa?",
      "answer": "Leonardo da Vinci",
      "category": 2,
      "difficulty": 2
    },
    // Other questions for the category...
  ],
  "total_questions": 8,
  "current_category": "Art"
}
```


### Play Quiz

Endpoint
`POST /quizzes`

Description
Generates a random trivia question for quiz play.

Request Parameters
`previous_questions`: A list of ID's of previous questions.
`quiz_category`: An object with id and type representing the quiz category.

Response
`success`: Boolean indicating if a question was retrieved.
`question`: A formatted question object

Example Response

```json
{
  "success": true,
  "question": {
    "id": 7,
    "question": "How many planets are in our solar system?",
    "answer": "8",
    "category": 1,
    "difficulty": 1
  }
}
```