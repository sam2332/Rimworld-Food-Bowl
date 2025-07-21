# Food Bowl Mod for RimWorld

A simple RimWorld mod that adds a Food Bowl - a specialized single-stack storage building for food items.

## Features

- **Single-stack storage**: Holds exactly one stack of any food type
- **Food preservation**: Prevents food deterioration just like shelves
- **Affordable**: Cheaper to build than shelves (only 8 materials vs 20 for shelf)
- **Compact**: 1x1 footprint, perfect for small spaces
- **Universal food storage**: Accepts all food categories (raw, cooked, meals, etc.)
- **Easy to build**: No research requirements, available from game start

## Building Requirements

- 8 units of any material (Wood, Steel, Stone blocks, etc.)
- 200 work to build
- Found in Furniture category

## How to Use

1. Build the Food Bowl from the Furniture menu (Misc13 hotkey)
2. Set storage settings like any other storage building
3. By default, it accepts all food types at Important priority
4. Colonists will automatically haul food to the bowl
5. Food stored in the bowl will never deteriorate

## Compatibility

- Compatible with RimWorld 1.6
- No conflicts with other mods
- Uses vanilla storage systems

## Technical Details

- Uses Building_Storage class (same as shelves)
- maxItemsInCell: 1 (single stack only)
- storageGroupTag: "FoodBowl" (can be linked with other food bowls)
- Includes Blueprint_Storage for planning mode

## Installation

1. Subscribe to the mod on Steam Workshop, or
2. Download and extract to your RimWorld/Mods folder
3. Enable in the mod list
4. No save game compatibility issues

## Version History

- v1.0: Initial release
  - Food Bowl building
  - Supports all food types
  - Single-stack storage
  - Food preservation
