"""
Example: Modify character stats
"""

import sys
from pathlib import Path
import shutil

from elden_ring_save_parser_lib import Save


def main(save_path: str, slot_index: int):
    # Load save file
    save = Save.from_file(save_path)
    
    # Validate slot
    if slot_index < 0 or slot_index >= 10:
        print(f"Error: Slot index must be 0-9, got {slot_index}")
        return 1
    
    slot = save.character_slots[slot_index]
    
    if slot.is_empty():
        print(f"Error: Slot {slot_index} is empty")
        return 1
    
    char = slot.player_game_data
    
    print("=" * 70)
    print(f"MODIFY CHARACTER STATS - {char.character_name}")
    print("=" * 70)
    print()
    
    # Show current stats
    print("Current Stats:")
    print("-" * 70)
    print(f"Level: {char.level}")
    print(f"Runes: {char.runes:,}")
    print(f"HP: {char.hp}/{char.max_hp}")
    print(f"FP: {char.fp}/{char.max_fp}")
    print(f"Stamina: {char.sp}/{char.max_sp}")
    print()
    print("Attributes:")
    print(f"  Vigor: {char.vigor}")
    print(f"  Mind: {char.mind}")
    print(f"  Endurance: {char.endurance}")
    print(f"  Strength: {char.strength}")
    print(f"  Dexterity: {char.dexterity}")
    print(f"  Intelligence: {char.intelligence}")
    print(f"  Faith: {char.faith}")
    print(f"  Arcane: {char.arcane}")
    print()
    
    # Ask for confirmation
    print("What would you like to modify?")
    print()
    print("Examples:")
    print("  1. Max out stats (Level 713, all stats 99)")
    print("  2. Give runes (999,999,999)")
    print("  3. Max HP/FP/Stamina")
    print("  4. Custom modification")
    print("  0. Cancel")
    print()
    
    choice = input("Enter choice (0-4): ").strip()
    
    if choice == "0":
        print("Cancelled.")
        return 0
    
    # Create backup
    backup_path = Path(save_path).with_suffix(".backup")
    print()
    print(f"Creating backup: {backup_path}")
    shutil.copy2(save_path, backup_path)
    
    # Apply modifications
    modified = False
    
    if choice == "1":
        # Max out everything
        print()
        print("Maxing out stats...")
        char.level = 713
        char.vigor = 99
        char.mind = 99
        char.endurance = 99
        char.strength = 99
        char.dexterity = 99
        char.intelligence = 99
        char.faith = 99
        char.arcane = 99
        char.runes = 999999999
        modified = True
        print("Level set to 713")
        print("All attributes set to 99")
        print("Runes set to 999,999,999")
    
    elif choice == "2":
        # Give runes
        print()
        runes = input("Enter runes amount (default 999999999): ").strip()
        if runes:
            char.runes = int(runes)
        else:
            char.runes = 999999999
        modified = True
        print(f"  ✓ Runes set to {char.runes:,}")
    
    elif choice == "3":
        # Max HP/FP/Stamina
        print()
        print("Maxing HP/FP/Stamina...")
        char.max_hp = 2100  # Soft cap with buffs
        char.hp = char.max_hp
        char.max_fp = 450   # Soft cap
        char.fp = char.max_fp
        char.max_sp = 180   # Soft cap
        char.sp = char.max_sp
        modified = True
        print("  ✓ HP set to 2100/2100")
        print("  ✓ FP set to 450/450")
        print("  ✓ Stamina set to 180/180")
    
    elif choice == "4":
        # Custom modification
        print()
        print("Custom modification (press Enter to skip):")
        print()
        
        level = input(f"Level (current: {char.level}): ").strip()
        if level:
            char.level = int(level)
            modified = True
        
        runes = input(f"Runes (current: {char.runes}): ").strip()
        if runes:
            char.runes = int(runes)
            modified = True
        
        vigor = input(f"Vigor (current: {char.vigor}): ").strip()
        if vigor:
            char.vigor = int(vigor)
            modified = True
        
        mind = input(f"Mind (current: {char.mind}): ").strip()
        if mind:
            char.mind = int(mind)
            modified = True
        
        endurance = input(f"Endurance (current: {char.endurance}): ").strip()
        if endurance:
            char.endurance = int(endurance)
            modified = True
        
        strength = input(f"Strength (current: {char.strength}): ").strip()
        if strength:
            char.strength = int(strength)
            modified = True
        
        dexterity = input(f"Dexterity (current: {char.dexterity}): ").strip()
        if dexterity:
            char.dexterity = int(dexterity)
            modified = True
        
        intelligence = input(f"Intelligence (current: {char.intelligence}): ").strip()
        if intelligence:
            char.intelligence = int(intelligence)
            modified = True
        
        faith = input(f"Faith (current: {char.faith}): ").strip()
        if faith:
            char.faith = int(faith)
            modified = True
        
        arcane = input(f"Arcane (current: {char.arcane}): ").strip()
        if arcane:
            char.arcane = int(arcane)
            modified = True
    
    else:
        print("Invalid choice.")
        return 1
    
    if not modified:
        print("No modifications made.")
        return 0
    
    # Save changes
    print()
    print("Recalculating checksums...")
    save.recalculate_checksums()
    
    print(f"Saving to: {save_path}")
    save.save()
    
    print()
    print("=" * 70)
    print("CHARACTER MODIFIED SUCCESSFULLY")
    print("=" * 70)
    print()
    print("Modified:")
    print(f"  Character: {char.character_name}")
    print(f"  Level: {char.level}")
    print(f"  Runes: {char.runes:,}")
    print()
    print(f"Backup: {backup_path}")
    print()
    print("WARNING: Using modified stats may be considered cheating!")
    print("   Use at your own risk.")
    
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python modify_stats.py <save_file> <slot_index>")
        print()
        print("Example:")
        print("  python modify_stats.py ER0000.sl2 0")
        print()
        print("Slot indices: 0-9 (Slot 1 = index 0)")
        sys.exit(1)
    
    save_path = sys.argv[1]
    slot_index = int(sys.argv[2])
    
    if not Path(save_path).exists():
        print(f"Error: File not found: {save_path}")
        sys.exit(1)
    
    try:
        sys.exit(main(save_path, slot_index))
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
