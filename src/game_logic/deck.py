"""
Deck module for the Wizard card game.

This module defines the Deck class for managing the collection of cards in the Wizard game.
"""

import random
from typing import List, Optional, Tuple

from .card import Card, CardType, CardColor


class Deck:
    """
    Represents the deck of cards in the Wizard card game.
    
    The deck consists of 60 cards:
    - 52 regular cards (13 cards in each of 4 colors, values 1-13)
    - 4 Wizard cards
    - 4 Fool cards
    """
    
    def __init__(self):
        """Initialize a new deck with all 60 cards in order."""
        self.cards: List[Card] = []
        self._initialize_cards()
    
    def _initialize_cards(self):
        """Create all 60 cards for the deck."""
        # Add regular cards (1-13) in each color
        for color in [CardColor.HUMANS, CardColor.ELVES, CardColor.DWARVES, CardColor.GIANTS]:
            for value in range(1, 14):  # 1 to 13
                self.cards.append(Card(CardType.REGULAR, color, value))
        
        # Add 4 Wizard cards
        for _ in range(4):
            self.cards.append(Card(CardType.WIZARD))
        
        # Add 4 Fool cards
        for _ in range(4):
            self.cards.append(Card(CardType.FOOL))
    
    def shuffle(self, seed: Optional[int] = None):
        """
        Shuffle the deck of cards.
        
        Args:
            seed: Optional random seed for reproducible shuffling
        """
        if seed is not None:
            random.seed(seed)
        random.shuffle(self.cards)
    
    def deal(self, num_cards: int) -> List[Card]:
        """
        Deal a specified number of cards from the top of the deck.
        
        Args:
            num_cards: Number of cards to deal
            
        Returns:
            A list of dealt cards
            
        Raises:
            ValueError: If there are not enough cards left in the deck
        """
        if num_cards > len(self.cards):
            raise ValueError(f"Cannot deal {num_cards} cards. Only {len(self.cards)} left in deck.")
        
        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt_cards
    
    def deal_to_players(self, num_players: int, cards_per_player: int) -> Tuple[List[List[Card]], List[Card]]:
        """
        Deal cards to players for a round of Wizard.
        
        Args:
            num_players: Number of players in the game
            cards_per_player: Number of cards to deal to each player
            
        Returns:
            A tuple containing:
                - A list of hands (each hand is a list of cards)
                - The remaining cards in the deck
                
        Raises:
            ValueError: If there are not enough cards for the requested deal
        """
        total_cards_needed = num_players * cards_per_player
        if total_cards_needed > len(self.cards):
            raise ValueError(
                f"Cannot deal {cards_per_player} cards to {num_players} players. "
                f"Only {len(self.cards)} left in deck."
            )
        
        # Deal cards to each player
        hands = []
        for _ in range(num_players):
            hands.append(self.deal(cards_per_player))
        
        return hands, self.cards
    
    def draw_trump_card(self) -> Optional[Card]:
        """
        Draw the top card from the deck to determine the trump color.
        
        Returns:
            The drawn card, or None if the deck is empty
        """
        if not self.cards:
            return None
        
        trump_card = self.cards[0]
        self.cards = self.cards[1:]
        return trump_card
    
    def __len__(self) -> int:
        """Return the number of cards left in the deck."""
        return len(self.cards)
    
    def __str__(self) -> str:
        """Return a string representation of the deck."""
        return f"Deck with {len(self.cards)} cards remaining"
