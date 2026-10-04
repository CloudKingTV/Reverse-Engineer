# Core Keeper API surface (from open-source mods)

Game type names referenced by open-source community mods (CoreLib, limoka/CoreKeeperMods (MIT), Valgard/ck_mod_settings_menu), with types the mods declare themselves removed. **Names only:** this shows *what exists*, not how it works. Use it to orient the decompile once the real DLLs are available.

Caveat: the filter is a heuristic, so a few Unity, .NET or helper-method names may remain.

## IComponentData (…CD) (106)

`AnimationOrientationCD`, `AnvilCD`, `BlockSaveCD`, `BossCD`, `CattleCD`, `ChanceToDropLootCD`, `ColliderCacheCD`, `CommandMinionWeaponCD`, `ConditionsTableCD`, `ConnectionAdminLevelCD`, `ConsumesManaCD`, `CookedFoodCD`, `CookingIngredientCD`, `CooldownCD`, `CoreBossSpawnCD`, `CraftingCD`, `CraftingSlotsNeedPrerequisitesCheckCD`, `CraftingVisualCD`, `CritterCD`, `CritterCatchingCD`, `DamageReductionCD`, `DatabaseBankCD`, `DestroyEntityIfNotOnTileCD`, `DestroyEntityIfPlacementNotValidCD`, `DestructibleObjectCD`, `DiggableCD`, `DirectionBasedOnVariationCD`, `DirectionCD`, `DisablePhysicsCD`, `DistanceToPlayerCD`, `DontBlockDiggingCD`, `DontDropLootCD`, `DontDropSelfCD`, `DropLootDelayCD`, `DropsLootFromLootTableCD`, `DropsLootWhenDamagedCD`, `DurabilityCD`, `EffectEventCD`, `ElectricityCD`, `EntityDestroyedCD`, `EquipmentSlotCD`, `EquippedObjectCD`, `EventTerminalCD`, `ExtractableCD`, `ExtractorCD`, `FactionCD`, `FireflyCD`, `FishingCD`, `FullnessCD`, `GhostEffectEventBufferPointerCD`, `GodModeCD`, `GroundDecorationCD`, `GrowingCD`, `HealthCD`, `HungerCD`, `IncineratorCD`, `IndestructibleCD`, `IsExplosiveCD`, `KilledByPlayerCD`, `LevelCD`, `MealsEatenCD`, `MeleeWeaponCD`, `MineableDamageDecreaseCD`, `MinionCD`, `MoveToPredictedByEntityDestroyedCD`, `ObjectDataCD`, `ObjectPropertiesCD`, `OwnerReferenceCD`, `PaintToolCD`, `PaintableObjectCD`, `PetCD`, `PetCandyCD`, `PheromoneAdderCD`, `PlacementCD`, `PlantCD`, `PlayAnimationStateCD`, `PlayerCustomizationCD`, `PlayerInvincibilityCD`, `PlayerMovementCD`, `PlayerStateCD`, `PortalCD`, `PotionCD`, `ProximityTriggerCD`, `PseudoTileCD`, `PugAutomationCD`, `RandomCD`, `RecipeCD`, `ReduceDurabilityOfEquippedTriggerCD`, `RequiresDrillCD`, `ResizableTileSizeCD`, `RootPlantCD`, `SecondaryUseCD`, `SeedCD`, `SerializeWorldDataCD`, `SummonAreaCD`, `SurfacePriorityCD`, `TileCD`, `TileWithTilesetToObjectDataMapCD`, `TriggerAnimationOnDeathCD`, `TriggerSelectEnemyToAttackForMinionCommandCD`, `WaitingForEatableSlotConsumeResultCD`, `WarmupCD`, `WaterSourceCD`, `WaterSpreaderCD`, `WayPointCD`, `WorldInfoCD`

## Dynamic buffers (23)

`AdaptiveEntityBuffer`, `CompanionEntityBuffer`, `ConditionsBuffer`, `ContainedObjectsBuffer`, `DealDamageToEntityBuffer`, `DropsLootBuffer`, `DynamicBuffer`, `EffectEventBuffer`, `GhostEffectEventBuffer`, `GivesConditionsWhenEquippedBuffer`, `HealthChangeBuffer`, `IncludedCraftingBuildingsBuffer`, `InventoryBuffer`, `InventoryChangeBuffer`, `LevelEntitiesBuffer`, `NeedTileUpdateBuffer`, `PlacementSizeByEquipmentTypeBuffer`, `SetupCanCraftBuffer`, `SkillBuffer`, `SkillConditionsBuffer`, `SummarizedConditionEffectsBuffer`, `SummarizedConditionsBuffer`, `TileUpdateBuffer`

## Authoring components (28)

`AlwaysDropSpecificVariationAuthoring`, `CookingIngredientAuthoring`, `CooldownAuthoring`, `CraftingAuthoring`, `DamageReductionAuthoring`, `DeathStateAuthoring`, `DontDropSelfAuthoring`, `DropLootAuthoring`, `FlowerAuthoring`, `HealthAuthoring`, `IdleStateAuthoring`, `IgnoreVertexOffsetsAuthoring`, `InventoryAuthoring`, `InventoryItemAuthoring`, `LinkedEntityGroupAuthoring`, `LocalInteractableAuthoring`, `MigrateToAuthoring`, `MineableAuthoring`, `ModAPIAuthoring`, `NonHittableAuthoring`, `ObjectAuthoring`, `PhysicsBodyAuthoring`, `PhysicsShapeAuthoring`, `PlaceableObjectAuthoring`, `PlantAuthoring`, `SeedAuthoring`, `StateAuthoring`, `TookDamageStateAuthoring`

## Systems (20)

`AchievementSystem`, `BeginSimulationEntityCommandBufferSystem`, `ClientCommSystem`, `DeserializeComponentsSystem`, `DisableBurstForSystem`, `DropLootSystem`, `EquipmentLateUpdateSystem`, `EquipmentUpdateSystem`, `ISystem`, `MapUpdateSystem`, `RpcCommandRequestSystem`, `SelectedEquipmentChangeSystem`, `SerializeWorldSystem`, `ServerCommSystem`, `ServerSystem`, `SummarizeConditionsSystem`, `TileTypeColorLookupSystem`, `UpdateHealthFromBufferSystem`, `WaterSpreadingSystem`, `WorldInfoSystem`

## Converters (authoring → ECS) (5)

`CooldownConverter`, `EntityMonoBehaviourDataConverter`, `LootTableConverter`, `ObjectConverter`, `SingleAuthoringComponentConverter`

## Equipment slot behaviours (12)

`BucketSlot`, `DefaultPlaceSlot`, `EatableSlot`, `EmptySlot`, `EquipmentSlot`, `HoeSlot`, `PaintToolSlot`, `PlaceObjectSlot`, `RoofingToolSlot`, `SeederSlot`, `ShovelSlot`, `WaterCanSlot`

## Managers / handlers / controllers (15)

`AudioManager`, `ClientHandler`, `ConversionManager`, `ECSManager`, `EntityManager`, `LocalizationManager`, `MemoryManager`, `MenuManager`, `MusicManager`, `PlacementHandler`, `PlayerController`, `SceneHandler`, `ServerHandler`, `TextManager`, `UIManager`

## Tables / banks / databases / data blocks (44)

`ActiveColourTable`, `AlchemyTable`, `AutomationTable`, `CartographyTable`, `ColourTable`, `ConditionInfo`, `DistilleryTable`, `ElectronicsTable`, `EndTable`, `EntityAuthoringDataBlock`, `EntityObjectInfo`, `GlobalColourTable`, `GraphicalObjectDataBlock`, `Info`, `InvariantInfo`, `LanguageDataBlock`, `LocalColourTable`, `LogInfo`, `LootInfo`, `LootTable`, `MapWorkshopTilesetBank`, `NeedDatabase`, `NumberFormatInfo`, `ObjectAuthoringToObjectInfo`, `ObjectInfo`, `OnGetObjectInfo`, `PaintersTable`, `ParameterInfo`, `PoolParameterDataBlock`, `PoolablePrefabBank`, `PooledObjectDataBlock`, `PugDatabase`, `PugDatabaseBank`, `ReadColourTable`, `SaveDataBlock`, `StartInfo`, `StartTable`, `Table`, `TextDataBlock`, `TileInfo`, `TilesetDataBlock`, `TilesetLayerDefinitionDataBlock`, `UpdateGraphicsFromObjectInfo`, `WorldInfo`

## Harmony patch targets, i.e. game methods mods hook (75)

Each entry is `Class.Method` (or just `Class`). These show where specific logic lives in the game code.

- `AudioManager.Initialized`
- `AudioManager.IsLegalSfxID`
- `ChatWindow.AddMessageHeight`
- `ChatWindow.AllocPugText`
- `ChatWindow.Awake`
- `ChatWindow.Deactivate`
- `ChatWindow.Update`
- `ColorReplacer.UpdateColorReplacerFromObjectData`
- `ControlMappingMenu.Initialize`
- `ConversionManager.CreateAndEnqueue`
- `ConversionManager.RunConverters`
- `CooldownConverter.Convert`
- `CraftingBuilding.GetCraftingUISettings`
- `ECSManager.Init`
- `EffectEventExtensions.PlayEffect`
- `Emote.OnOccupied`
- `EntityMonoBehaviourDataConverter.Convert`
- `EquipmentUpdateSystem.OnUpdate`
- `HoeSlot.Dig`
- `HoeSlot.UpdateEquipment`
- `InputManager_Base.Start`
- `LootTableConverter.Convert`
- `MapUI.RevealDistance`
- `MapUpdateSystem.UpdateTiles`
- `MemoryManager.Init`
- `MenuManager.Init`
- `MenuManager.IsAnyMenuActive`
- `MenuManager.quantumConsole`
- `MusicManager.Init`
- `MusicManager.SetNewMusicPlaylist`
- `ObjectAuthoring.ObjectAuthoringToObjectInfo`
- `ObjectConverter.Convert`
- `PaintToolSlot.PaintIndexToTileset`
- `PaintToolSlot.UpdateEquipment`
- `PlaceObjectSlot.UpdateEquipment`
- `PlacementHandler.CanPlaceObjectAtPosition`
- `PlacementHandler.CanPlaceObjectAtPositionForSlotType`
- `PlacementHandler.FindPlaceablePositionFromMouseOrJoystick`
- `PlacementHandler.FindPlaceablePositionFromOwnerDirection`
- `PlacementHandler.UpdatePlaceIcon`
- `PlacementHandler.UpdatePlaceablePosition`
- `PlacementHandlerWatering.CanPlaceObjectAtPosition`
- `PlayerController.AE_FootStep`
- `PlayerController.EquipSlot`
- `PlayerController.GetObjectName`
- `PlayerController.GetSlotPoolForObjectType`
- `PlayerController.ReduceDurabilityOfAllEquipment`
- `PlayerController.ReduceDurabilityOfEquipment`
- `PlayerController.ReduceDurabilityOfHeldEquipment`
- `PlayerController.ReducePercentageDurabilityOfAllEquipment`
- `PlayerController.ReducePercentageDurabilityOfEquipment`
- `PlayerController.UpdateEquippedSlotVisuals`
- `PugDatabase.BuildAuthoringListFromEntityDataBlocks`
- `RadicalMenu.TypeToMenu`
- `RoofingToolSlot.ToggleRoof`
- `SceneHandler.Awake`
- `ShovelSlot.Dig`
- `ShovelSlot.UpdateEquipment`
- `SlotUIBase.GetHoverStats`
- `SpriteInstancingModAssetProcessor.Done`
- `SpriteSkinFromEntityAndSeason.UpdateSkin`
- `TilesetTypeUtility.GetAdaptiveTexture`
- `TilesetTypeUtility.GetEditorOverrideMaterial`
- `TilesetTypeUtility.GetFriendlyName`
- `TilesetTypeUtility.GetOverrideMaterial`
- `TilesetTypeUtility.GetOverrideParticles`
- `TilesetTypeUtility.GetTexture`
- `TilesetTypeUtility.GetTileset`
- `TitleScreenAnimator.OpenMenu`
- `UIManager.Init`
- `UIManager.LateUpdate`
- `UIManager.TryHideAllInventoryAndCraftingUI`
- `UIManager.isAnyInventoryShowing`
- `WaterCanSlot.PlaceItem`
- `WaterSpreadingSystem.OnUpdate`
