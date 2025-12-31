# Elden Ring Save Library

A Python library for parsing, reading, and modifying Elden Ring save files.

## Features

- Parse Elden Ring save files
- Read character data (stats, inventory, equipment, etc)
- Detect corruption (Torrent bug, time/weather desync, SteamId issues)
- Fix corruption automatically
- Modify save data programmatically
- Recalculate checksums

## Installation

```bash
pip install elden-ring-save-parser-lib
```

Or install from source:

```bash
git clone https://github.com/Hapfel1/elden-ring-save-parser-lib
cd elden-ring-save-parser-lib
pip install -e .
```

## Quick Start

### Read Save File

```python
from elden-ring-save-parser-lib import Save

# Load save file
save = Save.from_file("ER0000.sl2")

# Get active character slots
for slot_idx in save.get_active_slots():
    slot = save.character_slots[slot_idx]
    
    # Character info
    char = slot.player_game_data
    print(f"Character: {char.character_name}")
    print(f"Level: {char.level}")
    print(f"Runes: {char.runes}")
    print(f"HP: {char.hp}/{char.max_hp}")
    
    # Location
    map_id = slot.map_id
    print(f"Map: {map_id.to_decimal()}")
```

### Check for Corruption

```python
from elden_ring_save_lib import Save

save = Save.from_file("ER0000.sl2")
slot = save.character_slots[0]

# Check for corruption
has_corruption, issues = slot.has_corruption()

if has_corruption:
    print("Corruption detected:")
    for issue in issues:
        print(f"  - {issue}")
```

### Fix Corruption

```python
from elden_ring_save_lib import Save

save = Save.from_file("ER0000.sl2")

# Fix corruption in slot 0
was_fixed, fixes = save.fix_character_corruption(0)

if was_fixed:
    print("Fixed:")
    for fix in fixes:
        print(f"  - {fix}")
    
    # Recalculate checksums and save
    save.recalculate_checksums()
    save.save()
```

### Modify Character Stats

```python
from elden_ring_save_lib import Save

save = Save.from_file("ER0000.sl2")
char = save.character_slots[0].player_game_data

# Modify stats
char.level = 150
char.runes = 999999
char.vigor = 60

# Save changes
save.recalculate_checksums()
save.save()
```

### Check Torrent Status

```python
from elden_ring_save_lib import Save

save = Save.from_file("ER0000.sl2")
slot = save.character_slots[0]

# Get Torrent data
horse = slot.horse

print(f"Torrent HP: {horse.hp}")
print(f"Torrent State: {horse.state.name}")

# Check for Torrent bug
if slot.has_torrent_bug():
    print("Torrent stuck loading bug detected!")
```

## API Reference

### Main Classes

#### `Save`

Main save file class.

**Methods:**
- `Save.from_file(filepath: str) -> Save` - Load save from file
- `get_active_slots() -> list[int]` - Get list of active character slot indices
- `fix_character_corruption(slot_index: int) -> tuple[bool, list[str]]` - Fix corruption
- `recalculate_checksums()` - Recalculate all checksums
- `save(filepath: str | None = None)` - Save to file

**Properties:**
- `character_slots: list[UserDataX]` - 10 character slots
- `user_data_10_parsed: UserData10` - Common section (SteamId, ProfileSummary)
- `is_ps: bool` - PlayStation save format

#### `UserDataX`

Character slot data.

**Methods:**
- `has_corruption() -> tuple[bool, list[str]]` - Check for any corruption
- `has_torrent_bug() -> bool` - Check for Torrent bug
- `has_weather_corruption() -> bool` - Check for weather corruption
- `has_time_corruption(seconds_played: int | None = None) -> bool` - Check for time corruption
- `has_steamid_corruption() -> bool` - Check for SteamId corruption
- `is_empty() -> bool` - Check if slot is empty

**Properties:**
- `player_game_data: PlayerGameData` - Character stats and data
- `horse: RideGameData` - Torrent data
- `map_id: MapId` - Current map location
- `world_area_time: WorldAreaTime` - In-game time
- `world_area_weather: WorldAreaWeather` - Weather data
- `steam_id: int` - SteamId
- `equip_inventory_data: EquipInventoryData` - Equipment
- `chr_asm: ChrAsm` - Face/appearance data

#### `PlayerGameData`

Character stats and attributes.

**Properties:**
- `character_name: str` - Character name
- `level: int` - Character level
- `runes: int` - Current runes
- `hp: int` - Current HP
- `max_hp: int` - Maximum HP
- `fp: int` - Current FP
- `max_fp: int` - Maximum FP
- `sp: int` - Current stamina
- `max_sp: int` - Maximum stamina
- `vigor: int` - Vigor stat
- `mind: int` - Mind stat
- `endurance: int` - Endurance stat
- `strength: int` - Strength stat
- `dexterity: int` - Dexterity stat
- `intelligence: int` - Intelligence stat
- `faith: int` - Faith stat
- `arcane: int` - Arcane stat

#### `RideGameData`

Torrent (horse) data.

**Properties:**
- `hp: int` - Torrent HP
- `state: HorseState` - Torrent state (INACTIVE, DEAD, ACTIVE)
- `coordinates: FloatVector3` - Torrent position
- `map_id: MapId` - Torrent map location
- `angle: FloatVector4` - Torrent rotation

**Methods:**
- `has_bug() -> bool` - Check for infinite loading bug (HP=0, State=ACTIVE)
- `fix_bug()` - Fix the bug (set State to DEAD)

#### `MapId`

Map location identifier.

**Methods:**
- `to_decimal() -> str` - Convert to decimal format ("60 42 36 0")
- `to_hex_string() -> str` - Convert to hex format ("00_24_2A_3C")
- `is_dlc() -> bool` - Check if location is in Shadow of the Erdtree DLC

### Data Types

- `FloatVector3` - 3D float vector (x, y, z)
- `FloatVector4` - 4D float vector (x, y, z, w)
- `Gaitem` - Variable-length item structure
- `HorseState` - Enum (INACTIVE=1, DEAD=3, ACTIVE=13)

### Exceptions

- `SaveFileError` - Base exception
- `CorruptedSaveError` - Save file is corrupted
- `UnsupportedVersionError` - Save version not supported
- `ChecksumMismatchError` - Checksum validation failed

## Corruption Types

The library can detect and fix:

1. **Torrent Bug** - HP=0 with State=ACTIVE causes infinite loading
2. **Time Corruption** - WorldAreaTime doesn't match seconds_played
3. **Weather Corruption** - WorldAreaWeather.AreaId doesn't match map location
4. **SteamId Corruption** - SteamId is 0 in character slot

## Examples

See the `examples/` directory for more examples:

- `read_save.py` - Read and display save information
- `fix_torrent.py` - Fix Torrent infinite loading bug
- `check_corruption.py` - Check all characters for corruption
- `modify_stats.py` - Modify character stats

## Development

```bash
# Clone repository
git clone https://github.com/Hapfel1/elden-ring-save-parser-lib
cd elden-ring-save-parser-lib

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

## Credits

Based on reverse engineering work and the Rust ER-Save-Lib implementation.

## License

MIT License - See LICENSE file for details

## Disclaimer

This library is for educational purposes. Use at your own risk. Always backup your save files before modifying them.