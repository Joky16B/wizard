"""
Trick module for the Wizard card game.

This module defines the Trick class for managing a single trick in the Wizard game.
"""

from typing import Dict, List, Optional, Tuple

from .apprentice import Apprentice
from .card import Card, CardType, CardColor


class Trick:
    """
    Represents a single trick in the Wizard card game.
    
    A trick consists of each apprentice playing one card. The trick is won by
    the apprentice who played the highest card according to the game rules.
    """
    
    def __init__(self, leading_apprentice: Apprentice, trump_color: Optional[CardColor] = None):
        """
        Initialize a new trick.
        
        Args:
            leading_apprentice: The apprentice who leads the trick
            trump_color: The current trump color (if any)
        """
        self.leading_apprentice = leading_apprentice
        self.trump_color = trump_color
        self.cards_played: Dict[Apprentice, Card] = {}
        self.leading_color: Optional[CardColor] = None
        self.winner: Optional[Apprentice] = None
        self.is_complete = False
    
    def play_card(self, apprentice: Apprentice, card: Card) -> bool:
        """
        Record a card played by an apprentice.
        
        Args:
            apprentice: The apprentice playing the card
            card: The card being played
            
        Returns:
            True if the play is valid, False otherwise
            
        Raises:
            ValueError: If the trick is already complete or the apprentice has already played
        """
        if self.is_complete:
            raise ValueError("Cannot play card: trick is already complete")
        
        if apprentice in self.cards_played:
            raise ValueError(f"Apprentice {apprentice.name} has already played a card in this trick")
        
        # If this is the first card played, set the leading color
        if not self.cards_played:
            # If the first card is a Regular card, set the leading color
            # Wizard and Fool don't set leading color
            if card.card_type == CardType.REGULAR:
                self.leading_color = card.color
        elif self.leading_color is None and len(self.cards_played) == 1:
            # If the first card was a Fool or Wizard, the second card sets the leading color
            # (unless it's also a Fool or Wizard)
            if card.card_type == CardType.REGULAR:
                self.leading_color = card.color
        
        # Record the card played
        self.cards_played[apprentice] = card
        
        return True
    
    def determine_winner(self) -> Optional[Apprentice]:
        """
        Determine the winner of the trick.
        
        Returns:
            The apprentice who won the trick, or None if the trick is not complete
            
        Note:
            The winner is determined by the following rules:
            1. The first Wizard card played wins the trick
            2. If no Wizard is played, the highest card of the trump color wins
            3. If no trump is played, the highest card of the leading color wins
            4. If only Fools are played, the first Fool wins
        """
        if not self.cards_played:
            return None
        
        # Check if only Fools were played
        if all(card.card_type == CardType.FOOL for card in self.cards_played.values()):
            # The first Fool played wins (first key in the dictionary)
            return next(iter(self.cards_played))
        
        # Find the first Wizard played
        for apprentice, card in self.cards_played.items():
            if card.card_type == CardType.WIZARD:
                self.winner = apprentice
                return apprentice
        
        # If no Wizard, find the highest trump card
        highest_card = None
        highest_apprentice = None
        
        for apprentice, card in self.cards_played.items():
            if card.card_type == CardType.FOOL:
                continue  # Fools never win unless only Fools are played
                
            if highest_card is None:
                highest_card = card
                highest_apprentice = apprentice
            elif card.is_higher_than(highest_card, self.trump_color, self.leading_color):
                highest_card = card
                highest_apprentice = apprentice
        
        self.winner = highest_apprentice
        return highest_apprentice
    
    def get_played_cards(self) -> List[Tuple[Apprentice, Card]]:
        """
        Get all cards played in this trick with their associated apprentices.
        
        Returns:
            A list of (apprentice, card) tuples in the order they were played
        """
        return list(self.cards_played.items())
    
    def is_valid_play(self, apprentice: Apprentice, card: Card) -> bool:
        """
        Check if playing the given card is valid according to the rules.
        
        Args:
            apprentice: The apprentice playing the card
            card: The card being played
            
        Returns:
            True if the play is valid, False otherwise
        """
        # If the leading color is not set yet, any card can be played
        if self.leading_color is None:
            return True
        
        # Wizard and Fool cards can always be played
        if card.card_type in (CardType.WIZARD, CardType.FOOL):
            return True
        
        # If the first card was a Wizard, any card can be played
        first_card = next(iter(self.cards_played.values())) if self.cards_played else None
        if first_card and first_card.card_type == CardType.WIZARD:
            return True
        
        # Otherwise, must follow the leading color if possible
        if card.color != self.leading_color:
            # Check if the apprentice has any cards of the leading color
            has_leading_color = apprentice.can_follow_color(self.leading_color)
            if has_leading_color:
                return False  # Must follow leading color
        
        return True
    
    def complete_trick(self) -> Optional[Apprentice]:
        """
        Mark the trick as complete and determine the winner.
        
        Returns:
            The apprentice who won the trick
        """
        self.is_complete = True
        winner = self.determine_winner()
        if winner:
            winner.win_trick()
        return winner
    
    def __str__(self) -> str:
        """Return a string representation of the trick."""
        cards_str = ", ".join(f"{a.name}: {c}" for a, c in self.cards_played.items())
        return f"Trick with {len(self.cards_played)} cards played: {cards_str}"
