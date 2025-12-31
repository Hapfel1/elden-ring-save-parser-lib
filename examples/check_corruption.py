"""
Example: Check all characters for corruption
"""

import sys
from pathlib import Path

from elden_ring_save_parser_lib import Save


def main(save_path: str):
    # Load save file
    save = Save.from_file(save_path)
    
    print("=" * 70)
    print("CORRUPTION CHECK")
    print("=" * 70)
    print()
    
    total_corrupted = 0
    
    # Check each active slot
    for slot_idx in save.get_active_slots():
        slot = save.character_slots[slot_idx]
        char_name = slot.player_game_data.character_name
        
        print(f"Slot {slot_idx + 1}: {char_name}")
        print("-" * 70)
        
        # Check for corruption
        has_corruption, issues = slot.has_corruption()
        
        if has_corruption:
            total_corrupted += 1
            print("CORRUPTION DETECTED:")
            
            for issue in issues:
                # Parse issue format: "type:details"
                if ":" in issue:
                    issue_type, details = issue.split(":", 1)
                else:
                    issue_type, details = issue, ""
                
                # Display user-friendly messages
                if issue_type == "torrent_bug":
                    print(f"  • Torrent Bug: {details}")
                    print("    → Torrent stuck in loading state")
                    print("    → Fix: Set state to DEAD")
                elif issue_type == "weather_corruption":
                    print(f"  • Weather Corruption: {details}")
                    print("    → Weather data doesn't match map location")
                    print("    → Fix: Sync AreaId with map")
                elif issue_type == "time_corruption":
                    print(f"  • Time Corruption: {details}")
                    print("    → Time doesn't match playtime")
                    print("    → Fix: Calculate from seconds_played")
                elif issue_type == "steamid_corruption":
                    print(f"  • SteamId Corruption: {details}")
                    print("    → SteamId is invalid")
                    print("    → Fix: Copy from USER_DATA_10")
                else:
                    print(f"  • {issue}")
        else:
            print("No corruption detected")
        
        print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total active slots: {len(save.get_active_slots())}")
    print(f"Corrupted slots: {total_corrupted}")
    print()
    
    if total_corrupted > 0:
        print("Corruption found!")
        print()
        print("To fix corruption:")
        print(f"  python fix_torrent.py {save_path} <slot_number>")
        print()
        print("Or fix programmatically:")
        print("  from elden_ring_save_parser_lib import Save")
        print(f"  save = Save.from_file('{save_path}')")
        print("  save.fix_character_corruption(slot_index)")
        print("  save.recalculate_checksums()")
        print("  save.save()")
        return 1
    else:
        print("✓ All characters are clean!")
        return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_corruption.py <save_file>")
        print()
        print("Example:")
        print("  python check_corruption.py ER0000.sl2")
        print("  python check_corruption.py ER0000.co2")
        sys.exit(1)
    
    save_path = sys.argv[1]
    
    if not Path(save_path).exists():
        print(f"Error: File not found: {save_path}")
        sys.exit(1)
    
    sys.exit(main(save_path))
