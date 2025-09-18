# Word Guessing Game API Requirements

## 1. Objective

The primary objective of this API is to allow users to guess a hidden daily word.

## 2. API Endpoint

### Get Daily Word Guess

Retrieves the result of a user's guess for the daily word.

- **URL:** `https://wordle.votee.dev:8000/daily`
- **Method:** `GET`

## 3. Request

### Query Parameters

| Parameter | Type    | Required | Description                           |
| :-------- | :------ | :------- | :------------------------------------ |
| `guess`   | string  | Yes      | The user's guessed word.              |
| `size`    | integer | Yes      | The length of the word to be guessed. |

### Example Request

```bash
cURL -X GET 'https://wordle.votee.dev:8000/daily?guess=string&size=6'
```

## 4. Response

### Success Response (200 OK)

The API returns a JSON array of objects, where each object represents a letter in the guessed word.

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

### Result Key

The `result` field for each letter can have one of the following values:

- **`absent`**: The letter is not in the target word at all.
- **`present`**: The letter is in the target word, but in the wrong position.
- **`correct`**: The letter is in the correct position.

## 5. Winning Criteria

A guess is considered winning when the API returns a response where the `result` is `"correct"` for all letter slots.

## 6. Feedback Strategy

### Overview

The API response provides valuable feedback that can be used to construct intelligent regular expressions for subsequent guesses. By analyzing the `result` field for each letter position, you can build constraints that eliminate invalid words and guide the selection of better guesses.

### Regular Expression Construction

Based on the API response, construct regular expressions using the following strategy:

#### 6.1 Position Constraints (Correct Letters)

For letters marked as `"correct"`, fix them at their exact positions in the regular expression.

**Example:** If position 0 has letter 'h' marked as correct:

```regex
^h....$ (for a 5-letter word)
```

#### 6.2 Word Length Constraint

Use the `size` parameter to ensure the word matches the expected length.

**Example:** For a 5-letter word:

```regex
^.{5}$ 
```

#### 6.3 Exclusion Constraints (Absent Letters)

For letters marked as `"absent"`, ensure they are not included anywhere in the word using negative lookahead.

**Example:** Exclude letters 'a', 'g', 'c':

```regex
^(?!.*[agc]).*$
```

#### 6.4 Inclusion Constraints (Present Letters)

For letters marked as `"present"`, ensure they exist in the word but not at their guessed positions.

**Example:** Include letter 'e' but not at position 1, include letter 'l' but not at position 2:

```regex
^(?=.*e)(?=.*l)(?!.e...)(?!..l..).*$
```

#### 6.5 Complete Regular Expression Pattern

Combine all constraints into a comprehensive pattern:

1. **Word length**: Match exact character count
2. **Correct positions**: Fix known letters
3. **Absent letters**: Exclude completely
4. **Present letters**: Include but exclude from wrong positions
5. **Format constraints**: Lowercase letters only, no numbers

### Example: Word "hello" Feedback Strategy

Given the target word is "hello" and you've made several guesses, here's how to construct the regular expression:

#### Assumptions from API responses

- Word size: 5 characters
- Position 0: 'h' is `correct`
- Position 2: 'l' is `correct`
- Position 4: 'o' is `correct`
- Letters 'a', 'g', 'c', 'd', 'r', 'z' are `absent`
- Letters 'e', 'l' are `present` (but 'l' is already correctly placed)

#### Constructed Regular Expression

```regex
^h.l.o$
```

#### With all constraints combined

```regex
^(?=.*e)(?!.*[agcdrz])h[^agcdrz]l[^agcdrz]o$
```

#### Breakdown

- `^h.l.o$`: Positions 0, 2, 4 are fixed as 'h', 'l', 'o'
- `(?=.*e)`: Must contain letter 'e' somewhere
- `(?!.*[agcdrz])`: Must not contain any of these absent letters
- `[^agcdrz]`: Positions 1 and 3 cannot be any absent letters
- Implicit: lowercase letters only, no numbers

### Implementation Strategy

1. **Parse API Response**: Extract `correct`, `present`, and `absent` letters with their positions
2. **Build Position Map**: Create fixed positions for correct letters
3. **Generate Exclusions**: Compile list of absent letters
4. **Handle Present Letters**: Ensure inclusion while avoiding wrong positions
5. **Construct Regex**: Combine all constraints into a single pattern
6. **Validate Words**: Use the regex to filter potential next guesses

### Advanced Considerations

- **Duplicate Letters**: Handle cases where the same letter appears multiple times
- **Frequency Analysis**: Consider letter frequency in common words
- **Progressive Refinement**: Update regex after each guess to narrow possibilities
- **Word Lists**: Apply regex against dictionary of valid words

