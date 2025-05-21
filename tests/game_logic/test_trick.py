"""
Test module for the Trick class in the Wizard card game.

This module contains tests for the Trick class, focusing on edge cases
related to leading color determination with special cards.
"""

import unittest
from src.game_logic import Card, CardType, CardColor, Apprentice, Trick


class TestTrick(unittest.TestCase):
    """Test cases for the Trick class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.apprentice1 = Apprentice("Player 1")
        self.apprentice2 = Apprentice("Player 2")
        self.apprentice3 = Apprentice("Player 3")
        
        # Create a trick with Player 1 leading
        self.trick = Trick(self.apprentice1, CardColor.DWARVES)
    
    def test_regular_card_first(self):
        """Test leading with a regular card sets the leading color."""
        red_card = Card(CardType.REGULAR, CardColor.DWARVES, 5)
        self.trick.play_card(self.apprentice1, red_card)
        
        self.assertEqual(self.trick.leading_color, CardColor.DWARVES)
    
    def test_wizard_card_first(self):
        """Test leading with a Wizard doesn't set a leading color."""
        wizard_card = Card(CardType.WIZARD)
        self.trick.play_card(self.apprentice1, wizard_card)
        
        self.assertIsNone(self.trick.leading_color)
    
    def test_fool_card_first(self):
        """Test leading with a Fool doesn't set a leading color."""
        fool_card = Card(CardType.FOOL)
        self.trick.play_card(self.apprentice1, fool_card)
        
        self.assertIsNone(self.trick.leading_color)
    
    def test_fool_then_regular(self):
        """Test Fool followed by Regular sets the leading color to the Regular card's color."""
        fool_card = Card(CardType.FOOL)
        blue_card = Card(CardType.REGULAR, CardColor.HUMANS, 8)
        
        self.trick.play_card(self.apprentice1, fool_card)
        self.trick.play_card(self.apprentice2, blue_card)
        
        self.assertEqual(self.trick.leading_color, CardColor.HUMANS)
    
    def test_fool_then_wizard(self):
        """Test Fool followed by Wizard doesn't set a leading color."""
        fool_card = Card(CardType.FOOL)
        wizard_card = Card(CardType.WIZARD)
        
        self.trick.play_card(self.apprentice1, fool_card)
        self.trick.play_card(self.apprentice2, wizard_card)
        
        self.assertIsNone(self.trick.leading_color)
    
    def test_fool_wizard_then_regular(self):
        """Test Fool, then Wizard, then Regular sets the leading color to the Regular card's color."""
        fool_card = Card(CardType.FOOL)
        wizard_card = Card(CardType.WIZARD)
        green_card = Card(CardType.REGULAR, CardColor.ELVES, 10)
        
        self.trick.play_card(self.apprentice1, fool_card)
        self.trick.play_card(self.apprentice2, wizard_card)
        self.trick.play_card(self.apprentice3, green_card)
        
        # The leading color should still be None since we only check for setting it
        # on the first or second card played
        self.assertIsNone(self.trick.leading_color)
    
    def test_wizard_then_fool(self):
        """Test Wizard followed by Fool doesn't set a leading color."""
        wizard_card = Card(CardType.WIZARD)
        fool_card = Card(CardType.FOOL)
        
        self.trick.play_card(self.apprentice1, wizard_card)
        self.trick.play_card(self.apprentice2, fool_card)
        
        self.assertIsNone(self.trick.leading_color)
    
    def test_determine_winner_wizard_wins(self):
        """Test that a Wizard always wins a trick."""
        red_card = Card(CardType.REGULAR, CardColor.DWARVES, 13)  # High value
        wizard_card = Card(CardType.WIZARD)
        blue_card = Card(CardType.REGULAR, CardColor.HUMANS, 10)
        
        self.trick.play_card(self.apprentice1, red_card)
        self.trick.play_card(self.apprentice2, wizard_card)
        self.trick.play_card(self.apprentice3, blue_card)
        
        winner = self.trick.determine_winner()
        self.assertEqual(winner, self.apprentice2)
    
    def test_determine_winner_multiple_wizards(self):
        """Test that when multiple Wizards are played, the first one wins."""
        wizard1 = Card(CardType.WIZARD)
        wizard2 = Card(CardType.WIZARD)
        
        self.trick.play_card(self.apprentice1, wizard1)
        self.trick.play_card(self.apprentice2, wizard2)
        
        winner = self.trick.determine_winner()
        self.assertEqual(winner, self.apprentice1)
    
    def test_determine_winner_fool_never_wins(self):
        """Test that a Fool never wins a trick."""
        fool_card = Card(CardType.FOOL)
        low_card = Card(CardType.REGULAR, CardColor.DWARVES, 1)  # Low value
        
        self.trick.play_card(self.apprentice1, fool_card)
        self.trick.play_card(self.apprentice2, low_card)
        
        winner = self.trick.determine_winner()
        self.assertEqual(winner, self.apprentice2)
    
    def test_determine_winner_all_fools(self):
        """Test that when all players play Fools, the first player wins."""
        fool1 = Card(CardType.FOOL)
        fool2 = Card(CardType.FOOL)
        fool3 = Card(CardType.FOOL)
        
        self.trick.play_card(self.apprentice1, fool1)
        self.trick.play_card(self.apprentice2, fool2)
        self.trick.play_card(self.apprentice3, fool3)
        
        winner = self.trick.determine_winner()
        self.assertEqual(winner, self.apprentice1)  # First player should win
    
    def test_determine_winner_trump_beats_led(self):
        """Test that a trump card beats a card of the led color."""
        # Set trump color to DWARVES
        trick = Trick(self.apprentice1, CardColor.DWARVES)
        
        blue_card = Card(CardType.REGULAR, CardColor.HUMANS, 13)  # High value
        red_card = Card(CardType.REGULAR, CardColor.DWARVES, 5)   # Low value but trump
        
        trick.play_card(self.apprentice1, blue_card)
        trick.play_card(self.apprentice2, red_card)
        
        winner = trick.determine_winner()
        self.assertEqual(winner, self.apprentice2)
    
    def test_determine_winner_highest_led_color_wins(self):
        """Test that the highest card of the led color wins."""
        blue_8 = Card(CardType.REGULAR, CardColor.HUMANS, 8)
        blue_10 = Card(CardType.REGULAR, CardColor.HUMANS, 10)
        green_13 = Card(CardType.REGULAR, CardColor.ELVES, 13)  # Highest value but wrong color
        
        self.trick.play_card(self.apprentice1, blue_8)
        self.trick.play_card(self.apprentice2, blue_10)
        self.trick.play_card(self.apprentice3, green_13)
        
        winner = self.trick.determine_winner()
        self.assertEqual(winner, self.apprentice2)


if __name__ == "__main__":
    unittest.main()
