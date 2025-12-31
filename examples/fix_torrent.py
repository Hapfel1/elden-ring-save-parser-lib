"""
Example: Fix Torrent infinite loading bug
"""

import sys
from pathlib import Path

from elden_ring_save_parser_lib import Save


def main(save_path: str, slot_index: int):
    # Load save file
    save = Save.from_file(save_path)
    
    # Check slot
    if slot_index < 0 or slot_index >= 10:
        print(f"Error: Slot index must be 0-9, got {slot_index}")
        return 1
    
    slot = save.character_slots[slot_index]
    
    if slot.is_empty():
        print(f"Error: Slot {slot_index} is empty")
        return 1
    
    char_name = slot.player_game_data.character_name
    print(f"Character: {char_name} (Slot {slot_index})")
    print()
    
    # Check Torrent status
    horse = slot.horse
    if not horse:
        print("Error: No Torrent data found")
        return 1
    
    print(f"Torrent HP: {horse.hp}")
    print(f"Torrent State: {horse.state.name}")
    print()
    
    # Check for bug
    if not horse.has_bug():
        print("✓ Torrent is OK - no bug detected")
        return 0
    
    print("TORRENT BUG DETECTED!")
    print("   HP=0 with State=ACTIVE causes infinite loading")
    print()
    
    # Create backup
    backup_path = Path(save_path).with_suffix(".backup")
    print(f"Creating backup: {backup_path}")
    import shutil
    shutil.copy2(save_path, backup_path)
    print()
    
    # Fix the bug
    print("Fixing Torrent bug...")
    was_fixed, fixes = save.fix_character_corruption(slot_index)
    
    if was_fixed:
        print("✓ Fixed:")
        for fix in fixes:
            print(f"  - {fix}")
        print()
        
        # Recalculate checksums and save
        print("Recalculating checksums...")
        save.recalculate_checksums()
        
        print(f"Saving to: {save_path}")
        save.save()
        
        print()
        print("Done! Torrent bug fixed.")
        print(f"  Backup: {backup_path}")
        return 0
    else:
        print("Error: Could not fix Torrent bug")
        return 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python fix_torrent.py <save_file> <slot_index>")
        print()
        print("Example:")
        print("  python fix_torrent.py ER0000.sl2 0")
        sys.exit(1)
    
    save_path = sys.argv[1]
    slot_index = int(sys.argv[2])
    
    sys.exit(main(save_path, slot_index))