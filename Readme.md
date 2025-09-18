# AI Wordle Solver

This project contains a collection of Python scripts that use an AI model to automatically solve various Wordle-style guessing games. The AI intelligently uses feedback from each guess to construct a regular expression, narrowing down the possibilities for the next guess until the word is solved.

## ✨ Features

- **AI-Powered Guessing**: Leverages a generative AI model to make intelligent word guesses based on constraints.
- **Dynamic Regex Generation**: Builds and refines a regular expression after each attempt to zero in on the correct word.
- **Multiple Game Modes**: Supports three different Wordle game APIs:
    1.  Daily static word
    2.  Randomly generated word
    3.  User-specified target word
- **Configurable**: Easily change the AI model or word parameters via a configuration file and command-line arguments.

## ⚙️ Setup

Follow these steps to get the project running.

### 1. Install Dependencies

This project requires Python 3. Make sure you have it installed. Then, install the necessary packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

The scripts require an API key for the Gemini AI model. You need to create a `.env` file in the root of the project.

1.  Create a file named `.env`.
2.  Add the following content to the file, replacing `YOUR_API_KEY_HERE` with your actual Gemini API key.

```env
# .env

# Your Google Gemini API Key
GEMINI_API_KEY="YOUR_API_KEY_HERE"

# The model to use for generating guesses
GEMINI_MODEL_NAME="gemini-2.5-pro"
```

## 🤖 AI Model

This project has been developed and tested using Google's **`gemini-2.5-pro`** model. The model name is configured in the `.env` file via the `GEMINI_MODEL_NAME` variable.

## 🚀 Usage

There are three different scripts, each corresponding to a different game mode.

### 1. Daily Word Game (`guess_1.py`)

This script is for playing against the single "daily" word. You must specify the length of the word.

**Command:**
```bash
python guess_1.py --size <word_length>
```

**Example (for a 5-letter word):**
```bash
python guess_1.py --size 5
```

### 2. Random Word Game (`guess_2.py`)

This script plays against a randomly generated word. The word size is optional (defaults to 5), and you can provide a seed for reproducible games.

**Command:**
```bash
python guess_2.py [--size <word_length>] [--seed <number>]
```

**Examples:**
```bash
# Play a standard 5-letter random game
python guess_2.py

# Play a 6-letter random game
python guess_2.py --size 6

# Play a reproducible 6-letter game using a seed
python guess_2.py --size 6 --seed 12345
```

### 3. Specific Word Game (`guess_3.py`)

This script allows you to play against a specific target word of your choice. This is useful for testing or creating custom challenges.

**Command:**
```bash
python guess_3.py --word <target_word>
```

**Example:**
```bash
# Play against the word "apple"
python guess_3.py --word apple
```
