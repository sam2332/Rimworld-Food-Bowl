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
        private float lastCheckTime = 0f;
        private const float CHECK_INTERVAL_SECONDS = 4f; // Check every 4 seconds

        public CompProperties_EmptyFoodBowlIndicator Props => (CompProperties_EmptyFoodBowlIndicator)props;

        public override void PostSpawnSetup(bool respawningAfterLoad)
        {
            base.PostSpawnSetup(respawningAfterLoad);
            parentStorage = parent as Building_Storage;
            
            // Initialize check time to avoid immediate check on spawn
            if (!respawningAfterLoad)
            {
                lastCheckTime = UnityEngine.Time.time;
            }
        }

        public override void PostExposeData()
        {
            base.PostExposeData();
            Scribe_Values.Look(ref lastCheckTime, "lastCheckTime", 0f);
        }

        public override void CompTick()
        {
            base.CompTick();
            
            // Check every 4 real seconds regardless of game speed
            if (UnityEngine.Time.time >= lastCheckTime + CHECK_INTERVAL_SECONDS)
            {
                lastCheckTime = UnityEngine.Time.time;
                UpdateEmptyIndicator();
            }
        }

        private void UpdateEmptyIndicator()
        {
            if (parentStorage?.slotGroup == null || !parent.Spawned)
                return;

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
