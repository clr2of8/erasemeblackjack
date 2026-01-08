#!/usr/bin/env python3
"""
A basic command-line Blackjack game.
"""

import random


class Card:
    """Represents a playing card."""
    
    CARD_WIDTH = 9  # Width of the card interior
    CARD_HEIGHT = 7  # Number of lines in ASCII art
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    def value(self):
        """Returns the value of the card."""
        if self.rank in ['Jack', 'Queen', 'King']:
            return 10
        elif self.rank == 'Ace':
            return 11  # Aces are worth 11 by default, adjusted in hand calculation
        else:
            return int(self.rank)
    
    def _get_suit_symbol(self):
        """Returns the Unicode symbol for the card's suit."""
        symbols = {
            'Hearts': '♥',
            'Diamonds': '♦',
            'Clubs': '♣',
            'Spades': '♠'
        }
        return symbols.get(self.suit, '?')
    
    def _get_rank_display(self):
        """Returns the display string for the card's rank."""
        if self.rank == 'Jack':
            return 'J'
        elif self.rank == 'Queen':
            return 'Q'
        elif self.rank == 'King':
            return 'K'
        elif self.rank == 'Ace':
            return 'A'
        else:
            return self.rank
    
    def get_ascii_lines(self):
        """Returns the card as ASCII art lines."""
        suit_symbol = self._get_suit_symbol()
        rank_display = self._get_rank_display()
        
        # Adjust spacing based on rank length
        padding = ' ' * (self.CARD_WIDTH - 1 - len(rank_display))
        rank_line = f"{rank_display}{padding}"
        
        lines = [
            "┌─────────┐",
            f"│{rank_line}│",
            "│         │",
            f"│    {suit_symbol}    │",
            "│         │",
            f"│{rank_line}│",
            "└─────────┘"
        ]
        return lines


class Deck:
    """Represents a deck of cards."""
    
    def __init__(self):
        self.cards = []
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))
    
    def shuffle(self):
        """Shuffles the deck."""
        random.shuffle(self.cards)
    
    def deal(self):
        """Deals a card from the deck."""
        if not self.cards:
            # Reshuffle if deck is empty
            self.__init__()
            self.shuffle()
        return self.cards.pop()


class Hand:
    """Represents a hand of cards."""
    
    def __init__(self):
        self.cards = []
    
    def add_card(self, card):
        """Adds a card to the hand."""
        self.cards.append(card)
    
    def get_value(self):
        """Calculates the value of the hand."""
        value = 0
        aces = 0
        
        for card in self.cards:
            value += card.value()
            if card.rank == 'Ace':
                aces += 1
        
        # Adjust for aces if value is over 21
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        
        return value
    
    def display(self, hide_first=False):
        """Displays the hand as ASCII art."""
        # Create a hidden card ASCII art
        hidden_card_lines = [
            "┌─────────┐",
            "│░░░░░░░░░│",
            "│░░░░░░░░░│",
            "│░░░░░░░░░│",
            "│░░░░░░░░░│",
            "│░░░░░░░░░│",
            "└─────────┘"
        ]
        
        # Collect all card line arrays
        card_lines_list = []
        
        if hide_first:
            # Add hidden card
            card_lines_list.append(hidden_card_lines)
            # Add visible cards
            for card in self.cards[1:]:
                card_lines_list.append(card.get_ascii_lines())
        else:
            # Add all cards
            for card in self.cards:
                card_lines_list.append(card.get_ascii_lines())
        
        # Print cards side by side
        if card_lines_list:
            for line_index in range(Card.CARD_HEIGHT):
                line_parts = []
                for card_lines in card_lines_list:
                    line_parts.append(card_lines[line_index])
                print("  " + "  ".join(line_parts))
        
        # Print value if not hiding
        if not hide_first:
            print(f"  Value: {self.get_value()}")


class BlackjackGame:
    """Represents a Blackjack game."""
    
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
    
    def play(self):
        """Plays a round of Blackjack."""
        print("\n" + "="*50)
        print("Welcome to Blackjack!")
        print("="*50)
        
        # Shuffle and deal
        self.deck.shuffle()
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        
        # Show initial hands
        print("\nDealer's hand:")
        self.dealer_hand.display(hide_first=True)
        
        print("\nYour hand:")
        self.player_hand.display()
        
        # Check for player blackjack
        player_blackjack = self.player_hand.get_value() == 21
        dealer_blackjack = self.dealer_hand.get_value() == 21
        
        if player_blackjack and dealer_blackjack:
            print("\nDealer's hand:")
            self.dealer_hand.display()
            print("\nBoth have Blackjack! It's a tie!")
            return
        elif player_blackjack:
            print("\nBlackjack! You win!")
            return
        elif dealer_blackjack:
            print("\nDealer's hand:")
            self.dealer_hand.display()
            print("\nDealer has Blackjack! You lose.")
            return
        
        # Player's turn
        while True:
            choice = input("\nWould you like to (h)it or (s)tand? ").lower()
            
            if choice == 'h':
                self.player_hand.add_card(self.deck.deal())
                print("\nYour hand:")
                self.player_hand.display()
                
                if self.player_hand.get_value() > 21:
                    print("\nBust! You lose.")
                    return
                elif self.player_hand.get_value() == 21:
                    break
            elif choice == 's':
                break
            else:
                print("Invalid choice. Please enter 'h' or 's'.")
        
        # Dealer's turn
        print("\nDealer's turn...")
        print("\nDealer's hand:")
        self.dealer_hand.display()
        
        while self.dealer_hand.get_value() < 17:
            print("\nDealer hits...")
            self.dealer_hand.add_card(self.deck.deal())
            self.dealer_hand.display()
        
        # Determine winner
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()
        
        print("\n" + "="*50)
        if dealer_value > 21:
            print("Dealer busts! You win!")
        elif player_value > dealer_value:
            print(f"You win! ({player_value} vs {dealer_value})")
        elif player_value < dealer_value:
            print(f"Dealer wins! ({dealer_value} vs {player_value})")
        else:
            print(f"It's a tie! ({player_value})")
        print("="*50)


def main():
    """Main function to run the game."""
    while True:
        game = BlackjackGame()
        game.play()
        
        play_again = input("\nWould you like to play again? (y/n) ").lower()
        if play_again != 'y':
            print("\nThanks for playing!")
            break


if __name__ == "__main__":
    main()
