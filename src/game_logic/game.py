"""
Game module for the Wizard card game.

This module defines the Game class for managing the overall game state.
"""

from enum import Enum, auto
from typing import Dict, List, Optional, Tuple

from .apprentice import Apprentice
from .card import CardColor
from .round import Round, RoundPhase


class GamePhase(Enum):
    """Enum representing the phases of the Wizard game."""
    SETUP = auto()
    ROUND_IN_PROGRESS = auto()
    GAME_OVER = auto()


class Game:
    """
    Represents the overall Wizard card game.
    
    The game consists of multiple rounds, with the number of rounds determined
    by the number of apprentices.
    """
    
    def __init__(self, apprentice_names: List[str]):
        """
        Initialize a new game with the given apprentice names.
        
        Args:
            apprentice_names: The names of the apprentices playing the game
            
        Raises:
            ValueError: If there are fewer than 3 or more than 6 apprentices
        """
        if len(apprentice_names) < 3 or len(apprentice_names) > 6:
            raise ValueError("Wizard requires 3-6 apprentices")
        
        # Create apprentices
        self.apprentices = [Apprentice(name) for name in apprentice_names]
        
        # Randomly select the first dealer and confidant
        import random
        dealer_index = random.randint(0, len(self.apprentices) - 1)
        self.apprentices[dealer_index].is_dealer = True
        
        confidant_index = (dealer_index + 1) % len(self.apprentices)
        self.apprentices[confidant_index].is_confidant = True
        
        # Calculate the maximum number of rounds based on apprentice count
        self.max_rounds = self._calculate_max_rounds(len(self.apprentices))
        
        # Initialize game state
        self.current_round_number = 0
        self.current_round: Optional[Round] = None
        self.round_history: List[Round] = []
        self.phase = GamePhase.SETUP
        
        # Experience points history by round
        self.experience_points_history: List[Dict[Apprentice, int]] = []
    
    def _calculate_max_rounds(self, num_apprentices: int) -> int:
        """
        Calculate the maximum number of rounds based on the number of apprentices.
        
        Args:
            num_apprentices: The number of apprentices in the game
            
        Returns:
            The maximum number of rounds
        """
        # With 60 cards, the max cards per apprentice is 60 / num_apprentices
        max_cards = 60 // num_apprentices
        return max_cards
    
    def start_game(self):
        """
        Start the game by beginning the first round.
        
        Raises:
            ValueError: If the game is not in the SETUP phase
        """
        if self.phase != GamePhase.SETUP:
            raise ValueError(f"Cannot start game in {self.phase} phase")
        
        self._start_next_round()
    
    def _start_next_round(self):
        """Start the next round of the game."""
        self.current_round_number += 1
        
        # Find the current dealer
        dealer_index = next(i for i, a in enumerate(self.apprentices) if a.is_dealer)
        
        # Create a new round
        self.current_round = Round(self.current_round_number, self.apprentices, dealer_index)
        
        # Deal cards
        self.current_round.deal_cards()
        
        self.phase = GamePhase.ROUND_IN_PROGRESS
    
    def make_prediction(self, apprentice: Apprentice, prediction: int) -> bool:
        """
        Record an apprentice's prediction for the current round.
        
        Args:
            apprentice: The apprentice making the prediction
            prediction: The number of tricks predicted
            
        Returns:
            True if the prediction is valid and recorded, False otherwise
            
        Raises:
            ValueError: If there is no current round or the game is not in progress
        """
        if self.phase != GamePhase.ROUND_IN_PROGRESS or not self.current_round:
            raise ValueError("Cannot make predictions: no round in progress")
        
        return self.current_round.make_prediction(apprentice, prediction)
    
    def play_card(self, apprentice: Apprentice, card_index: int) -> bool:
        """
        Play a card from an apprentice's hand in the current round.
        
        Args:
            apprentice: The apprentice playing the card
            card_index: The index of the card in the apprentice's hand
            
        Returns:
            True if the play is valid and executed, False otherwise
            
        Raises:
            ValueError: If there is no current round or the game is not in progress
        """
        if self.phase != GamePhase.ROUND_IN_PROGRESS or not self.current_round:
            raise ValueError("Cannot play card: no round in progress")
        
        return self.current_round.play_card(apprentice, card_index)
    
    def set_dealer_chosen_trump(self, color: CardColor):
        """
        Set the trump color chosen by the dealer when the trump card is a Wizard.
        
        Args:
            color: The color chosen as trump
            
        Raises:
            ValueError: If there is no current round or the game is not in progress
        """
        if self.phase != GamePhase.ROUND_IN_PROGRESS or not self.current_round:
            raise ValueError("Cannot set trump color: no round in progress")
        
        self.current_round.set_dealer_chosen_trump(color)
    
    def end_round(self):
        """
        End the current round, calculate scores, and prepare for the next round.
        
        Returns:
            A dictionary mapping each apprentice to their points for this round
            
        Raises:
            ValueError: If there is no current round or it's not in the SCORING phase
        """
        if not self.current_round or self.current_round.phase != RoundPhase.SCORING:
            raise ValueError("Cannot end round: round not ready for scoring")
        
        # Score the round
        round_points = self.current_round.score_round()
        self.experience_points_history.append(round_points)
        
        # Add the round to history
        self.round_history.append(self.current_round)
        
        # Update dealer for next round
        self._rotate_dealer()
        
        # Reset apprentices for the next round
        for apprentice in self.apprentices:
            apprentice.reset_for_new_round()
        
        # Check if the game is over
        if self.current_round_number >= self.max_rounds:
            self.phase = GamePhase.GAME_OVER
        else:
            # Start the next round
            self._start_next_round()
        
        return round_points
    
    def _rotate_dealer(self):
        """Rotate the dealer role to the next apprentice."""
        current_dealer_index = next(i for i, a in enumerate(self.apprentices) if a.is_dealer)
        
        # Remove dealer status from current dealer
        self.apprentices[current_dealer_index].is_dealer = False
        
        # Set the next apprentice as dealer
        next_dealer_index = (current_dealer_index + 1) % len(self.apprentices)
        self.apprentices[next_dealer_index].is_dealer = True
    
    def get_winner(self) -> Optional[Apprentice]:
        """
        Get the apprentice with the highest experience points.
        
        Returns:
            The winning apprentice, or None if the game is not over
        """
        if self.phase != GamePhase.GAME_OVER:
            return None
        
        return max(self.apprentices, key=lambda a: a.experience_points)
    
    def get_current_apprentice(self) -> Optional[Apprentice]:
        """
        Get the apprentice whose turn it currently is.
        
        Returns:
            The current apprentice, or None if there is no active round
        """
        if not self.current_round or self.phase != GamePhase.ROUND_IN_PROGRESS:
            return None
        
        return self.current_round.get_current_apprentice()
    
    def get_game_state(self) -> Dict:
        """
        Get a dictionary representing the current game state.
        
        Returns:
            A dictionary with the current game state
        """
        state = {
            "phase": self.phase.name,
            "current_round": self.current_round_number,
            "max_rounds": self.max_rounds,
            "apprentices": [
                {
                    "name": a.name,
                    "experience_points": a.experience_points,
                    "is_dealer": a.is_dealer,
                    "is_confidant": a.is_confidant
                }
                for a in self.apprentices
            ]
        }
        
        if self.current_round:
            state["round_phase"] = self.current_round.phase.name
            
            if self.current_round.trump_color:
                state["trump_color"] = self.current_round.trump_color.name
            
            if self.current_round.phase == RoundPhase.PLAYING:
                current_apprentice = self.get_current_apprentice()
                if current_apprentice:
                    state["current_apprentice"] = current_apprentice.name
        
        return state
    
    def __str__(self) -> str:
        """Return a string representation of the game."""
        return f"Wizard Game with {len(self.apprentices)} apprentices, Round {self.current_round_number}/{self.max_rounds}"
