import json
import heapq
from typing import List, Dict, Tuple, optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import random
import time

# ==================== WORLD STATE & ENUMS ====================

class ActionType(Enum):
    HEAL_SELF = "HealSelf"
    ATTACK_ENEMEY = "AttackEnemy"
    RETREAT = "Retreat"
    DEFEND_TREASURE = "DefendTreasure"
    CALL_BACKUP = "CallBackup"
    SEARCH_FOR_POTION = "SearchForPotion"
    
class GoalType(Enum):
    SURVIVE = "Survive"
    ELIMINATE_THREAT = "EliminateThreat"
    PROTECT_TREASURE = "ProtectTreasure"
    PREPARE_FOR_BATTLE = "PrepareForBattle"
    
@dataclass
class WorldState:
    health: int = 100
    stamina: int = 20
    potion_count: int = 0
    trease_threat_level: str = "low"
    enemy_nearby: bool = false
    is_in_safe_zone: bool = true
    has_potion: bool = false
    backup_available: bool = true
    
    def copy(self):
        return WorldState(**asdict(self))
    
# ==================== COGNITIVE LAYER (LLM SIMULATION) ====================

class CognitiveEngine:
    """Simulates LLM-based reasoning for goal generation and reflection"""
    
    def __init__(self):
        self.memory = []
        
    def generate_goal(self, world_state: WorldState) -> Tuple[GoalType, str]:
        """Generate a goal based on current world state with reasoning"""
        
        reasoning_context = self.analyze_situation(world_state)
        
        # Priority-based goal selection with reasoning
        if world_state.health <= 30:
            goal = GoalType.SURVIVE
            reasoning = f"My health is critically low at {world_state.health}%. {reasoning_context['health_status']} Survival is my top priority."
        elif world_state.treasure_threat_level == "high" and world_state.enemy_nearby:
            goal = GoalType.ELIMINATE_THREAT
            reasoning = f"Treasure is under high threat and enemy is nearby. {reasoning_context['combat_readiness']} I must eliminate the threat immediately."
        elif world_state.treasure_threat_level in ["medium", "high"]:
            goal = GoalType.PROTECT_TREASURE
            reasoning = f"Treasure threat level is {world_state.treasure_threat_level}. {reasoning_context['defensive_position']} I need to defend our valuable assets."
        else:
            goal = GoalType.PREPARE_FOR_BATTLE
            reasoning = f"No immediate threats detected. {reasoning_context['preparation']} I should prepare for potential future encounters."
            
        return goal, reasoning
    
    def analyze_situation(self, world_state: WorldState) -> Dict[str, str]:
        """Analyze current situation for reasoning context"""

        context = {}
        
        # health analysis
        if world_state.health <= 30:
            context['health_status'] = "I'm severely wounded and need immediate healing or retreat."
        elif world_state.health <= 60:
            context['health_status'] = "My health is concerning but manageable."
        else:
            context['health_status'] = "I'm in good health and ready for combat."
            
        # Combat readiness
        if world_state.stamina <= 5:
            context['combat_readiness'] = "My stamina is too low for sustained combat."
        elif world_state.has_potion:
            context['combat_readiness'] = "I have healing potions available if needed."
        else:
            context['combat_readiness'] = "I have no healing resources available."
            
        # Defensive position
        if world_state.is_in_safe_zone:
            context['defensive_position'] = "I'm currently in a safe zone."
        else:
            context['defensive_position'] = "I'm exposed and vulnerable to attacks."
            
        # Preparation status
        if world_state.stamina >= 15 and world_state.has_potion:
            context['preparation'] = "I'm well-prepared with good stamina and healing resources."
        else:
            context['preparation'] = "I need to gather resources and restore my strength."
            
        return context
    
    def justify_action(self, action: ActionType, world_state: WorldState, goal: GoalType) -> str:
        """Provide reasoning for why an action was chosen"""
        
        base_reasoning = {
            ActionType.HEAL_SELF: f"I chose to heal because my health is at {world_state.health}% and I have potions available.",
            ActionType.ATTACK_ENEMY: f"I'm attacking because I have {world_state.health}% health, {world_state.stamina} stamina, and need to eliminate the threat.",
            ActionType.RETREAT: f"I'm retreating because my health ({world_state.health}%) or stamina ({world_state.stamina}) is too low for combat.",
            ActionType.DEFEND_TREASURE: f"I'm defending the treasure because the threat level is {world_state.treasure_threat_level} and it's my primary duty.",
            ActionType.CALL_BACKUP: f"I'm calling backup because I'm overwhelmed - health: {world_state.health}%, enemy nearby: {world_state.enemy_nearby}.",
            ActionType.SEARCH_FOR_POTION: f"I'm searching for potions because I have {world_state.potion_count} potions and may need healing resources."
        }
        
        goal_context = {
            GoalType.SURVIVE: "This supports my survival goal.",
            GoalType.ELIMINATE_THREAT: "This helps eliminate the current threat.",
            GoalType.PROTECT_TREASURE: "This directly protects our treasure.",
            GoalType.PREPARE_FOR_BATTLE: "This prepares me for future encounters."
        }
        
        return f"{base_reasoning.get(action, 'Unknown action reasoning')} {goal_context.get(goal, '')}"
    
    def reflect_on_failure(self, failed_action: ActionType, world_state: WorldState, reason: str) -> str:
        """Reflect on why a plan failed and suggest improvements"""
        
        self.memory.append({
            'failed_action': failed_action.value,
            'world_state': asdict(world_state),
            'reason': reason,
            'timestamp': time.time()
        })
        
        reflection_responses = {
            ActionType.HEAL_SELF: f"My healing attempt failed: {reason}. I should have checked potion availability first or found alternative healing.",
            ActionType.ATTACK_ENEMY: f"My attack failed: {reason}. Perhaps I overestimated my combat ability or underestimated the enemy.",
            ActionType.RETREAT: f"My retreat failed: {reason}. I should have planned an escape route earlier or called for backup sooner.",
            ActionType.SEARCH_FOR_POTION: f"My search failed: {reason}. I need to remember where potions are typically located or prioritize resource management.",
            ActionType.CALL_BACKUP: f"Backup call failed: {reason}. I should have alternative communication methods or self-reliance strategies.",
            ActionType.DEFEND_TREASURE: f"Defense failed: {reason}. I need better positioning or should have eliminated threats proactively."
        }
        
        base_reflection = reflection_responses.get(failed_action, f"Action {failed_action.value} failed: {reason}")
        learning = " Next time, I'll assess the situation more carefully and have contingency plans ready."
        
        return base_reflection + learning