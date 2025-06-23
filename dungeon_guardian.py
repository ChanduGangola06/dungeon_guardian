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
    
# ==================== COGNITIVE LAYER (LLM SIMULATION) ====================

class CognitiveEngine:
    """Simulates LLM-based reasoning for goal generation and reflection"""
    
    def __init__(self):
        self.memory = []
        
    def generate_goal(self, world_state: WorldState) -> Tuple[GoalType, str]:
        """Generate a goal based on current world state with reasoning"""
        
        reasoning_context = self._analyze_situation(world_state)
        
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
    
    def _analyze_situation(self, world_state: WorldState) -> Dict[str, str]:
        """Analyze current situation for reasoning context"""
        context = {}
        
        # Health analysis
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

# ==================== PLANNING LAYER (GOAP) ====================

@dataclass
class Action:
    action_type = ActionType
    preconditions: Dict[str, Any]
    effects: Dict[str, Any]
    cost: int = 1

class GOAPPlanner:
    
    def __init__(self):
        self.actions = self._define_actions()
        
    def _define_actions(self) -> List[Action]:
        """Define all available actions with preconditions and effects"""
        return [
            Action(
                ActionType.HEAL_SELF,
                preconditions={'has_potion': True},
                effects={'health': lambda h: min(100, h + 40), 'has_potion': False, 'potion_count': lambda p: max(0, p - 1)},
                cost=1
            ),
            Action(
                ActionType.ATTACK_ENEMY,
                preconditions={'enemy_nearby': True, 'stamina': lambda s: s >= 5},
                effects={'enemy_nearby': False, 'stamina': lambda s: s - 5, 'health': lambda h: h - random.randint(0, 15)},
                cost=2
            ),
            Action(
                ActionType.RETREAT,
                preconditions={'is_in_safe_zone': False},
                effects={'is_in_safe_zone': True, 'enemy_nearby': False, 'stamina': lambda s: s - 2},
                cost=1
            ),
            Action(
                ActionType.DEFEND_TREASURE,
                preconditions={'treasure_threat_level': lambda t: t in ['medium', 'high']},
                effects={'treasure_threat_level': 'low', 'stamina': lambda s: s - 3},
                cost=2
            ),
            Action(
                ActionType.CALL_BACKUP,
                preconditions={'backup_available': True},
                effects={'enemy_nearby': False, 'backup_available': False, 'treasure_threat_level': 'low'},
                cost=3
            ),
            Action(
                ActionType.SEARCH_FOR_POTION,
                preconditions={'potion_count': lambda p: p < 3},
                effects={'has_potion': True, 'potion_count': lambda p: p + 1, 'stamina': lambda s: s - 1},
                cost=1
            )
        ]
        
    def plan(self, start_state: WorldState, goal_conditions: Dict[str, Any]) -> List[ActionType]:
        """Create a plan using A* algorithm"""
        
        open_list = [(0, 0, start_state, [])]  # (f_score, g_score, state, actions)
        closed_set = set()
        
        while open_list:
            f_score, g_score, current_state, actions = heapq.heappop(open_list)
            
            state_key = self._state_to_key(current_state)
            if state_key in closed_set:
                continue
            closed_set.add(state_key)
            
            # Check if goal is satisfied
            if self._goal_satisfied(current_state, goal_conditions):
                return actions
            
            # Try each action
            for action in self.actions:
                if self._can_execute_action(current_state, action):
                    new_state = self._apply_action(current_state, action)
                    new_actions = actions + [action.action_type]
                    new_g_score = g_score + action.cost
                    new_f_score = new_g_score + self._heuristic(new_state, goal_conditions)
                    
                    heapq.heappush(open_list, (new_f_score, new_g_score, new_state, new_actions))
        
        return []  # No plan found
    
    def _can_execute_action(self, state: WorldState, action: Action) -> bool:
        """Check if action preconditions are met"""
        state_dict = asdict(state)
        
        for key, condition in action.preconditions.items():
            if key not in state_dict:
                return False
            
            if callable(condition):
                if not condition(state_dict[key]):
                    return False
            else:
                if state_dict[key] != condition:
                    return False
        
        return True
    
    def _apply_action(self, state: WorldState, action: Action) -> WorldState:
        """Apply action effects to create new state"""
        new_state = state.copy()
        new_state_dict = asdict(new_state)
        
        for key, effect in action.effects.items():
            if key in new_state_dict:
                if callable(effect):
                    new_value = effect(new_state_dict[key])
                else:
                    new_value = effect
                setattr(new_state, key, new_value)
        
        return new_state
    
    def _goal_satisfied(self, state: WorldState, goal_conditions: Dict[str, Any]) -> bool:
        """Check if goal conditions are satisfied"""
        state_dict = asdict(state)
        
        for key, condition in goal_conditions.items():
            if key not in state_dict:
                return False
            
            if callable(condition):
                if not condition(state_dict[key]):
                    return False
            else:
                if state_dict[key] != condition:
                    return False
        
        return True
    
    def _heuristic(self, state: WorldState, goal_conditions: Dict[str, Any]) -> int:
        """Simple heuristic for A* (can be improved)"""
        score = 0
        state_dict = asdict(state)
        
        for key, condition in goal_conditions.items():
            if key in state_dict:
                if callable(condition):
                    if not condition(state_dict[key]):
                        score += 1
                else:
                    if state_dict[key] != condition:
                        score += 1
        
        return score
    
    def _state_to_key(self, state: WorldState) -> str:
        """Convert state to hashable key"""
        return json.dumps(asdict(state), sort_keys=True)

# ==================== EXECUTION LAYER ====================

class SimulationEngine:
    """Simulates world state changes and action execution"""
    
    def __init__(self):
        self.failure_chance = 0.1  # 10% chance of action failure
    
    def execute_action(self, action: ActionType, world_state: WorldState) -> Tuple[bool, str, WorldState]:
        """Execute an action and return success status, message, and new state"""
        
        # Simulate random failures
        if random.random() < self.failure_chance:
            failure_reason = self._generate_failure_reason(action)
            return False, failure_reason, world_state
        
        # Apply action effects (simplified simulation)
        new_state = world_state.copy()
        success_message = ""
        
        if action == ActionType.HEAL_SELF:
            if world_state.has_potion:
                new_state.health = min(100, world_state.health + 40)
                new_state.has_potion = False
                new_state.potion_count = max(0, world_state.potion_count - 1)
                success_message = f"Healed successfully! Health restored to {new_state.health}%"
            else:
                return False, "No potions available for healing", world_state
                
        elif action == ActionType.ATTACK_ENEMY:
            if world_state.enemy_nearby and world_state.stamina >= 5:
                new_state.enemy_nearby = False
                new_state.stamina = world_state.stamina - 5
                damage_taken = random.randint(0, 15)
                new_state.health = max(0, world_state.health - damage_taken)
                success_message = f"Enemy defeated! Took {damage_taken} damage, stamina reduced by 5"
            else:
                return False, "Cannot attack: no enemy nearby or insufficient stamina", world_state
                
        elif action == ActionType.RETREAT:
            if not world_state.is_in_safe_zone:
                new_state.is_in_safe_zone = True
                new_state.enemy_nearby = False
                new_state.stamina = max(0, world_state.stamina - 2)
                success_message = "Successfully retreated to safe zone"
            else:
                return False, "Already in safe zone", world_state
                
        elif action == ActionType.DEFEND_TREASURE:
            if world_state.treasure_threat_level in ['medium', 'high']:
                new_state.treasure_threat_level = 'low'
                new_state.stamina = max(0, world_state.stamina - 3)
                success_message = "Treasure successfully defended"
            else:
                return False, "No significant threat to treasure", world_state
                
        elif action == ActionType.CALL_BACKUP:
            if world_state.backup_available:
                new_state.enemy_nearby = False
                new_state.backup_available = False
                new_state.treasure_threat_level = 'low'
                success_message = "Backup called successfully! Threats neutralized"
            else:
                return False, "Backup not available", world_state
                
        elif action == ActionType.SEARCH_FOR_POTION:
            if world_state.potion_count < 3:
                new_state.has_potion = True
                new_state.potion_count = world_state.potion_count + 1
                new_state.stamina = max(0, world_state.stamina - 1)
                success_message = f"Found a potion! Now have {new_state.potion_count} potions"
            else:
                return False, "Already carrying maximum potions", world_state
        
        return True, success_message, new_state
    
    def _generate_failure_reason(self, action: ActionType) -> str:
        """Generate contextual failure reasons"""
        failure_reasons = {
            ActionType.HEAL_SELF: "Potion was spoiled/stolen during attempt",
            ActionType.ATTACK_ENEMY: "Enemy dodged attack and counterattacked",
            ActionType.RETREAT: "Escape route was blocked",
            ActionType.DEFEND_TREASURE: "Overwhelmed by multiple attackers",
            ActionType.CALL_BACKUP: "Communication device malfunctioned",
            ActionType.SEARCH_FOR_POTION: "Search area was already looted"
        }
        return failure_reasons.get(action, "Unknown failure occurred")
    
    def introduce_world_changes(self, world_state: WorldState) -> WorldState:
        """Simulate random world state changes"""
        new_state = world_state.copy()
        
        # Random events
        if random.random() < 0.2:  # 20% chance of enemy appearance
            new_state.enemy_nearby = True
        
        if random.random() < 0.15:  # 15% chance of treasure threat increase
            threat_levels = ['low', 'medium', 'high']
            current_index = threat_levels.index(world_state.treasure_threat_level)
            if current_index < len(threat_levels) - 1:
                new_state.treasure_threat_level = threat_levels[current_index + 1]
        
        # Gradual stamina recovery when in safe zone
        if world_state.is_in_safe_zone and world_state.stamina < 20:
            new_state.stamina = min(20, world_state.stamina + 2)
        
        return new_state

# ==================== MAIN AGENT ====================

class DungeonGuardian:
    """The main Sentient Guardian agent"""
    
    def __init__(self):
        self.cognitive_engine = CognitiveEngine()
        self.planner = GOAPPlanner()
        self.simulator = SimulationEngine()
        
        self.current_state = WorldState()
        self.current_goal = None
        self.current_plan = []
        self.step_count = 0
    
    def run_simulation(self, initial_state: WorldState, max_steps: int = 20):
        """Run the main simulation loop"""
        self.current_state = initial_state
        
        print("🏰 DUNGEON GUARDIAN SIMULATION STARTED 🏰")
        print("=" * 60)
        self._print_world_state()
        
        for step in range(max_steps):
            self.step_count = step + 1
            print(f"\n📍 STEP {self.step_count}")
            print("-" * 40)
            
            # Generate goal using cognitive layer
            goal, goal_reasoning = self.cognitive_engine.generate_goal(self.current_state)
            self.current_goal = goal
            
            print(f"🎯 GOAL: {goal.value}")
            print(f"💭 REASONING: {goal_reasoning}")
            
            # Convert goal to GOAP conditions
            goal_conditions = self._goal_to_conditions(goal)
            
            # Plan actions
            plan = self.planner.plan(self.current_state, goal_conditions)
            
            if not plan:
                print("❌ No valid plan found! Ending simulation.")
                break
            
            self.current_plan = plan
            print(f"📋 PLAN: {' → '.join([action.value for action in plan])}")
            
            # Execute first action in plan
            if plan:
                action = plan[0]
                action_reasoning = self.cognitive_engine.justify_action(action, self.current_state, goal)
                print(f"⚡ EXECUTING: {action.value}")
                print(f"💭 WHY: {action_reasoning}")
                
                success, message, new_state = self.simulator.execute_action(action, self.current_state)
                
                if success:
                    print(f"✅ SUCCESS: {message}")
                    self.current_state = new_state
                else:
                    print(f"❌ FAILED: {message}")
                    reflection = self.cognitive_engine.reflect_on_failure(action, self.current_state, message)
                    print(f"🤔 REFLECTION: {reflection}")
            
            # Introduce world changes
            self.current_state = self.simulator.introduce_world_changes(self.current_state)
            
            # Print updated state
            self._print_world_state()
            
            # Check if simulation should continue
            if self._should_end_simulation():
                print("\n🏁 SIMULATION COMPLETED SUCCESSFULLY!")
                break
            
            time.sleep(0.5)  # Brief pause for readability
    
    def _goal_to_conditions(self, goal: GoalType) -> Dict[str, Any]:
        """Convert high-level goals to GOAP conditions"""
        goal_mappings = {
            GoalType.SURVIVE: {
                'health': lambda h: h >= 50,
                'is_in_safe_zone': True
            },
            GoalType.ELIMINATE_THREAT: {
                'enemy_nearby': False,
                'treasure_threat_level': 'low'
            },
            GoalType.PROTECT_TREASURE: {
                'treasure_threat_level': 'low'
            },
            GoalType.PREPARE_FOR_BATTLE: {
                'stamina': lambda s: s >= 15,
                'has_potion': True
            }
        }
        return goal_mappings.get(goal, {})
    
    def _print_world_state(self):
        """Print current world state in a readable format"""
        print(f"\n🌍 WORLD STATE:")
        print(f"   ❤️  Health: {self.current_state.health}%")
        print(f"   ⚡ Stamina: {self.current_state.stamina}")
        print(f"   🧪 Potions: {self.current_state.potion_count} ({'Has' if self.current_state.has_potion else 'None'})")
        print(f"   💎 Treasure Threat: {self.current_state.treasure_threat_level}")
        print(f"   👹 Enemy Nearby: {'Yes' if self.current_state.enemy_nearby else 'No'}")
        print(f"   🛡️  Safe Zone: {'Yes' if self.current_state.is_in_safe_zone else 'No'}")
        print(f"   📞 Backup Available: {'Yes' if self.current_state.backup_available else 'No'}")
    
    def _should_end_simulation(self) -> bool:
        """Check if simulation should end"""
        # End if guardian is defeated
        if self.current_state.health <= 0:
            print("\n💀 GUARDIAN DEFEATED!")
            return True
        
        # End if in a stable, safe state
        if (self.current_state.health >= 70 and 
            not self.current_state.enemy_nearby and 
            self.current_state.treasure_threat_level == 'low' and
            self.current_state.is_in_safe_zone):
            return True
        
        return False

# ==================== TEST SCENARIOS ====================

def create_test_scenarios():
    """Create the test scenarios from the requirements"""
    
    scenarios = {
        "Scenario 1: Low Health, No Healing, Enemy Nearby": WorldState(
            health=20,
            enemy_nearby=True,
            has_potion=False,
            treasure_threat_level="medium",
            stamina=5,
            is_in_safe_zone=False,
            potion_count=0
        ),
        
        "Scenario 2: Healthy, Treasure Under Threat": WorldState(
            health=85,
            enemy_nearby=True,
            has_potion=True,
            treasure_threat_level="high",
            stamina=15,
            is_in_safe_zone=False,
            potion_count=1
        ),
        
        "Scenario 3: No Enemy, Low Stamina, Potion Available": WorldState(
            health=70,
            enemy_nearby=False,
            has_potion=True,
            treasure_threat_level="low",
            stamina=2,
            is_in_safe_zone=True,
            potion_count=1
        ),
        
        "Scenario 4: No Potions, Enemy Near, Treasure Safe": WorldState(
            health=60,
            enemy_nearby=True,
            has_potion=False,
            treasure_threat_level="low",
            stamina=10,
            is_in_safe_zone=False,
            potion_count=0
        )
    }
    
    return scenarios

# ==================== MAIN EXECUTION ====================

if __name__ == "__main__":
    print("🏰 INITIALIZING DUNGEON GUARDIAN AI SYSTEM 🏰")
    
    # Run test scenarios
    scenarios = create_test_scenarios()
    
    for scenario_name, initial_state in scenarios.items():
        print(f"\n{'='*80}")
        print(f"🧪 TESTING: {scenario_name}")
        print(f"{'='*80}")
        
        guardian = DungeonGuardian()
        guardian.run_simulation(initial_state, max_steps=15)
        
        print(f"\n{'='*80}")
        print("📊 SCENARIO COMPLETE")
        print(f"{'='*80}")
        
        # Brief pause between scenarios
        time.sleep(1)
    
    print(f"\n🎉 ALL SCENARIOS COMPLETED!")
    print("Check the output above to see how the Guardian reasoned through each situation.")
