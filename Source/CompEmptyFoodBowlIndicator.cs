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

        public CompProperties_EmptyFoodBowlIndicator Props => (CompProperties_EmptyFoodBowlIndicator)props;

        public override void PostSpawnSetup(bool respawningAfterLoad)
        {
            base.PostSpawnSetup(respawningAfterLoad);
            parentStorage = parent as Building_Storage;
        }

        public override void CompTickRare()
        {
            base.CompTickRare();
            
            // Check every 250 ticks (TickerType.Rare interval) for responsive updates
            UpdateEmptyIndicator();
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
