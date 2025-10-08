import google.generativeai as genai
import random
import os

# ===== CONFIGURATION =====
# Make sure you set your API key before running:
# export GEMINI_API_KEY="your_gemini_key_here"
# Get your API key at https://aistudio.google.com/api-keys
genai.configure(api_key=os.getenv("GEMINI_API_KEY") or "YOUR_GEMINI_KEY_HERE")

# ===== HANGMAN ASCII ART =====
HANGMAN_PICS = [
    """
       +---+
       |   |
           |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    =========
    """
]

# ===== GEMINI WORD FETCH =====
def get_word_from_gemini(difficulty):
    """
    Fetch a random English word from Gemini based on difficulty.
    """
    prompt = f"Give me one random English word suitable for a {difficulty} level Hangman game. Only reply with the word itself, no explanation."

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        word = response.text.strip().lower()
        word = ''.join(ch for ch in word if ch.isalpha())

        if not word:
            raise ValueError("Invalid word received.")
        return word

    except Exception as e:
        print(f"⚠️ Gemini request failed: {e}")
        fallback = {
            "easy": ["apple", "ball", "rain", "cat"],
            "medium": ["planet", "silver", "garden", "bridge"],
            "hard": ["microscope", "philosophy", "abstraction", "quarantine"]
        }
        return random.choice(fallback[difficulty])


# ===== HELPER FUNCTIONS =====
def display_word(word, guessed_letters):
    """
    Displays a word with underscores in place of unguessed letters.

    Parameters
    ----------
    word : str
        The word to display.
    guessed_letters : set
        The set of letters that have been guessed.

    Returns
    -------
    str
        The word with underscores in place of unguessed letters.
    """

    return ' '.join(letter if letter in guessed_letters else '_' for letter in word)


# ===== MAIN GAME LOGIC =====
def play_hangman(word):
    """
    Play a game of Hangman with the given word.

    Parameters
    ----------
    word : str
        The word to play with.

    Returns
    -------
    None

    Notes
    -----
    The game will continue until the player either guesses the word
    or runs out of attempts (i.e., the Hangman is fully drawn).

    The player is prompted to enter a single letter at a time, and
    the game will display the current state of the Hangman and the
    word (with underscores in place of unguessed letters).

    If the player guesses a letter that is not in the word, the
    game will increment the wrong_guesses counter. If the player guesses
    a letter that is in the word, the game will display the correctly
    guessed letter in its correct position.

    If the player has guessed all the letters in the word, the game
    will end and display a winning message. If the player has run out
    of attempts, the game will end and display a losing message.
    """
    attempts = len(HANGMAN_PICS) - 1
    guessed_letters = set()
    wrong_guesses = 0

    print("\n🎯 Let’s play Hangman!")

    while wrong_guesses < attempts:
        print(HANGMAN_PICS[wrong_guesses])
        print(f"Word: {display_word(word, guessed_letters)}")
        print(f"Guessed: {' '.join(sorted(guessed_letters)) or '-'}")
        print(f"Attempts left: {attempts - wrong_guesses}\n")

        guess = input("Enter a letter: ").lower().strip()

        if not guess.isalpha() or len(guess) != 1:
            print("❌ Please enter a single valid letter.\n")
            continue
        if guess in guessed_letters:
            print("⚠️ You already guessed that letter.\n")
            continue

        guessed_letters.add(guess)

        if guess not in word:
            print("💀 Wrong guess!\n")
            wrong_guesses += 1
        else:
            print("✅ Correct guess!\n")

        if all(letter in guessed_letters for letter in word):
            print(HANGMAN_PICS[wrong_guesses])
            print(f"\n🎉 You WON! The word was: '{word.upper()}'\n")
            return

    print(HANGMAN_PICS[-1])
    print(f"\n☠️ Game Over! The word was '{word.upper()}'.\n")


# ===== ENTRY POINT =====
def main():
    """
    Main entry point for the Gemini Hangman game.

    Prompts the user to select the difficulty of the word to be guessed,
    fetches a word from Gemini based on the selected difficulty, and
    starts a new game of Hangman.

    """
    print("===== 🕹️ GEMINI HANGMAN =====")
    print("Choose difficulty: easy | medium | hard")

    difficulty = input("Enter difficulty: ").lower().strip()
    if difficulty not in ["easy", "medium", "hard"]:
        print("Invalid difficulty, defaulting to 'easy'")
        difficulty = "easy"

    print(f"\nFetching a {difficulty} word from Gemini...")
    word = get_word_from_gemini(difficulty)

    play_hangman(word)


if __name__ == "__main__":
    main()
