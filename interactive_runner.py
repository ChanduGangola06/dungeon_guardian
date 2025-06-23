"""
Interactive Runner for Dungeon Guardian
Save this as interactive_runner.py and run it for custom scenarios
"""

from dungeon_guardian import DungeonGuardian, WorldState

def create_custom_scenario():
    """Interactive scenario creator"""
    print("🏰 DUNGEON GUARDIAN - CUSTOM SCENARIO CREATOR")
    print("=" * 50)
    
    try:
        health = int(input("Enter Guardian Health (1-100): "))
        stamina = int(input("Enter Guardian Stamina (1-20): "))
        potion_count = int(input("Enter Potion Count (0-5): "))
        
        print("\nTreasure Threat Level:")
        print("1. Low")
        print("2. Medium") 
        print("3. High")
        threat_choice = int(input("Choose (1-3): "))
        threat_levels = {1: "low", 2: "medium", 3: "high"}
        threat_level = threat_levels.get(threat_choice, "low")
        
        enemy_nearby = input("Enemy Nearby? (y/n): ").lower().startswith('y')
        in_safe_zone = input("In Safe Zone? (y/n): ").lower().startswith('y')
        backup_available = input("Backup Available? (y/n): ").lower().startswith('y')
        
        return WorldState(
            health=max(1, min(100, health)),
            stamina=max(1, min(20, stamina)),
            potion_count=max(0, min(5, potion_count)),
            has_potion=potion_count > 0,
            treasure_threat_level=threat_level,
            enemy_nearby=enemy_nearby,
            is_in_safe_zone=in_safe_zone,
            backup_available=backup_available
        )
    
    except ValueError:
        print("Invalid input! Using default scenario.")
        return WorldState(health=50, stamina=10, potion_count=1, has_potion=True)

def main_menu():
    """Main interactive menu"""
    while True:
        print("\n🏰 DUNGEON GUARDIAN SIMULATOR")
        print("=" * 40)
        print("1. Run All Test Scenarios")
        print("2. Create Custom Scenario")
        print("3. Quick Demo")
        print("4. Exit")
        
        choice = input("\nChoose an option (1-4): ")
        
        if choice == "1":
            print("\n🧪 Running all test scenarios...")
            # Import and run the original test scenarios
            from dungeon_guardian import create_test_scenarios
            scenarios = create_test_scenarios()
            
            for scenario_name, initial_state in scenarios.items():
                print(f"\n{'='*60}")
                print(f"🧪 TESTING: {scenario_name}")
                print(f"{'='*60}")
                
                guardian = DungeonGuardian()
                guardian.run_simulation(initial_state, max_steps=10)
                
                input("\nPress Enter to continue to next scenario...")
        
        elif choice == "2":
            custom_state = create_custom_scenario()
            max_steps = int(input("\nMaximum simulation steps (5-30): ") or "15")
            max_steps = max(5, min(30, max_steps))
            
            print(f"\n🚀 Starting custom simulation...")
            guardian = DungeonGuardian()
            guardian.run_simulation(custom_state, max_steps=max_steps)
        
        elif choice == "3":
            print("\n⚡ Quick Demo - Critical Situation!")
            demo_state = WorldState(
                health=15,
                stamina=3,
                potion_count=0,
                has_potion=False,
                treasure_threat_level="high",
                enemy_nearby=True,
                is_in_safe_zone=False,
                backup_available=True
            )
            guardian = DungeonGuardian()
            guardian.run_simulation(demo_state, max_steps=8)
        
        elif choice == "4":
            print("👋 Thanks for using Dungeon Guardian!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
