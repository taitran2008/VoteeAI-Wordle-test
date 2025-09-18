import requests
import argparse
import time
from word_guesser import guess_word

def call_wordle_api(guess: str, target_word: str):
    """
    Calls the specific Wordle game API to get feedback on a guess against a target word.
    """
    url = f"https://wordle.votee.dev:8000/word/{target_word.lower()}"
    params = {"guess": guess.lower()}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: API call to {url} failed: {e}")
        return None

def play_game(target_word: str):
    """
    Main logic for the Wordle AI player.
    """
    word_size = len(target_word)
    if word_size <= 0:
        print("Error: Target word must have a positive length.")
        return

    # Initialize constraints
    correct_positions = {}
    present_letters = set()
    absent_letters = set()
    present_exclusions = {}
    
    attempts = 0
    current_guess = ""

    while True:
        attempts += 1
        print(f"\n{'='*10} Attempt {attempts} {'='*10}")

        # Get a guess from the AI, with retries
        print("🤖 Thinking of the next word...")
        
        next_guess = None
        max_retries = 15
        for i in range(max_retries):
            guess_attempt = guess_word(
                word_size=word_size,
                correct_positions=correct_positions,
                present_letters=present_letters,
                absent_letters=absent_letters,
                present_exclusions=present_exclusions
            )
            
            if guess_attempt and not guess_attempt.startswith("Error:"):
                next_guess = guess_attempt
                break  # Got a valid guess
            
            print(f"Warning: AI failed to provide a valid guess (Attempt {i + 1}/{max_retries}). Retrying...")
            print(f"Details: {guess_attempt}")
            time.sleep(1)  # Wait a moment before retrying

        if not next_guess:
            print(f"Error: Could not generate a valid guess after {max_retries} attempts. Aborting.")
            break  # Abort the main game loop
        
        current_guess = next_guess
        print(f"🧠 My guess is: {current_guess.upper()}")

        # Call the Wordle API with the new guess
        feedback = call_wordle_api(current_guess, target_word)
        if not feedback:
            print("Could not get feedback from the API. Aborting.")
            break
        
        print(f"API Feedback: {feedback}")

        # Check for a win
        if all(item['result'] == 'correct' for item in feedback):
            print(f"\n🎉 Success! The word is '{current_guess.upper()}'.")
            print(f"Guessed in {attempts} attempts.")
            break

        # Process feedback to update constraints for the next round
        # Create a map of letters in the current guess to their results
        guess_feedback_map = {}
        for item in feedback:
            letter = item['guess']
            result = item['result']
            if letter not in guess_feedback_map:
                guess_feedback_map[letter] = []
            guess_feedback_map[letter].append(result)

        for item in feedback:
            slot = item['slot']
            letter = item['guess']
            result = item['result']

            if result == 'correct':
                correct_positions[slot] = letter
                # If the letter was previously considered 'present', it's now confirmed.
                if letter in present_letters:
                    present_letters.remove(letter)
                # Its position is known, so remove it from the exclusion list.
                if letter in present_exclusions:
                    del present_exclusions[letter]
            
            elif result == 'present':
                # The letter is in the word, but not in this slot.
                # Add to 'present' only if not already in a confirmed correct position.
                if letter not in correct_positions.values():
                    present_letters.add(letter)
                
                # Add this incorrect position to the exclusion list for this letter.
                if letter not in present_exclusions:
                    present_exclusions[letter] = set()
                present_exclusions[letter].add(slot)

            elif result == 'absent':
                # A letter is truly absent only if all its occurrences in the guess are 'absent'
                # and it's not already known to be 'correct' or 'present'.
                if all(r == 'absent' for r in guess_feedback_map.get(letter, [])):
                    if letter not in correct_positions.values() and letter not in present_letters:
                        absent_letters.add(letter)
        
        print("\nUpdating constraints for the next guess...")
        print(f"Correct positions: {correct_positions}")
        print(f"Present letters: {present_letters}")
        print(f"Absent letters: {absent_letters}")
        print(f"Present Exclusions: {present_exclusions}")
        time.sleep(1) # Pause for readability

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="An AI-powered CLI to solve a Wordle puzzle against a specific target word.",
        epilog="Example: python guess_3.py --word crane"
    )
    parser.add_argument(
        "--word", 
        type=str, 
        required=True, 
        help="The target word to guess against."
    )
    args = parser.parse_args()
    
    play_game(args.word)
