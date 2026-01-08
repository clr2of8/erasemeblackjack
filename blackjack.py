#!/usr/bin/env python3
"""
A basic command-line Blackjack game.
"""

import random


class Card:
    """Represents a playing card."""
    
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
        """Displays the hand."""
        if hide_first:
            print(f"  [Hidden]")
            for card in self.cards[1:]:
                print(f"  {card}")
        else:
            for card in self.cards:
                print(f"  {card}")
            print(f"  Value: {self.get_value()}")


class BlackjackGame:
    """Represents a Blackjack game."""
    
    def __init__(self, balance=1000):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.balance = balance
        self.bet = 0
    
    def play(self):
        """Plays a round of Blackjack."""
        print("\n" + "="*50)
        print("Welcome to Blackjack!")
        print("="*50)
        
        # Display balance and place bet
        print(f"\nYour balance: ${self.balance}")
        
        if self.balance <= 0:
            print("\nYou're out of money! Game over.")
            return False
        
        # Get bet amount (default to $100)
        while True:
            bet_input = input(f"\nEnter your bet amount (default $100): ").strip()
            if bet_input == "":
                self.bet = 100
            else:
                try:
                    bet_value = float(bet_input)
                    self.bet = int(bet_value)
                except ValueError:
                    print("Invalid bet. Please enter a number.")
                    continue
            
            if self.bet <= 0:
                print("Bet must be positive.")
                continue
            elif self.bet > self.balance:
                print(f"You don't have enough money. Your balance is ${self.balance}.")
                continue
            else:
                break
        
        print(f"Bet placed: ${self.bet}")
        
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
            print(f"Your bet of ${self.bet} is returned.")
            return True
        elif player_blackjack:
            winnings = round(self.bet * 1.5)  # Blackjack pays 3:2, rounded to nearest dollar
            self.balance += winnings
            print(f"\nBlackjack! You win ${winnings}!")
            print(f"Your new balance: ${self.balance}")
            return True
        elif dealer_blackjack:
            print("\nDealer's hand:")
            self.dealer_hand.display()
            self.balance -= self.bet
            print(f"\nDealer has Blackjack! You lose ${self.bet}.")
            print(f"Your new balance: ${self.balance}")
            return True
        
        # Player's turn
        while True:
            choice = input("\nWould you like to (h)it or (s)tand? ").lower()
            
            if choice == 'h':
                self.player_hand.add_card(self.deck.deal())
                print("\nYour hand:")
                self.player_hand.display()
                
                if self.player_hand.get_value() > 21:
                    self.balance -= self.bet
                    print(f"\nBust! You lose ${self.bet}.")
                    print(f"Your new balance: ${self.balance}")
                    return True
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
            self.balance += self.bet
            print(f"Dealer busts! You win ${self.bet}!")
            print(f"Your new balance: ${self.balance}")
        elif player_value > dealer_value:
            self.balance += self.bet
            print(f"You win ${self.bet}! ({player_value} vs {dealer_value})")
            print(f"Your new balance: ${self.balance}")
        elif player_value < dealer_value:
            self.balance -= self.bet
            print(f"Dealer wins! You lose ${self.bet}. ({dealer_value} vs {player_value})")
            print(f"Your new balance: ${self.balance}")
        else:
            print(f"It's a tie! ({player_value})")
            print(f"Your bet of ${self.bet} is returned.")
        print("="*50)
        return True


def main():
    """Main function to run the game."""
    game = BlackjackGame()
    
    while True:
        continue_game = game.play()
        
        if not continue_game or game.balance <= 0:
            if game.balance <= 0:
                print("\nYou're out of money! Thanks for playing!")
            else:
                print("\nThanks for playing!")
            break
        
        play_again = input("\nWould you like to play again? (y/n) ").lower()
        if play_again != 'y':
            print(f"\nYou're leaving with ${game.balance}. Thanks for playing!")
            break
        
        # Reset hands for next round
        game.player_hand = Hand()
        game.dealer_hand = Hand()


if __name__ == "__main__":
    main()
