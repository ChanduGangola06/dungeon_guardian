# 🏰 Dungeon Guardian - Intelligent Autonomous NPC Agent

An advanced AI agent that combines **GOAP (Goal-Oriented Action Planning)** with **LLM-style reasoning** to create an intelligent dungeon guardian that can think, plan, and adapt to changing situations.

## 🎯 Overview

The Dungeon Guardian is a sophisticated NPC agent that:
- **Thinks** using simulated LLM reasoning
- **Plans** using GOAP algorithms  
- **Adapts** by learning from failures
- **Explains** its decisions in natural language
- **Protects** a dungeon through intelligent behavior

## 🏗️ Architecture

The system consists of three main layers:

### 1. 🧠 Cognitive Layer
- **Goal Generation**: Analyzes world state to determine priorities
- **Action Justification**: Explains why actions are chosen
- **Reflection**: Learns from failures and adapts behavior
- **Memory**: Stores past experiences for future reference

### 2. 🛠️ Planning Layer (GOAP)
- **Action System**: 6 core actions with preconditions/effects
- **A* Planning**: Finds optimal action sequences
- **Dynamic Replanning**: Adapts when conditions change

### 3. 🎮 Execution Layer
- **World Simulation**: Manages state changes and action outcomes
- **Failure Simulation**: Introduces realistic failure scenarios
- **Environmental Changes**: Simulates dynamic world events

## 🎲 World State Components

The agent tracks these key world state variables:

- **Health** (0-100%): Guardian's current health
- **Stamina** (0-20): Energy for actions
- **Potion Count**: Available healing resources
- **Treasure Threat Level**: low/medium/high
- **Enemy Nearby**: Boolean threat detection
- **Safe Zone Status**: Current location safety
- **Backup Availability**: External help availability

## ⚔️ Available Actions

| Action | Description | Preconditions | Effects |
|--------|-------------|---------------|---------|
| **HealSelf** | Use potion to restore health | Has potion | +40 health, -1 potion |
| **AttackEnemy** | Combat nearby enemies | Enemy present, stamina ≥5 | Remove enemy, -5 stamina |
| **Retreat** | Move to safe zone | Not in safe zone | Safe zone = true |
| **DefendTreasure** | Protect valuable assets | Threat level ≥ medium | Reduce threat level |
| **CallBackup** | Request reinforcements | Backup available | Remove threats |
| **SearchForPotion** | Find healing resources | Potion count < 3 | +1 potion |

## 🎯 Goal Types

The agent can pursue four main goals:

1. **Survive**: Priority when health is critical
2. **Eliminate Threat**: When enemies threaten treasure
3. **Protect Treasure**: When treasure is under attack
4. **Prepare for Battle**: When no immediate threats exist

## 🧪 Test Scenarios

The system includes 4 comprehensive test scenarios:

### Scenario 1: Critical Survival
- Health: 20%, Enemy nearby, No potions
- **Expected**: Prioritize retreat and finding healing

### Scenario 2: Combat Ready
- Health: 85%, Enemy nearby, High treasure threat
- **Expected**: Aggressive elimination of threats

### Scenario 3: Preparation Phase
- Health: 70%, No enemies, Low stamina
- **Expected**: Resource gathering and preparation

### Scenario 4: Tactical Engagement
- Health: 60%, Enemy present, No healing resources
- **Expected**: Calculated combat with fallback plans

## 🧠 How LLM-Style Reasoning is Simulated

The Dungeon Guardian simulates LLM-style reasoning through its **Cognitive Layer**:
- **Goal Generation**: The agent analyzes the current world state and generates a goal, providing natural language reasoning for its choice (e.g., "Treasure is under high threat and enemy is nearby. I must eliminate the threat immediately.").
- **Action Justification**: Before each action, the agent explains in natural language why it chose that action, referencing its current state and goal.
- **Reflection on Failure**: If an action fails, the agent reflects on the failure, explains why it happened, and suggests how it will adapt in the future.
- **Memory**: The agent stores past failures and uses them to inform future decisions.

This approach mimics the way a large language model might reason, justify, and adapt, but is implemented with traditional Python logic and templates for transparency and reproducibility.

## 🚀 How to Run

### Requirements
- Python 3.7+
- No external dependencies required (standard library only)

### Run the Interactive Simulator
This is the recommended way to explore scenarios and interact with the agent:

```bash
python interactive_runner.py
```

You will be presented with a menu to:
- Run all built-in test scenarios
- Create and run your own custom scenario
- Try a quick demo

### Run a Custom Scenario Directly
You can also run the main agent with a hardcoded scenario by running:

```bash
python dungeon_guardian.py
```

This will execute a sample scenario defined at the bottom of `dungeon_guardian.py`.

---

For more details, see the code and comments in `dungeon_guardian.py` and `interactive_runner.py`.

## 🚀 Output

🔧 RUNNING CUSTOM SCENARIO
🏰 DUNGEON GUARDIAN SIMULATION STARTED 🏰
============================================================

🌍 WORLD STATE:
   ❤️  Health: 45%
   ⚡ Stamina: 12
   🧪 Potions: 1 (Has)
   💎 Treasure Threat: high
   👹 Enemy Nearby: Yes
   🛡️  Safe Zone: No
   📞 Backup Available: Yes

📍 STEP 1
----------------------------------------
🎯 GOAL: EliminateThreat
💭 REASONING: Treasure is under high threat and enemy is nearby. I have healing potions available if needed. I must eliminate the threat immediately.
📋 PLAN: CallBackup
⚡ EXECUTING: CallBackup
💭 WHY: I'm calling backup because I'm overwhelmed - health: 45%, enemy nearby: True. This helps eliminate the current threat.
✅ SUCCESS: Backup called successfully! Threats neutralized

🌍 WORLD STATE:
   ❤️  Health: 45%
   ⚡ Stamina: 12
   🧪 Potions: 1 (Has)
   💎 Treasure Threat: medium
   👹 Enemy Nearby: No
   🛡️  Safe Zone: No
   📞 Backup Available: No

📍 STEP 2
----------------------------------------
🎯 GOAL: ProtectTreasure
💭 REASONING: Treasure threat level is medium. I'm exposed and vulnerable to attacks. I need to defend our valuable assets.
📋 PLAN: DefendTreasure
⚡ EXECUTING: DefendTreasure
💭 WHY: I'm defending the treasure because the threat level is medium and it's my primary duty. This directly protects our treasure.
❌ FAILED: Overwhelmed by multiple attackers
🤔 REFLECTION: Defense failed: Overwhelmed by multiple attackers. I need better positioning or should have eliminated threats proactively. Next time, I'll assess the situation more carefully and have contingency plans ready.

🌍 WORLD STATE:
   ❤️  Health: 45%
   ⚡ Stamina: 12
   🧪 Potions: 1 (Has)
   💎 Treasure Threat: medium
   👹 Enemy Nearby: No
   🛡️  Safe Zone: No
   📞 Backup Available: No

📍 STEP 3
----------------------------------------
🎯 GOAL: ProtectTreasure
💭 REASONING: Treasure threat level is medium. I'm exposed and vulnerable to attacks. I need to defend our valuable assets.
📋 PLAN: DefendTreasure
⚡ EXECUTING: DefendTreasure
💭 WHY: I'm defending the treasure because the threat level is medium and it's my primary duty. This directly protects our treasure.
✅ SUCCESS: Treasure successfully defended

🌍 WORLD STATE:
   ❤️  Health: 45%
   ⚡ Stamina: 9
   🧪 Potions: 1 (Has)
   💎 Treasure Threat: low
   👹 Enemy Nearby: No
   🛡️  Safe Zone: No
   📞 Backup Available: No

📍 STEP 4
----------------------------------------
🎯 GOAL: PrepareForBattle
💭 REASONING: No immediate threats detected. I need to gather resources and restore my strength. I should prepare for potential future encounters.

## 🚀