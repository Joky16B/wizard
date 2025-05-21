"""
Round module for the Wizard card game.

This module defines the Round class for managing a complete round in the Wizard game.
"""

from enum import Enum, auto
from typing import Dict, List, Optional, Tuple

from .apprentice import Apprentice
from .card import Card, CardType, CardColor
from .deck import Deck
from .trick import Trick


class RoundPhase(Enum):
    """Enum representing the phases of a round in the Wizard game."""
    DEALING = auto()
    PREDICTING = auto()
    PLAYING = auto()
    SCORING = auto()
    COMPLETE = auto()


class Round:
    """
    Represents a complete round in the Wizard card game.
    
    A round consists of dealing cards, making predictions, playing tricks,
    and scoring the results.
    """
    
    def __init__(self, round_number: int, apprentices: List[Apprentice], dealer_index: int):
        """
        Initialize a new round.
        
        Args:
            round_number: The current round number (1-based)
            apprentices: The list of apprentices in the game
            dealer_index: The index of the dealer in the apprentices list
        """
        self.round_number = round_number
        self.apprentices = apprentices
        self.dealer_index = dealer_index
        self.cards_per_apprentice = round_number  # In round 1, each apprentice gets 1 card, etc.
        
        self.deck = Deck()
        self.trump_card: Optional[Card] = None
        self.trump_color: Optional[CardColor] = None
        
        self.current_trick: Optional[Trick] = None
        self.tricks_played: List[Trick] = []
        self.current_apprentice_index: int = (dealer_index + 1) % len(apprentices)  # Left of dealer
        
        self.phase = RoundPhase.DEALING
    
    def deal_cards(self):
        """
        Deal cards to all apprentices for this round.
        
        Returns:
            The trump card (or None if there are no cards left)
        """
        if self.phase != RoundPhase.DEALING:
            raise ValueError(f"Cannot deal cards in {self.phase} phase")
        
        # Shuffle the deck
        self.deck.shuffle()
        
        # Deal cards to each apprentice
        hands, remaining_cards = self.deck.deal_to_players(
            len(self.apprentices), self.cards_per_apprentice
        )
        
        for i, apprentice in enumerate(self.apprentices):
            apprentice.receive_cards(hands[i])
        
        # Determine trump color (if any)
        if remaining_cards:
            self.trump_card = self.deck.draw_trump_card()
            
            if self.trump_card:
                if self.trump_card.card_type == CardType.WIZARD:
                    # Dealer chooses trump color (for now, just set to None)
                    # In a real implementation, we would prompt the dealer
                    self.trump_color = None
                elif self.trump_card.card_type == CardType.FOOL:
                    # No trump color for this round
                    self.trump_color = None
                else:
                    # Regular card determines trump color
                    self.trump_color = self.trump_card.color
        else:
            # Last round has no trump
            self.trump_card = None
            self.trump_color = None
        
        self.phase = RoundPhase.PREDICTING
        return self.trump_card
    
    def set_dealer_chosen_trump(self, color: CardColor):
        """
        Set the trump color chosen by the dealer when the trump card is a Wizard.
        
        Args:
            color: The color chosen as trump
        
        Raises:
            ValueError: If the trump card is not a Wizard or the phase is not PREDICTING
        """
        if self.phase != RoundPhase.PREDICTING:
            raise ValueError(f"Cannot set dealer-chosen trump in {self.phase} phase")
        
        if not self.trump_card or self.trump_card.card_type != CardType.WIZARD:
            raise ValueError("Dealer can only choose trump color when the trump card is a Wizard")
        
        self.trump_color = color
    
    def make_prediction(self, apprentice: Apprentice, prediction: int) -> bool:
        """
        Record an apprentice's prediction for the round.
        
        Args:
            apprentice: The apprentice making the prediction
            prediction: The number of tricks predicted
            
        Returns:
            True if the prediction is valid and recorded, False otherwise
            
        Raises:
            ValueError: If the phase is not PREDICTING
        """
        if self.phase != RoundPhase.PREDICTING:
            raise ValueError(f"Cannot make predictions in {self.phase} phase")
        
        if prediction < 0 or prediction > self.cards_per_apprentice:
            return False
        
        apprentice.make_prediction(prediction)
        
        # Check if all apprentices have made predictions
        if all(a.prediction is not None for a in self.apprentices):
            self.phase = RoundPhase.PLAYING
            self._start_first_trick()
        
        return True
    
    def _start_first_trick(self):
        """Start the first trick of the round."""
        # The apprentice to the left of the dealer leads the first trick
        first_apprentice_index = (self.dealer_index + 1) % len(self.apprentices)
        first_apprentice = self.apprentices[first_apprentice_index]
        
        self.current_trick = Trick(first_apprentice, self.trump_color)
        self.current_apprentice_index = first_apprentice_index
    
    def _start_next_trick(self, leading_apprentice: Apprentice):
        """
        Start the next trick of the round.
        
        Args:
            leading_apprentice: The apprentice who leads the next trick
        """
        self.current_trick = Trick(leading_apprentice, self.trump_color)
        # Find the index of the leading apprentice
        self.current_apprentice_index = self.apprentices.index(leading_apprentice)
    
    def play_card(self, apprentice: Apprentice, card_index: int) -> bool:
        """
        Play a card from an apprentice's hand.
        
        Args:
            apprentice: The apprentice playing the card
            card_index: The index of the card in the apprentice's hand
            
        Returns:
            True if the play is valid and executed, False otherwise
            
        Raises:
            ValueError: If the phase is not PLAYING or it's not the apprentice's turn
        """
        if self.phase != RoundPhase.PLAYING:
            raise ValueError(f"Cannot play cards in {self.phase} phase")
        
        if apprentice != self.apprentices[self.current_apprentice_index]:
            raise ValueError(f"It is not {apprentice.name}'s turn to play")
        
        if not self.current_trick:
            raise ValueError("No active trick")
        
        # Check if the card can be legally played
        playable_indices = apprentice.get_playable_cards(self.current_trick.leading_color)
        if card_index not in playable_indices:
            return False
        
        # Play the card
        card = apprentice.play_card(card_index)
        self.current_trick.play_card(apprentice, card)
        
        # Move to the next apprentice
        self.current_apprentice_index = (self.current_apprentice_index + 1) % len(self.apprentices)
        
        # Check if the trick is complete
        if len(self.current_trick.cards_played) == len(self.apprentices):
            winner = self.current_trick.complete_trick()
            self.tricks_played.append(self.current_trick)
            
            # Check if the round is complete
            if len(self.tricks_played) == self.cards_per_apprentice:
                self.phase = RoundPhase.SCORING
            else:
                # Start the next trick with the winner leading
                self._start_next_trick(winner)
        
        return True
    
    def score_round(self) -> Dict[Apprentice, int]:
        """
        Calculate and apply the scores for the round.
        
        Returns:
            A dictionary mapping each apprentice to their points for this round
            
        Raises:
            ValueError: If the phase is not SCORING
        """
        if self.phase != RoundPhase.SCORING:
            raise ValueError(f"Cannot score round in {self.phase} phase")
        
        round_points = {}
        
        for apprentice in self.apprentices:
            points = apprentice.calculate_round_points()
            apprentice.add_experience_points(points)
            round_points[apprentice] = points
        
        self.phase = RoundPhase.COMPLETE
        return round_points
    
    def get_next_dealer_index(self) -> int:
        """
        Get the index of the dealer for the next round.
        
        Returns:
            The index of the next dealer in the apprentices list
        """
        return (self.dealer_index + 1) % len(self.apprentices)
    
    def get_current_apprentice(self) -> Optional[Apprentice]:
        """
        Get the apprentice whose turn it currently is.
        
        Returns:
            The current apprentice, or None if the round is not in the PLAYING phase
        """
        if self.phase != RoundPhase.PLAYING:
            return None
        
        return self.apprentices[self.current_apprentice_index]
    
    def get_trick_count(self) -> int:
        """
        Get the number of tricks played so far in this round.
        
        Returns:
            The number of completed tricks
        """
        return len(self.tricks_played)
    
    def get_tricks_remaining(self) -> int:
        """
        Get the number of tricks remaining in this round.
        
        Returns:
            The number of tricks yet to be played
        """
        return self.cards_per_apprentice - len(self.tricks_played)
    
    def __str__(self) -> str:
        """Return a string representation of the round."""
        return f"Round {self.round_number} ({self.phase.name})"
