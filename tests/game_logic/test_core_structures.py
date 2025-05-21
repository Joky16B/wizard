"""
Test module for the core data structures of the Wizard card game.

This module contains tests for the Card, Deck, Apprentice, Trick, Round, and Game classes.
"""

import unittest
from src.game_logic import Card, CardType, CardColor, Deck, Apprentice, Trick, Round, Game


class TestCard(unittest.TestCase):
    """Test cases for the Card class."""
    
    def test_regular_card_creation(self):
        """Test creating a regular card."""
        card = Card(CardType.REGULAR, CardColor.HUMANS, 5)
        self.assertEqual(card.card_type, CardType.REGULAR)
        self.assertEqual(card.color, CardColor.HUMANS)
        self.assertEqual(card.value, 5)
        self.assertEqual(card.display_value, "5")
    
    def test_wizard_card_creation(self):
        """Test creating a Wizard card."""
        card = Card(CardType.WIZARD)
        self.assertEqual(card.card_type, CardType.WIZARD)
        self.assertEqual(card.color, CardColor.NONE)
        self.assertIsNone(card.value)
        self.assertEqual(card.display_value, "Z")
    
    def test_fool_card_creation(self):
        """Test creating a Fool card."""
        card = Card(CardType.FOOL)
        self.assertEqual(card.card_type, CardType.FOOL)
        self.assertEqual(card.color, CardColor.NONE)
        self.assertIsNone(card.value)
        self.assertEqual(card.display_value, "N")
    
    def test_invalid_regular_card(self):
        """Test that creating an invalid regular card raises an error."""
        # Regular card without color
        with self.assertRaises(ValueError):
            Card(CardType.REGULAR, None, 5)
        
        # Regular card with invalid value
        with self.assertRaises(ValueError):
            Card(CardType.REGULAR, CardColor.HUMANS, 14)
        
        with self.assertRaises(ValueError):
            Card(CardType.REGULAR, CardColor.HUMANS, 0)
    
    def test_card_comparison(self):
        """Test card comparison logic."""
        # Create some test cards
        wizard = Card(CardType.WIZARD)
        fool = Card(CardType.FOOL)
        red_10 = Card(CardType.REGULAR, CardColor.DWARVES, 10)
        blue_8 = Card(CardType.REGULAR, CardColor.HUMANS, 8)
        green_13 = Card(CardType.REGULAR, CardColor.ELVES, 13)
        
        # Set trump and led colors for testing
        trump_color = CardColor.DWARVES
        led_color = CardColor.HUMANS
        
        # Wizard beats everything
        self.assertTrue(wizard.is_higher_than(red_10, trump_color, led_color))
        self.assertTrue(wizard.is_higher_than(green_13, trump_color, led_color))
        self.assertTrue(wizard.is_higher_than(fool, trump_color, led_color))
        
        # Fool loses to everything
        self.assertFalse(fool.is_higher_than(red_10, trump_color, led_color))
        self.assertFalse(fool.is_higher_than(green_13, trump_color, led_color))
        self.assertFalse(fool.is_higher_than(wizard, trump_color, led_color))
        
        # Trump beats non-trump
        self.assertTrue(red_10.is_higher_than(blue_8, trump_color, led_color))
        self.assertTrue(red_10.is_higher_than(green_13, trump_color, led_color))
        
        # Higher card in same color wins
        red_5 = Card(CardType.REGULAR, CardColor.DWARVES, 5)
        self.assertTrue(red_10.is_higher_than(red_5, trump_color, led_color))
        
        # Led color beats non-led, non-trump color
        self.assertTrue(blue_8.is_higher_than(green_13, trump_color, led_color))


class TestDeck(unittest.TestCase):
    """Test cases for the Deck class."""
    
    def test_deck_creation(self):
        """Test creating a deck with all 60 cards."""
        deck = Deck()
        self.assertEqual(len(deck.cards), 60)
        
        # Count card types
        regular_cards = sum(1 for card in deck.cards if card.card_type == CardType.REGULAR)
        wizard_cards = sum(1 for card in deck.cards if card.card_type == CardType.WIZARD)
        fool_cards = sum(1 for card in deck.cards if card.card_type == CardType.FOOL)
        
        self.assertEqual(regular_cards, 52)
        self.assertEqual(wizard_cards, 4)
        self.assertEqual(fool_cards, 4)
    
    def test_deck_shuffle(self):
        """Test shuffling the deck."""
        deck1 = Deck()
        deck2 = Deck()
        
        # Before shuffling, the cards should be in the same order
        self.assertEqual(str(deck1.cards), str(deck2.cards))
        
        # After shuffling, the cards should be in a different order
        deck2.shuffle(seed=42)  # Use a fixed seed for reproducibility
        self.assertNotEqual(str(deck1.cards), str(deck2.cards))
    
    def test_dealing_cards(self):
        """Test dealing cards from the deck."""
        deck = Deck()
        
        # Deal 5 cards
        dealt_cards = deck.deal(5)
        self.assertEqual(len(dealt_cards), 5)
        self.assertEqual(len(deck.cards), 55)
        
        # Try to deal too many cards
        with self.assertRaises(ValueError):
            deck.deal(56)
    
    def test_deal_to_players(self):
        """Test dealing cards to multiple players."""
        deck = Deck()
        
        # Deal 3 cards to 4 players
        hands, remaining = deck.deal_to_players(4, 3)
        
        self.assertEqual(len(hands), 4)
        for hand in hands:
            self.assertEqual(len(hand), 3)
        
        self.assertEqual(len(remaining), 48)  # 60 - (4 * 3) = 48
        
        # Try to deal too many cards
        with self.assertRaises(ValueError):
            deck.deal_to_players(4, 13)  # 4 * 13 = 52, but we only have 48 left


class TestApprentice(unittest.TestCase):
    """Test cases for the Apprentice class."""
    
    def test_apprentice_creation(self):
        """Test creating an apprentice."""
        apprentice = Apprentice("Test Apprentice")
        self.assertEqual(apprentice.name, "Test Apprentice")
        self.assertEqual(apprentice.hand, [])
        self.assertIsNone(apprentice.prediction)
        self.assertEqual(apprentice.tricks_won, 0)
        self.assertEqual(apprentice.experience_points, 0)
        self.assertFalse(apprentice.is_dealer)
        self.assertFalse(apprentice.is_confidant)
    
    def test_receive_cards(self):
        """Test receiving cards."""
        apprentice = Apprentice("Test Apprentice")
        cards = [
            Card(CardType.REGULAR, CardColor.HUMANS, 5),
            Card(CardType.WIZARD),
            Card(CardType.FOOL)
        ]
        
        apprentice.receive_cards(cards)
        self.assertEqual(len(apprentice.hand), 3)
    
    def test_make_prediction(self):
        """Test making a prediction."""
        apprentice = Apprentice("Test Apprentice")
        apprentice.make_prediction(2)
        self.assertEqual(apprentice.prediction, 2)
        
        # Test invalid prediction
        with self.assertRaises(ValueError):
            apprentice.make_prediction(-1)
    
    def test_play_card(self):
        """Test playing a card."""
        apprentice = Apprentice("Test Apprentice")
        cards = [
            Card(CardType.REGULAR, CardColor.HUMANS, 5),
            Card(CardType.WIZARD),
            Card(CardType.FOOL)
        ]
        apprentice.receive_cards(cards)
        
        # Play the Wizard card (index 1)
        played_card = apprentice.play_card(1)
        self.assertEqual(played_card.card_type, CardType.WIZARD)
        self.assertEqual(len(apprentice.hand), 2)
        
        # Try to play an invalid card
        with self.assertRaises(IndexError):
            apprentice.play_card(5)
    
    def test_can_follow_color(self):
        """Test checking if an apprentice can follow a color."""
        apprentice = Apprentice("Test Apprentice")
        cards = [
            Card(CardType.REGULAR, CardColor.HUMANS, 5),
            Card(CardType.REGULAR, CardColor.HUMANS, 10),
            Card(CardType.REGULAR, CardColor.DWARVES, 7),
            Card(CardType.WIZARD),
            Card(CardType.FOOL)
        ]
        apprentice.receive_cards(cards)
        
        self.assertTrue(apprentice.can_follow_color(CardColor.HUMANS))
        self.assertTrue(apprentice.can_follow_color(CardColor.DWARVES))
        self.assertFalse(apprentice.can_follow_color(CardColor.ELVES))
    
    def test_get_playable_cards(self):
        """Test getting playable cards."""
        apprentice = Apprentice("Test Apprentice")
        cards = [
            Card(CardType.REGULAR, CardColor.HUMANS, 5),
            Card(CardType.REGULAR, CardColor.HUMANS, 10),
            Card(CardType.REGULAR, CardColor.DWARVES, 7),
            Card(CardType.WIZARD),
            Card(CardType.FOOL)
        ]
        apprentice.receive_cards(cards)
        
        # If no color is led, all cards are playable
        playable = apprentice.get_playable_cards()
        self.assertEqual(len(playable), 5)
        
        # If HUMANS is led, HUMANS cards and special cards are playable
        playable = apprentice.get_playable_cards(CardColor.HUMANS)
        self.assertEqual(len(playable), 4)  # 2 HUMANS cards + Wizard + Fool
        
        # If ELVES is led, all cards are playable (since apprentice has no ELVES)
        playable = apprentice.get_playable_cards(CardColor.ELVES)
        self.assertEqual(len(playable), 5)
    
    def test_calculate_round_points(self):
        """Test calculating round points."""
        apprentice = Apprentice("Test Apprentice")
        
        # Correct prediction: 20 + (10 * tricks_won)
        apprentice.prediction = 3
        apprentice.tricks_won = 3
        self.assertEqual(apprentice.calculate_round_points(), 50)
        
        # Incorrect prediction: -10 * difference
        apprentice.prediction = 2
        apprentice.tricks_won = 4
        self.assertEqual(apprentice.calculate_round_points(), -20)
        
        apprentice.prediction = 5
        apprentice.tricks_won = 2
        self.assertEqual(apprentice.calculate_round_points(), -30)
        
        # No prediction made
        apprentice.prediction = None
        with self.assertRaises(ValueError):
            apprentice.calculate_round_points()


if __name__ == "__main__":
    unittest.main()
