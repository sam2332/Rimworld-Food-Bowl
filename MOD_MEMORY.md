# Food Bowl Mod - Development Memory

## Recent Fixes and Changes

### Shadow Fix (Current Session)
**Issue**: Food bowl showing full 1x1 shadow that looked disproportionately large
**Root Cause**: `staticSunShadowHeight` was set to `0.1`, creating a shadow for a small (0.8x0.8) object
**Solution**: 
- Changed `staticSunShadowHeight` from `0.1` to `0` to disable shadows completely
- Small objects like bowls, plant pots, and furniture typically don't cast shadows in RimWorld
- Consistent with game's approach for similar small items with low `fillPercent` values

### Empty Bowl Overlay Fix (Previous Session)
**Issue**: Empty bowl overlay not showing in game
**Root Cause**: `tickerType` was set to `Never`, preventing component from ticking
**Solution**: 
- Changed `tickerType` from `Never` to `Rare` in Buildings_FoodBowl.xml
- Removed debug logging from CompEmptyFoodBowlIndicator.cs

**Technical Details**:
- Components with CompTick() methods require parent objects to have proper ticker types
- `Never` = object never ticks (most static buildings)
- `Rare` = ticks every 250 game ticks (~4 times per second at 1x speed)
- Our component checks every 4 real seconds, so `Rare` provides adequate tick frequency
- Similar to CompRottable which also requires `Rare` or `Normal` ticker types

### Food Filter Simplification (Previous Session)
**Change**: Simplified the allowed food types for Food Bowl storage
**Previous Configuration**: 
- Foods category (too broad) with many specific ThingDefs and exclusions
- Allowed: Hay, Kibble, Milk, InsectJelly, Pemmican, RawBerries, RawFungus, RawAgave
- Disallowed: Human meat, all meals, etc.

**New Configuration**: 
- **Categories**: MeatRaw, PlantFoodRaw (vegetables)
- **Specific Items**: Kibble, Pemmican  
- **Disallowed**: Meat_Human, Meat_Twisted

**Benefits**:
- Much cleaner and more intuitive configuration
- Uses RimWorld's proper food category system
- Covers user's requested "all meats, veggies, kibble, pemmican"
- Eliminates need for long lists of specific items
- Still excludes inappropriate foods (human meat, twisted meat)

### XML Cross-Reference Error Resolution (Previous Session)
**Issue**: Multiple "Could not resolve cross-reference" errors for invalid ThingDef names
**ThingDefs with Errors**:
- `SimpleMeal` → Fixed to `MealSimple`
- `FineMeal` → Fixed to `MealFine` (plus variants `MealFine_Veg`, `MealFine_Meat`)
- `LavishMeal` → Fixed to `MealLavish` (plus variants `MealLavish_Veg`, `MealLavish_Meat`)
- `SurvivalMeal` → Fixed to `MealSurvivalPack`
- `PlantMatter` → Removed (this is a ThingCategory, not a ThingDef)
- `Meat_Insect` → Previously removed (invalid ThingDef)

**Resolution**: Updated `disallowedThingDefs` in Buildings_FoodBowl.xml with correct ThingDef names from RimWorld 1.6 game files.

**Verified Valid ThingDefs in Configuration**:
- Now simplified to use categories instead of long lists

## Key Game Source References
- Meal ThingDefs: `Game XML DEFS/Data/Core/Defs/ThingDefs_Items/Items_Food.xml`
- Plant Resources: `Game XML DEFS/Data/Core/Defs/ThingDefs_Items/Items_Resource_RawPlant.xml`
- Animal Products: `Game XML DEFS/Data/Core/Defs/ThingDefs_Items/Items_Resource_AnimalProduct.xml`

## Build Status
✅ Mod compiles successfully after ThingDef fixes
✅ All XML cross-references resolved
✅ Ready for testing in RimWorld 1.6

## Current Mod Configuration
- **Purpose**: Pet food storage bowl (single-stack)
- **Materials**: Metallic, Woody, Stony (8 cost)
- **Category**: Furniture
- **Storage**: Foods category with pet-focused filter
- **Features**: showStoredThings=false, preventDeteriorationOnTop=true, maxItemsInCell=1
