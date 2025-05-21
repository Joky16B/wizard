"""
Card module for the Wizard card game.

This module defines the Card class and related constants for the Wizard card game.
"""

from enum import Enum, auto
from typing import Optional


class CardType(Enum):
    """Enum representing the types of cards in the Wizard game."""
    REGULAR = auto()
    WIZARD = auto()
    FOOL = auto()


class CardColor(Enum):
    """Enum representing the colors of cards in the Wizard game."""
    HUMANS = "blue"     # Blue
    ELVES = "green"     # Green
    DWARVES = "red"     # Red
    GIANTS = "yellow"   # Yellow
    NONE = None         # No color (for Wizard and Fool cards)


class Card:
    """
    Represents a card in the Wizard card game.
    
    A card can be a regular numbered card (1-13) in one of four colors,
    a Wizard card ("Z"), or a Fool card ("N").
    """
    
    def __init__(self, card_type: CardType, color: Optional[CardColor] = None, value: Optional[int] = None):
        """
        Initialize a new card.
        
        Args:
            card_type: The type of card (REGULAR, WIZARD, or FOOL)
            color: The color of the card (required for REGULAR cards, None for special cards)
            value: The value of the card (1-13 for REGULAR cards, None for special cards)
        
        Raises:
            ValueError: If the card parameters are invalid
        """
        self.card_type = card_type
        
        # Validate and set card properties based on type
        if card_type == CardType.REGULAR:
            if color is None or color == CardColor.NONE:
                raise ValueError("Regular cards must have a color")
            if value is None or not (1 <= value <= 13):
                raise ValueError("Regular cards must have a value between 1 and 13")
            self.color = color
            self.value = value
        elif card_type in (CardType.WIZARD, CardType.FOOL):
            self.color = CardColor.NONE
            self.value = None
        else:
            raise ValueError(f"Invalid card type: {card_type}")
    
    @property
    def display_value(self) -> str:
        """Get the display value of the card."""
        if self.card_type == CardType.WIZARD:
            return "Z"
        elif self.card_type == CardType.FOOL:
            return "N"
        else:
            return str(self.value)
    
    def __str__(self) -> str:
        """Return a string representation of the card."""
        if self.card_type == CardType.WIZARD:
            return "Wizard (Z)"
        elif self.card_type == CardType.FOOL:
            return "Fool (N)"
        else:
            return f"{self.value} of {self.color.name}"
    
    def __repr__(self) -> str:
        """Return a detailed string representation of the card."""
        if self.card_type == CardType.REGULAR:
            return f"Card(CardType.REGULAR, CardColor.{self.color.name}, {self.value})"
        else:
            return f"Card(CardType.{self.card_type.name})"
    
    def is_higher_than(self, other: 'Card', trump_color: Optional[CardColor], led_color: Optional[CardColor]) -> bool:
        """
        Determine if this card is higher than another card in the context of a trick.
        
        Args:
            other: The card to compare against
            trump_color: The current trump color (or None if no trump)
            led_color: The color that was led in this trick
            
        Returns:
            True if this card is higher than the other card, False otherwise
        """
        # Wizard is always highest
        if self.card_type == CardType.WIZARD:
            return True
        if other.card_type == CardType.WIZARD:
            return False
        
        # Fool is always lowest
        if self.card_type == CardType.FOOL:
            return False
        if other.card_type == CardType.FOOL:
            return True
        
        # Both are regular cards
        if self.color == trump_color and other.color != trump_color:
            # This card is trump, other is not
            return True
        elif self.color != trump_color and other.color == trump_color:
            # Other card is trump, this is not
            return False
        elif self.color == other.color:
            # Same color, compare values
            return self.value > other.value
        elif self.color == led_color and other.color != led_color:
            # This card follows led color, other doesn't
            return True
        else:
            # Different colors, neither is trump or led color
            # In this case, the card doesn't win the trick
            return False
