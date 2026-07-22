import random


def get_valid_guess(low, high):
    """Prompt the user until they enter a valid integer within range."""
    while True:
        raw = input(f"Enter your guess ({low}-{high}): ").strip()
        try:
            guess = int(raw)
        except ValueError:
            print("That's not a valid number. Try again.")
            continue
        if guess < low or guess > high:
            print(f"Please enter a number between {low} and {high}.")
            continue
        return guess


def play_round(low=1, high=100, max_attempts=7):
    secret_number = random.randint(low, high)
    attempts = 0

    print(f"\nI'm thinking of a number between {low} and {high}.")
    print(f"You have {max_attempts} attempts. Good luck!\n")

    while attempts < max_attempts:
        guess = get_valid_guess(low, high)
        attempts += 1

        if guess == secret_number:
            print(f"\n🎉 Correct! The number was {secret_number}.")
            print(f"You got it in {attempts} attempt(s).")
            return True
        elif guess < secret_number:
            print("Higher! ⬆️\n")
        else:
            print("Lower! ⬇️\n")

        remaining = max_attempts - attempts
        if remaining > 0:
            print(f"Attempts remaining: {remaining}")

    print(f"\n😢 Out of attempts! The number was {secret_number}.")
    return False


def main():
    print("=" * 40)
    print("   WELCOME TO THE NUMBER GUESSING GAME")
    print("=" * 40)

    wins = 0
    rounds = 0

    while True:
        play_round()
        rounds += 1

        result = input("\nPlay again? (y/n): ").strip().lower()
        if result != "y":
            break

    print(f"\nThanks for playing! You played {rounds} round(s).")


if __name__ == "__main__":
    main()