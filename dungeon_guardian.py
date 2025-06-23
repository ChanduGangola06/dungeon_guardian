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