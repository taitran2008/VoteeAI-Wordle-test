# Random Word Guessing Game API Requirements

## 🎯 Objective of the Game

You're playing a **Wordle-style** game where you guess a hidden **random target word**. 
## 📡 API Endpoint

### Get Random Word Guess

Retrieves the result of a user's guess for a randomly generated word.

- **URL:** `https://wordle.votee.dev:8000/random`
- **Method:** `GET`

## 3. Request

## 🔧 Parameters

You send your guess and optionally configure word size and randomness via **query parameters**:

| Parameter | Required? | Type    | Default | Description |
|----------|-----------|---------|---------|-------------|
| `guess`  | ✅ Yes     | string  | —       | Your guessed word (e.g., `"crane"`) |
| `size`   | ❌ No      | integer | `5`     | Length of the random target word (supports other sizes like 4, 6, etc.) |
| `seed`   | ❌ No      | integer | `null`  | If provided, ensures the same random word is generated each time (for reproducibility) |

### Example Requests

```bash
# Basic random word guess (5 letters, no seed)
curl -X GET 'https://wordle.votee.dev:8000/random?guess=table'

# Random word guess with custom size
curl -X GET 'https://wordle.votee.dev:8000/random?guess=string&size=6'

# Random word guess with seed for reproducible results
curl -X GET 'https://wordle.votee.dev:8000/random?guess=house&size=5&seed=12345'
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

1. **Start guessing** — pick a word (e.g., `"crane"`) and send it as `guess=crane`
2. **Read the response** — see which letters are correct/present/absent
3. **Refine your next guess** based on the clues
4. Repeat until you guess the word correctly (all letters return `"correct"`)

💡 *Tip: Use common starter words like "CRANE", "SLATE", or "AUDIO" to maximize early information.*

## 6. Seed Behavior

When a `seed` parameter is provided:

- The same seed will always generate the same target word for a given word size
- This allows for reproducible games and testing
- Multiple players can play the same word by using the same seed
- If no seed is provided, a truly random word is selected each time

## 7. Word Size Constraints

- **Minimum size**: 3 letters
- **Maximum size**: 8 letters
- **Default size**: 5 letters (when not specified)
- Invalid sizes will result in a 422 validation error

## 8. Error Handling

### Common Error Scenarios

| Error | Status | Description |
|-------|--------|-------------|
| Missing guess | 422 | The `guess` parameter is required |
| Invalid word size | 422 | Word size must be between 3-8 letters |
| Invalid guess length | 422 | Guess length must match the specified size |
| Invalid characters | 422 | Guess must contain only alphabetic characters |

### Example Error Response

```json
{
  "detail": [
    {
      "loc": ["query", "size"],
      "msg": "ensure this value is greater than or equal to 3",
      "type": "value_error.number.not_ge",
      "ctx": {"limit_value": 3}
    }
  ]
}
```

