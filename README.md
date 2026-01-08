# erasemeblackjack

A simple command-line Blackjack game written in Python.

## How to Play

Run the game with:
```bash
python3 blackjack.py
```

### Game Rules
- The goal is to get as close to 21 as possible without going over
- Face cards (Jack, Queen, King) are worth 10 points
- Aces are worth 11 points, but automatically adjust to 1 if needed to avoid busting
- Number cards are worth their face value
- The dealer must hit until reaching 17 or higher
- You win if:
  - Your hand value is higher than the dealer's without going over 21
  - The dealer busts (goes over 21)
  - You get a Blackjack (21 on first two cards)
- You lose if:
  - You bust (go over 21)
  - The dealer's hand value is higher than yours

### Commands
- `h` - Hit (take another card)
- `s` - Stand (keep your current hand)
- `y` - Play again
- `n` - Quit the game

Enjoy!