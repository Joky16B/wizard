# Wizard Card Game - Core Components

This document identifies and describes the core components needed for implementing the Wizard card game.

## 1. Card Components

### Card
- **Properties**:
  - `color`: Humans (blue), Elves (green), Dwarves (red), Giants (yellow), or None (for special cards)
  - `value`: 1-13 for regular cards, special values for Wizard and Fool
  - `type`: Regular, Wizard ("Z"), or Fool ("N")
  - `image`: Visual representation of the card
- **Behaviors**:
  - Compare with other cards (for determining trick winner)
  - Display information

### Deck
- **Properties**:
  - Collection of 60 character cards (52 regular cards, 4 Wizards, 4 Fools)
- **Behaviors**:
  - Shuffle
  - Deal cards to players
  - Draw top card (for determining Trump color)

## 2. Player Components

### Apprentice (Player)
- **Properties**:
  - `name`: Apprentice identifier
  - `hand`: Collection of cards currently held
  - `prediction`: Number of tricks apprentice predicts to win in current round
  - `tricks_won`: Number of tricks actually won in current round
  - `experience_points`: Cumulative score across all rounds
  - `is_dealer`: Boolean indicating if apprentice is current dealer
  - `is_confidant`: Boolean indicating if apprentice is the scorekeeper
- **Behaviors**:
  - Make prediction
  - Play card
  - View hand
  - View game state
  - Calculate experience points

### AI Apprentice (extension of Apprentice)
- **Additional Behaviors**:
  - Analyze hand strength
  - Make strategic prediction
  - Select optimal card to play

## 3. Game State Components

### Round
- **Properties**:
  - `round_number`: Current round number
  - `cards_per_player`: Number of cards dealt this round
  - `trump_color`: Current Trump color
  - `trump_card`: Card that determined Trump
  - `player_predictions`: Record of each apprentice's prediction
  - `tricks_played`: Number of tricks completed in round
  - `tricks_remaining`: Number of tricks left in round
- **Behaviors**:
  - Initialize round
  - Process predictions
  - Track tricks
  - Calculate round experience points

### Trick
- **Properties**:
  - `leading_player`: Apprentice who led the trick
  - `leading_color`: Color that must be followed
  - `cards_played`: Cards played in current trick with apprentice association
  - `winner`: Apprentice who won the trick
- **Behaviors**:
  - Add played card
  - Determine trick winner
  - Reset for next trick

### Game
- **Properties**:
  - `apprentices`: List of apprentices in game
  - `confidant`: Apprentice who keeps score (Tablet of Truth)
  - `current_dealer`: Apprentice who is dealing
  - `current_round`: Round object for current round
  - `current_trick`: Trick object for current trick
  - `experience_points`: Historical record of points by round
  - `game_phase`: Current phase (deal, predict, play, score)
  - `max_rounds`: Maximum number of rounds based on apprentice count
- **Behaviors**:
  - Initialize game
  - Manage round progression
  - Track overall game state
  - Determine wise Wizard (winner)
  - Save/load game state

## 4. UI Components

### Card Display
- Visual representation of character cards
- Highlight playable cards
- Show played cards in trick
- Distinctive visuals for Wizard and Fool cards

### Apprentice Interface
- Hand display
- Prediction interface
- Card selection mechanism
- Experience Points display

### Game Board
- Trump color indicator
- Current trick display
- Prediction tracker (Tablet of Truth)
- Round and trick counter
- Apprentice turn indicator

### Scoreboard
- Current round Experience Points
- Cumulative Experience Points
- Prediction vs. tricks won comparison

## 5. Utility Components

### Rule Enforcer
- Validate card plays (following color, legal plays)
- Special rules for Wizard and Fool cards
- Apply correct Experience Points calculation

### Game Logger
- Record game actions
- Track statistics
- Enable replay or analysis

### Settings Manager
- Game variants configuration
- UI preferences
- Sound/visual effects settings

## Implementation Considerations

1. **Separation of Concerns**:
   - Separate game logic from UI
   - Use MVC or similar pattern

2. **Event System**:
   - Implement event-driven architecture for game state changes
   - Allow components to subscribe to relevant events

3. **Serialization**:
   - Design components to be serializable for save/load functionality

4. **Extensibility**:
   - Structure code to allow for game variants
   - Make AI behavior pluggable with different strategies
