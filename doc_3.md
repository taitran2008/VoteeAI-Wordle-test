# Word Guessing Game API Requirements

## 🎯 Objective of the Game

You're playing a **Wordle-style** game where you guess against a **specific target word**.

## 📡 API Endpoint

### Guess Word

Retrieves the result of a user's guess against a selected word.

- **URL:** `https://wordle.votee.dev:8000/word/{word}`
- **Method:** `GET`

## 3. Request

## 🔧 Parameters

You send your guess via **query parameters** and specify the target word in the **path**:

### Path Parameters

| Parameter | Required? | Type    | Description |
|----------|-----------|---------|-------------|
| `word`   | ✅ Yes     | string  | The target word to guess against (e.g., `"crane"`) |

### Query Parameters

| Parameter | Required? | Type    | Description |
|----------|-----------|---------|-------------|
| `guess`  | ✅ Yes     | string  | Your guessed word (e.g., `"table"`) |

### Example Requests

```bash
# Basic word guess against specific target word
curl -X GET 'https://wordle.votee.dev:8000/word/crane?guess=table'

# Another example with different target and guess
curl -X GET 'https://wordle.votee.dev:8000/word/house?guess=horse'
```

## 4. Response

### Success Response (200 OK)

The API returns a JSON array of objects, where each object represents a letter in the guessed word.

### Example Response Body

```json
[
  {
    "slot": 0,
    "guess": "h",
    "result": "correct"
  },
  {
    "slot": 1,
    "guess": "o",
    "result": "present"
  },
  {
    "slot": 2,
    "guess": "u",
    "result": "absent"
  },
  {
    "slot": 3,
    "guess": "s",
    "result": "absent"
  },
  {
    "slot": 4,
    "guess": "e",
    "result": "correct"
  }
]
```

### Validation Error Response (422)

When the request parameters are invalid, the API returns a validation error.

```json
{
  "detail": [
    {
      "loc": ["query", "guess"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Result Key

The `result` field for each letter can have one of the following values:

- **`absent`**: The letter is not in the target word at all.
- **`present`**: The letter is in the target word, but in the wrong position.
- **`correct`**: The letter is in the correct position.

## 🎮 How to Play Step-by-Step

1. **Choose a target word** — specify the word you want to guess against in the URL path (e.g., `/word/crane`)
2. **Make your guess** — send your guess word as the `guess` query parameter
3. **Read the response** — see which letters are correct/present/absent
4. **Refine your next guess** based on the clues
5. Repeat until you guess the word correctly (all letters return `"correct"`)

💡 *Tip: This endpoint is perfect for playing against known words or creating custom challenges.*

## 6. Word Length Constraints

- The guess word must be the same length as the target word
- Both target and guess words must contain only alphabetic characters
- Word length is determined by the target word specified in the path

## 7. Error Handling

### Common Error Scenarios

| Error | Status | Description |
|-------|--------|-------------|
| Missing guess | 422 | The `guess` parameter is required |
| Length mismatch | 422 | Guess length must match target word length |
| Invalid characters | 422 | Both target and guess must contain only alphabetic characters |
| Missing word path | 404 | The target word must be specified in the URL path |

### Example Error Response

```json
{
  "detail": [
    {
      "loc": ["query", "guess"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## 8. Comparison with Random Word Endpoint

This endpoint differs from the `/random` endpoint in that:

- **Target word is predetermined**: You specify exactly which word to guess against
- **No size parameter needed**: Word length is determined by the target word
- **No seed parameter**: Since the target word is fixed, no randomization is involved
- **Perfect for custom games**: Allows players to create specific word challenges
