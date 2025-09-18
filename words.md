# Word Guessing Game API - Specific Word Endpoint

## 1. Objective

This API endpoint allows users to guess against a specific selected word, providing flexibility to test guesses against any word rather than just the daily word.

## 2. API Endpoint

### Guess Against Specific Word

Retrieves the result of a user's guess against a specified target word.

- **URL:** `https://wordle.votee.dev:8000/word/{word}`
- **Method:** `GET`

## 3. Request

### Path Parameters

| Parameter | Type   | Required | Description                                    |
| :-------- | :----- | :------- | :--------------------------------------------- |
| `word`    | string | Yes      | The target word to guess against.              |

### Query Parameters

| Parameter | Type   | Required | Description              |
| :-------- | :----- | :------- | :----------------------- |
| `guess`   | string | Yes      | The user's guessed word. |

### Example Request

```bash
curl -X GET 'https://wordle.votee.dev:8000/word/string?guess=string'
```

### Additional Examples

```bash
# Guess "hello" against target word "world"
curl -X GET 'https://wordle.votee.dev:8000/word/world?guess=hello'

# Guess "test" against target word "tests"
curl -X GET 'https://wordle.votee.dev:8000/word/tests?guess=test'
```

## 4. Response

### Success Response (200 OK)

The API returns a JSON array of objects, where each object represents a letter in the guessed word compared against the target word.

### Example Response Body

```json
[
  {
    "slot": 0,
    "guess": "s",
    "result": "correct"
  },
  {
    "slot": 1,
    "guess": "t",
    "result": "present"
  },
  {
    "slot": 2,
    "guess": "r",
    "result": "absent"
  },
  {
    "slot": 3,
    "guess": "i",
    "result": "absent"
  },
  {
    "slot": 4,
    "guess": "n",
    "result": "absent"
  },
  {
    "slot": 5,
    "guess": "g",
    "result": "absent"
  }
]
```

### Error Response (422 Validation Error)

When the request parameters are invalid or missing, the API returns a validation error.

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

### Response Fields

Each letter object in the response contains:

| Field    | Type    | Description                                    |
| :------- | :------ | :--------------------------------------------- |
| `slot`   | integer | The position of the letter (0-indexed).       |
| `guess`  | string  | The guessed letter at this position.          |
| `result` | string  | The result of the guess (see below).          |

### Result Values

The `result` field for each letter can have one of the following values:

- **`absent`**: The letter is not in the target word at all.
- **`present`**: The letter is in the target word, but in the wrong position.
- **`correct`**: The letter is in the correct position.

## 5. Winning Criteria

A guess is considered winning when the API returns a response where the `result` is `"correct"` for all letter slots.

## 6. Use Cases

This endpoint is useful for:

- **Testing specific words**: Validate guesses against known words for testing purposes
- **Educational purposes**: Practice with specific word patterns or difficulty levels
- **Game development**: Build custom word guessing games with predefined word sets
- **Algorithm testing**: Test word-guessing algorithms against controlled word sets

## 7. Notes

- The target word length is determined by the `{word}` path parameter
- The guess word should typically match the length of the target word for meaningful results
- Word comparison is case-sensitive (verify with API documentation)
- Special characters and numbers may or may not be supported (verify with API documentation)