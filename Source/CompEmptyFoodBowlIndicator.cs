using RimWorld;
using Verse;
using System.Linq;
using UnityEngine;

namespace FoodBowl
{
    public class CompEmptyFoodBowlIndicator : ThingComp
    {
        private Building_Storage parentStorage;
        private OverlayHandle? emptyOverlayHandle;
        private int lastCheckTick = 0;
        private const int CHECK_INTERVAL_TICKS = 30000; // Check every 30000 ticks about 12 ingame hours

        public CompProperties_EmptyFoodBowlIndicator Props => (CompProperties_EmptyFoodBowlIndicator)props;

        public override void PostSpawnSetup(bool respawningAfterLoad)
        {
            base.PostSpawnSetup(respawningAfterLoad);
            parentStorage = parent as Building_Storage;
            
            // Initialize check tick to avoid immediate check on spawn
            if (!respawningAfterLoad)
            {
                lastCheckTick = Find.TickManager.TicksGame;
            }
        }

        public override void PostExposeData()
        {
            base.PostExposeData();
            Scribe_Values.Look(ref lastCheckTick, "lastCheckTick", 0);
        }

        public override void CompTickRare()
        {
            base.CompTickRare();
            
            // Check every 250 ticks (same as TickerType.Rare interval)
            if (Find.TickManager.TicksGame >= lastCheckTick + CHECK_INTERVAL_TICKS)
            {
                lastCheckTick = Find.TickManager.TicksGame;
                UpdateEmptyIndicator();
            }
        }

        private void UpdateEmptyIndicator()
        {
            if (parentStorage?.slotGroup == null || !parent.Spawned)
            {
                return;
            }

            bool isEmpty = !parentStorage.slotGroup.HeldThings.Any();
  
            if (isEmpty && !emptyOverlayHandle.HasValue)
            {
                // Show empty indicator
                var overlayDrawer = parent.Map?.overlayDrawer;
                if (overlayDrawer != null)
                {
                    emptyOverlayHandle = overlayDrawer.Enable(parent, OverlayTypes.QuestionMark);
                }
            }
            else if (!isEmpty && emptyOverlayHandle.HasValue)
            {
                // Hide empty indicator
                var overlayDrawer = parent.Map?.overlayDrawer;
                if (overlayDrawer != null)
                {
                    overlayDrawer.Disable(parent, ref emptyOverlayHandle);
                }
            }
        }

        public override void PostDeSpawn(Map map, DestroyMode mode = DestroyMode.Vanish)
        {
            base.PostDeSpawn(map, mode);
            
            // Clean up overlay when despawning
            if (emptyOverlayHandle.HasValue)
            {
                map?.overlayDrawer?.Disable(parent, ref emptyOverlayHandle);
            }
        }
    }

    public class CompProperties_EmptyFoodBowlIndicator : CompProperties
    {
        public CompProperties_EmptyFoodBowlIndicator()
        {
            compClass = typeof(CompEmptyFoodBowlIndicator);
        }
    }
}
