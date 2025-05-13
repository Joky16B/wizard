# Wizard Card Game - Game Flow and Rounds Structure

## Game Phases Overview

The Wizard card game follows a structured flow with distinct phases that repeat each round until the game ends. This document outlines the complete game flow and round structure to guide implementation.

## Overall Game Structure

1. **Game Initialization**
   - Player setup (3-6 apprentices/players)
   - Shuffle deck of 60 character cards
   - Appoint a Confidant (scorekeeper)
   - Determine first dealer
   - Initialize Experience Points tracking

2. **Round Sequence**
   - Rounds progress from 1 card per player to maximum (based on player count)
   - After maximum round is played, game ends

3. **Game End**
   - Final Experience Points are tallied
   - The Apprentice with the highest score ascends to the level of Wizard

## Detailed Round Structure

Each round consists of the following phases:

### 1. Deal Phase
- Dealer deals cards face-down to each player
  - Round 1: 1 card per player
  - Round 2: 2 cards per player
  - And so on...
- Cards not dealt form a face-down deck in the middle of the table
- After dealing, turn up top card of remaining deck to determine Trump color
  - If Wizard ("Z"): dealer chooses Trump color
  - If Fool ("N"): no Trump in this round
  - Otherwise: card's color becomes Trump
- Note: The last round has no Trump since there are no cards left

### 2. Prediction Phase
- Starting with player to dealer's left, each player makes a prediction
- Prediction represents how many tricks player expects to win in the round
- All predictions are recorded by the Confidant on the Tablet of Truth

### 3. Trick-Taking Phase
- Player to dealer's left leads first card for the first trick
- Play proceeds clockwise
- Players must follow the led color if possible
- If unable to follow the led color, any card may be played
- Special cards:
  - Wizard cards may always be played, even if a player could follow the led color
  - Fool cards may always be played, even if a player could follow the led color
  - If a trick is opened with a Wizard, following players may play any card
  - If a trick is opened with a Fool, the second card played determines the color that must be followed
- Trick winner determination (in order):
  - The first Wizard card played in the trick
  - The highest card of the Trump color
  - The highest card of the led color
  - Exception: If only Fools are played, the first Fool wins (possible only with 3-4 players)
- Winner of trick leads next trick
- Continue until all cards are played

### 4. Scoring Phase
- Each player's actual tricks won is compared to their prediction
- Correct prediction: 20 Experience Points + 10 points per trick won
- Incorrect prediction: -10 Experience Points for each trick over or under prediction
- Scores are recorded and added to previous rounds

### 5. Round Transition
- Dealer role passes clockwise to the next Apprentice
- Card count increases by 1 for next round
- If maximum round reached, game ends; otherwise, new round begins

## Round Limits Based on Player Count
- 3 players: 20 rounds (60 cards ÷ 3 players)
- 4 players: 15 rounds (60 cards ÷ 4 players)
- 5 players: 12 rounds (60 cards ÷ 5 players)
- 6 players: 10 rounds (60 cards ÷ 6 players)

## Game State Tracking Requirements
Throughout the game, the following states need to be tracked:

1. **Global Game State**
   - Current round number
   - Current dealer
   - Current Trump color
   - Player Experience Points
   - Game phase (dealing, predicting, playing, scoring)

2. **Round State**
   - Cards dealt to each player
   - Trump card/color
   - Player predictions
   - Tricks won by each player

3. **Trick State**
   - Current leader
   - Cards played in current trick
   - Leading color
   - Winner of trick

## State Transitions
The game progresses through these state transitions:

```
Game Start → Deal Cards → Determine Trump → Predictions → 
Trick-Taking → Scoring → Next Round/Game End
```

Each state has specific entry conditions, actions, and exit conditions that will need to be implemented in the game logic.
