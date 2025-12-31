"""
Example: Read and display save file information
"""

from elden_ring_save_parser_lib import Save


def main():
    # Load save file
    save = Save.from_file("ER0000.sl2")
    
    print("=" * 70)
    print("ELDEN RING SAVE FILE")
    print("=" * 70)
    print(f"Format: {'PlayStation' if save.is_ps else 'PC'}")
    print(f"Active slots: {len(save.get_active_slots())}/10")
    print()
    
    # Display each active character
    for slot_idx in save.get_active_slots():
        slot = save.character_slots[slot_idx]
        char = slot.player_game_data
        
        print(f"SLOT {slot_idx + 1}: {char.character_name}")
        print("-" * 70)
        
        # Basic info
        print(f"Level: {char.level}")
        print(f"Runes: {char.runes:,}")
        print(f"HP: {char.hp}/{char.max_hp}")
        print(f"FP: {char.fp}/{char.max_fp}")
        print(f"Stamina: {char.sp}/{char.max_sp}")
        print()
        
        # Stats
        print("Stats:")
        print(f"  Vigor: {char.vigor}")
        print(f"  Mind: {char.mind}")
        print(f"  Endurance: {char.endurance}")
        print(f"  Strength: {char.strength}")
        print(f"  Dexterity: {char.dexterity}")
        print(f"  Intelligence: {char.intelligence}")
        print(f"  Faith: {char.faith}")
        print(f"  Arcane: {char.arcane}")
        print()
        
        # Location
        map_id = slot.map_id
        print(f"Location: {map_id.to_decimal()}")
        if map_id.is_dlc():
            print("  (Shadow of the Erdtree DLC)")
        print()
        
        # Torrent
        horse = slot.horse
        if horse:
            print(f"Torrent HP: {horse.hp}")
            print(f"Torrent State: {horse.state.name}")
            if horse.has_bug():
                print("TORRENT BUG DETECTED!")
        print()
        
        # Check corruption
        has_corruption, issues = slot.has_corruption()
        if has_corruption:
            print("CORRUPTION DETECTED:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("No corruption detected")
        
        print()


if __name__ == "__main__":
    main()