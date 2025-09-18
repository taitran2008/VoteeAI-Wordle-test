import time
import os
import re
import requests
from dotenv import load_dotenv

def construct_regex_pattern(word_size: int, correct_positions: dict = None, 
                           present_letters: set = None, absent_letters: set = None,
                           present_exclusions: dict = None) -> str:
    """
    Constructs a regular expression pattern based on Wordle feedback strategy.
    
    Based on the feedback strategy from guess.md:
    1. Position Constraints: Fix correct letters at their positions
    2. Word Length Constraint: Ensure exact word length
    3. Exclusion Constraints: Exclude absent letters
    4. Inclusion Constraints: Include present letters but not at wrong positions
    
    Args:
        word_size: The exact number of letters in the word
        correct_positions: Dict mapping position (0-indexed) to confirmed letters
        present_letters: Set of letters that are in the word but position unknown
        absent_letters: Set of letters that are not in the word
        present_exclusions: Dict mapping letters to a set of positions where they are known not to be.
        
    Returns:
        Regular expression pattern as a string
    """
    if not word_size or word_size <= 0:
        return ""
    
    # Initialize sets for processing
    correct_positions = correct_positions or {}
    present_letters = present_letters or set()
    absent_letters = absent_letters or set()
    present_exclusions = present_exclusions or {}
    
    # Build the position pattern (e.g., "h.l.o" for hello with known positions)
    position_pattern = []
    for i in range(word_size):
        if i in correct_positions:
            # Fixed letter at this position
            position_pattern.append(re.escape(correct_positions[i]))
        else:
            # Unknown letter at this position. The negative lookahead will handle exclusions.
            position_pattern.append(".")
    
    base_pattern = "".join(position_pattern)
    
    # Build constraints
    constraints = []
    
    # 1. Inclusion constraints for present letters
    for letter in present_letters:
        if letter not in correct_positions.values():  # Don't double-constrain already correct letters
            constraints.append(f"(?=.*{re.escape(letter)})")
    
    # 2. Exclusion constraints for absent letters
    if absent_letters:
        constraints.append(f"(?!.*[{''.join(sorted(map(re.escape, absent_letters)))}])")
    
    # 3. Present letter position exclusions
    for letter, positions in present_exclusions.items():
        for pos in positions:
            # Create a pattern like "(?!.e...)" to exclude 'e' from position 1
            exclusion_pattern = "." * pos + re.escape(letter) + "." * (word_size - pos - 1)
            constraints.append(f"(?!{exclusion_pattern})")

    # Combine all constraints with the base pattern
    if constraints:
        full_pattern = f"^{''.join(constraints)}{base_pattern}$"
    else:
        full_pattern = f"^{base_pattern}$"
    
    return full_pattern

def validate_word_against_pattern(word: str, pattern: str) -> bool:
    """
    Validates if a word matches the constructed regex pattern.
    
    Args:
        word: The word to validate
        pattern: The regex pattern to match against
        
    Returns:
        True if the word matches the pattern, False otherwise
    """
    if not word or not pattern:
        return False
    
    try:
        return bool(re.match(pattern, word.lower()))
    except re.error:
        # Invalid regex pattern
        return False

def guess_word(word_size: int = None, correct_positions: dict = None, 
               present_letters: set = None, absent_letters: set = None, present_exclusions: dict = None) -> str:
    """
    Calls the Gemini API to guess an English word based on given criteria using regex patterns.

    Args:
        word_size: The exact number of letters in the word.
        correct_positions: Dict mapping position (0-indexed) to confirmed letters.
        present_letters: Set of letters that are in the word but position unknown.
        absent_letters: Set of letters that are not in the word.
        present_exclusions: Dict mapping letters to a set of positions where they are known not to be.

    Returns:
        The guessed word as a string, or an error message.
    """
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")
    if not api_key:
        return "Error: GEMINI_API_KEY not found in .env file."

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key,
    }
    # Convert parameters to proper types for regex construction
    absent_letters = absent_letters or set()
    
    # Construct regex pattern using the feedback strategy
    regex_pattern = construct_regex_pattern(
        word_size=word_size,
        correct_positions=correct_positions,
        present_letters=present_letters,
        absent_letters=absent_letters,
        present_exclusions=present_exclusions
    )
    prompt_lines = [
        "You are playing Wordle. Guess a single meaningful English word — not placeholder text or random characters (e.g., avoid “sfsdf”, “fvfdhg”, etc.) that matches the given pattern.",
        "Respond with only the word itself, without any explanation, punctuation, or other text. e.g., respond with 'apple' not 'The word is apple.'"
    ]
    
    # Add regex pattern as the primary constraint
    if regex_pattern:
        prompt_lines.append(f"- Word must match this regex pattern: {regex_pattern}")
    else:
        # Fallback for edge cases where no pattern is generated
        if word_size:
            prompt_lines.append(f"- Word length: exactly {word_size} letters")
    
    # Regex pattern already encodes all learned constraints from previous guesses
    
    if len(prompt_lines) <= 2:  # Only base instructions
        return "Error: At least one criterion must be provided."

    prompt = "\n".join(prompt_lines)
    print(f"🤖 Regex Pattern: {regex_pattern}")

    # Gemini API format
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    try:
        # Use Gemini API endpoint
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        
        # Make a single API call - let the caller handle retries
        response = requests.post(api_url, headers=headers, json=data)
        
        if response.status_code == 429:
            return "Error: Rate limit hit (429) - please retry"
        elif response.status_code == 400:
            try:
                error_details = response.json()
                return f"Error: Bad Request (400) - {error_details.get('error', {}).get('message', 'Unknown error')}"
            except:
                return f"Error: Bad Request (400) - {response.text} {api_key}"
        elif response.status_code == 403:
            return "Error: Forbidden (403) - Check your API key permissions"
        elif response.status_code == 404:
            return f"Error: Model not found (404) - Model '{model}' may not exist"
        
        response.raise_for_status()  # Raise for other HTTP errors

        result = response.json()
        # Extract text from Gemini response format
        word = result['candidates'][0]['content']['parts'][0]['text'].strip()
        
        # Validate against regex pattern (using lowercase for validation)
        if regex_pattern and not validate_word_against_pattern(word.lower(), regex_pattern):
            return f"Error: AI suggested word '{word.upper()}' that doesn't match the required pattern {regex_pattern}"
        
        # Return in uppercase for consistency
        return word.upper()

    except requests.exceptions.RequestException as e:
        return f"Error making API call: {e}"
    except (KeyError, IndexError) as e:
        return f"Error parsing API response: {e}"

