"""
Apprentice module for the Wizard card game.

This module defines the Apprentice class representing a player in the Wizard game.
"""

from typing import List, Optional

from .card import Card, CardColor


class Apprentice:
    """
    Represents an apprentice (player) in the Wizard card game.
    
    An apprentice has a hand of cards, makes predictions about how many tricks
    they will win, and accumulates experience points throughout the game.
    """
    
    def __init__(self, name: str):
        """
        Initialize a new apprentice.
        
        Args:
            name: The name of the apprentice
        """
        self.name = name
        self.hand: List[Card] = []
        self.prediction: Optional[int] = None
        self.tricks_won: int = 0
        self.experience_points: int = 0
        self.is_dealer: bool = False
        self.is_confidant: bool = False
    
    def receive_cards(self, cards: List[Card]):
        """
        Add cards to the apprentice's hand.
        
        Args:
            cards: The cards to add to the hand
        """
        self.hand.extend(cards)
    
    def make_prediction(self, prediction: int):
        """
        Make a prediction for the number of tricks to win in the current round.
        
        Args:
            prediction: The number of tricks predicted to win
            
        Raises:
            ValueError: If the prediction is negative
        """
        if prediction < 0:
            raise ValueError("Prediction cannot be negative")
        self.prediction = prediction
    
    def play_card(self, card_index: int) -> Card:
        """
        Play a card from the apprentice's hand.
        
        Args:
            card_index: The index of the card in the hand to play
            
        Returns:
            The played card
            
        Raises:
            IndexError: If the card_index is out of range
        """
        if card_index < 0 or card_index >= len(self.hand):
            raise IndexError(f"Card index {card_index} is out of range for hand of size {len(self.hand)}")
        
        return self.hand.pop(card_index)
    
    def can_follow_color(self, color: CardColor) -> bool:
        """
        Check if the apprentice can follow the led color.
        
        Args:
            color: The color to check
            
        Returns:
            True if the apprentice has at least one card of the specified color, False otherwise
        """
        return any(card.color == color for card in self.hand)
    
    def get_playable_cards(self, led_color: Optional[CardColor] = None) -> List[int]:
        """
        Get the indices of cards that can be legally played.
        
        Args:
            led_color: The color that was led in the current trick (if any)
            
        Returns:
            A list of indices of cards that can be legally played
        """
        # If no color was led or apprentice can't follow color, all cards are playable
        if led_color is None or not self.can_follow_color(led_color):
            return list(range(len(self.hand)))
        
        # Otherwise, only cards of the led color and special cards (Wizard/Fool) are playable
        playable_indices = []
        for i, card in enumerate(self.hand):
            if card.color == led_color or card.color == CardColor.NONE:
                playable_indices.append(i)
        
        return playable_indices
    
    def win_trick(self):
        """Record that the apprentice has won a trick in the current round."""
        self.tricks_won += 1
    
    def calculate_round_points(self) -> int:
        """
        Calculate the experience points earned in the current round.
        
        Returns:
            The number of experience points earned
        """
        if self.prediction is None:
            raise ValueError("Cannot calculate points: no prediction was made")
        
        if self.prediction == self.tricks_won:
            # Correct prediction: 20 points + 10 points per trick won
            return 20 + (10 * self.tricks_won)
        else:
            # Incorrect prediction: -10 points for each trick over or under
            difference = abs(self.prediction - self.tricks_won)
            return -10 * difference
    
    def add_experience_points(self, points: int):
        """
        Add experience points to the apprentice's total.
        
        Args:
            points: The number of points to add (can be negative)
        """
        self.experience_points += points
    
    def reset_for_new_round(self):
        """Reset the apprentice's state for a new round."""
        self.hand = []
        self.prediction = None
        self.tricks_won = 0
    
    def __str__(self) -> str:
        """Return a string representation of the apprentice."""
        return f"{self.name} ({self.experience_points} points)"
