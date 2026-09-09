# Crash Patterns Reference

Common crash patterns in Unreal Engine projects, organized by category with symptoms, root causes, and fixes.

**Crash artifact locations:**
- Editor crashes: `Saved/Crashes/<CrashGUID>/` — contains `.dmp`, `.log`, `Diagnostics.txt`
- Packaged crashes (Windows): `%LOCALAPPDATA%/<Project>/Saved/Crashes/`
- Packaged crashes (Mac): `~/Library/Logs/<Project>/`
- For minidump analysis: open `.dmp` in Rider or Visual Studio with `.pdb` symbols from `Binaries/`

## Nullptr Dereference Patterns

### GetWorld() Returns Nullptr

**Symptom:** Access violation at or near address 0x00000000 in a constructor or static initializer.

**Cause:** `GetWorld()` is called during CDO construction or before the object is placed in a world.

**Where it happens:**
- `AActor` / `UActorComponent` constructors
- `UObject::PostInitProperties()` before the object is registered
- `UGameInstanceSubsystem::Initialize()` (world may not exist yet)
- Static helper functions called from constructors

**Fix:**
```cpp
// WRONG — crashes in constructor
AMyActor::AMyActor()
{
    UWorld* World = GetWorld(); // nullptr during CDO construction
    World->SpawnActor(...);    // crash
}

// CORRECT — defer to BeginPlay
void AMyActor::BeginPlay()
{
    Super::BeginPlay();
    UWorld* World = GetWorld(); // safe here
    World->SpawnActor(...);
}
```

### Cast<> Returns Nullptr

**Symptom:** Crash on the line after a `Cast<>` call when the result is used without null check.

**Cause:** The source object is not of the expected type, or is nullptr itself.

**Fix:** Always check `Cast<>` results. If the cast MUST succeed, use `CastChecked<>` for a clear assertion instead of a random nullptr crash.

```cpp
// WRONG — silent nullptr if wrong type
AMyCharacter* Char = Cast<AMyCharacter>(OtherActor);
Char->TakeDamage(...); // crash if OtherActor isn't AMyCharacter

// CORRECT — guard the cast
if (AMyCharacter* Char = Cast<AMyCharacter>(OtherActor))
{
    Char->TakeDamage(...);
}

// ALTERNATIVE — crash with clear message in dev builds
AMyCharacter* Char = CastChecked<AMyCharacter>(OtherActor);
```

### FindComponentByClass / GetComponentByClass Returns Nullptr

**Symptom:** Crash when accessing a component that was expected to exist on an actor.

**Cause:**
- The component was never added (Blueprint override removed it, or it's on a different actor class)
- The actor is a CDO and components aren't fully constructed
- The component was destroyed at runtime

**Fix:**
```cpp
// Always null-check component lookups
if (UHealthComponent* Health = FindComponentByClass<UHealthComponent>())
{
    Health->ApplyDamage(Amount);
}
else
{
    UE_LOG(LogTemp, Warning, TEXT("Actor %s missing HealthComponent"), *GetName());
}
```

### GetOwner() / GetInstigator() Returns Nullptr

**Symptom:** Crash in component or projectile code when accessing the owner.

**Cause:**
- Component not attached to any actor yet (during construction)
- Projectile spawned without setting instigator
- Owner actor was destroyed (GC'd) before the owned component/actor accessed it

**Fix:** Null-check, and for projectiles always set instigator at spawn time:
```cpp
FActorSpawnParameters SpawnParams;
SpawnParams.Instigator = GetInstigator();
SpawnParams.Owner = this;
GetWorld()->SpawnActor<AProjectile>(ProjectileClass, Transform, SpawnParams);
```

## Garbage Collection Crashes

### Dangling UObject Pointer

**Symptom:** Crash with access violation at address resembling `0xDDDDDDDD` or `0xFEEEFEEE` (debug fill patterns), or crash inside `UObject::IsValidLowLevel()`, `FGCArrayPool`, or `GUObjectArray`.

**Cause:** A raw `UObject*` pointer that is NOT marked `UPROPERTY()` — the GC doesn't know about it and collects the object.

**Fix:**
```cpp
// WRONG — invisible to GC
class AMyActor : public AActor
{
    UStaticMeshComponent* CachedMesh; // NOT a UPROPERTY — GC will collect it
};

// CORRECT — visible to GC
class AMyActor : public AActor
{
    UPROPERTY()
    UStaticMeshComponent* CachedMesh; // GC knows about this reference
};

// ALTERNATIVE — weak reference (for non-owning references)
TWeakObjectPtr<AActor> TargetActor; // Automatically becomes null when target is GC'd
if (TargetActor.IsValid())
{
    TargetActor->DoSomething();
}
```

### Calling Functions on GC'd Objects

**Symptom:** Intermittent crash in `UObject::ProcessEvent()` or virtual function dispatch. May work 90% of the time.

**Cause:** Object was garbage collected between when you cached the pointer and when you used it. Common with delegates, timers, and async callbacks.

**Fix:**
```cpp
// WRONG — delegate captures raw pointer
SomeDelegate.BindLambda([TargetActor]()
{
    TargetActor->Foo(); // TargetActor may be GC'd by now
});

// CORRECT — capture weak pointer
TWeakObjectPtr<AActor> WeakTarget = TargetActor;
SomeDelegate.BindLambda([WeakTarget]()
{
    if (AActor* Target = WeakTarget.Get())
    {
        Target->Foo();
    }
});
```

### TArray/TMap of Raw UObject Pointers

**Symptom:** Crash when iterating a container of `UObject*` — some entries are now invalid.

**Cause:** Container members are not `UPROPERTY()`, so GC doesn't trace into them.

**Fix:**
```cpp
// WRONG
TArray<UMyObject*> CachedObjects; // GC doesn't trace this

// CORRECT
UPROPERTY()
TArray<UMyObject*> CachedObjects; // GC traces all elements

// ALTERNATIVE for non-UPROPERTY contexts
TArray<TWeakObjectPtr<UMyObject>> CachedObjects;
```

## Stack Overflow

### Recursive Blueprint/C++ Calls

**Symptom:** `EXCEPTION_STACK_OVERFLOW` — immediate crash, often with a very deep callstack repeating the same few functions.

**Cause:**
- Blueprint event graph creates a cycle (EventA calls EventB calls EventA)
- C++ function indirectly calls itself through a chain of virtual overrides
- `OnRep_` function modifies the replicated property, triggering itself again

**Fix:**
- Add recursion guards: `static bool bIsProcessing = false; if (bIsProcessing) return; TGuardValue Guard(bIsProcessing, true);`
- For OnRep cycles: use a `bSuppressOnRep` flag or modify the value without going through the setter
- For Blueprint cycles: check the event graph for loops, use a "processed this frame" flag

### Deep Inheritance or Component Chains

**Symptom:** Stack overflow during construction or `BeginPlay()` with many Super:: calls in the stack.

**Cause:** Excessively deep class hierarchies (10+ levels) where each level adds significant stack usage in overridden functions.

**Fix:** Flatten the hierarchy. Use composition (components) instead of deep inheritance.

## Assertion Failures

### check() / checkf()

**Behavior:** Fatal crash in Development and Debug builds. **Completely removed** in Shipping (including the expression).

**Common assertions and what they mean:**
```
check(IsInGameThread())     — You're calling thread-unsafe code from a background thread
check(IsValid())            — Operating on a pending-kill or invalid object
check(Component != nullptr) — A required component is missing
checkf(Index >= 0 && Index < Num(), ...) — Array out of bounds
```

**Key rule:** NEVER put side-effect code inside `check()`:
```cpp
// WRONG — RemoveItem() is stripped in Shipping, item never removed
check(Inventory.RemoveItem(ItemId));

// CORRECT — separate the operation from the assertion
bool bRemoved = Inventory.RemoveItem(ItemId);
check(bRemoved);
```

### ensure() / ensureMsgf()

**Behavior:** Logs a callstack and continues execution. Reports once per callsite (won't spam). Expression always executes in all build configs.

**Use for:** Conditions that should be true but aren't fatal if violated.

### verify()

**Behavior:** Fatal crash in Development/Debug. Expression still executes in Shipping, but failure is silently ignored.

**Use for:** Operations with side effects that must execute but should assert in dev.

## Blueprint Compilation Crashes

**Symptom:** Editor crashes or hangs when compiling a Blueprint.

**Common causes:**
- Circular Blueprint dependencies (BP_A references BP_B which references BP_A)
- Blueprint referencing a C++ class that was removed or renamed without redirect
- Corrupted Blueprint binary data (manual merge conflicts in .uasset)
- Extremely complex Blueprint graph exceeding compiler limits

**Fix:**
- For circular dependencies: use Interfaces or soft references to break the cycle
- For missing C++ classes: add `CoreRedirects` in `DefaultEngine.ini`
- For corrupted Blueprints: revert to last known good version, recreate manually
- Open the Blueprint with `-NoLoadStartupPackages` to debug load issues

## Slate / UMG Null Widget Access

**Symptom:** Crash inside `SWidget::Paint()`, `SWidget::OnPaint()`, or `FSlateApplication::Tick()`. Often crash in `TSharedPtr` dereference.

**Cause:**
- Widget was removed from the hierarchy but a `TSharedPtr`/`TWeakPtr` reference is still used
- `WidgetTree->ConstructWidget<>()` returned nullptr (wrong outer or class)
- Accessing widget in `NativeConstruct()` before child widgets are created
- Closing a window/tab that still has active timers or async callbacks updating widgets

**Fix:**
```cpp
// Always check widget validity
if (TSharedPtr<SWidget> PinnedWidget = WeakWidget.Pin())
{
    PinnedWidget->SetVisibility(EVisibility::Visible);
}

// For UMG — check IsValid and IsInViewport
if (MyWidget && MyWidget->IsInViewport())
{
    MyWidget->RemoveFromParent();
}
```

## Async Loading Crashes

### Soft Reference Not Loaded

**Symptom:** `TSoftObjectPtr<>::Get()` returns nullptr at runtime even though the asset exists in the editor.

**Cause:** Soft references are not automatically loaded — they must be explicitly resolved via `LoadSynchronous()` or `RequestAsyncLoad()`.

**Fix:**
```cpp
// WRONG — Get() doesn't load, just checks if already in memory
UTexture2D* Tex = SoftTexture.Get(); // nullptr if not loaded

// CORRECT — synchronous load
UTexture2D* Tex = SoftTexture.LoadSynchronous();

// CORRECT — async load
FStreamableManager& Mgr = UAssetManager::GetStreamableManager();
Mgr.RequestAsyncLoad(SoftTexture.ToSoftObjectPath(),
    FStreamableDelegate::CreateUObject(this, &AMyActor::OnTextureLoaded));
```

### Streaming Level Crashes

**Symptom:** Crash when accessing actors in a streaming level that hasn't finished loading.

**Cause:** Code assumes level actors exist immediately after `LoadStreamLevel()`, but loading is async.

**Fix:**
- Use `OnLevelLoaded` delegate or `FLatentActionInfo` completion callback
- Check `ULevelStreaming::IsLevelLoaded()` / `IsLevelVisible()` before accessing actors
- Never cache pointers to actors in streaming levels across load/unload cycles

### Asset Registry Queries During Load

**Symptom:** Crash or empty results when querying `IAssetRegistry` during startup or level load.

**Cause:** Asset registry scanning is asynchronous. Queries before scanning completes return incomplete results.

**Fix:**
```cpp
IAssetRegistry& Registry = FModuleManager::LoadModuleChecked<FAssetRegistryModule>("AssetRegistry").Get();
if (Registry.IsLoadingAssets())
{
    // Defer query — register for completion callback
    Registry.OnFilesLoaded().AddUObject(this, &AMyActor::OnRegistryReady);
}
else
{
    // Safe to query
    PerformAssetQuery();
}
```

## Quick Diagnosis Table

| Crash Address Pattern | Likely Cause |
|----------------------|--------------|
| `0x00000000` (or small offset) | Nullptr dereference |
| `0xDDDDDDDD` | Use-after-free (debug heap fill) |
| `0xFEEEFEEE` | Freed memory access (Windows heap fill) |
| `0xCDCDCDCD` | Uninitialized heap memory |
| `0xCCCCCCCC` | Uninitialized stack memory |
| `0xFDFDFDFD` | Heap buffer overrun (guard bytes) |
| Stack overflow exception | Infinite recursion or extreme stack usage |
| Pure virtual call | Calling virtual function during destruction |

---

## Log Patterns

Common UE output log entries and their root causes. Filter logs with:

```bash
grep -n "Fatal\|Error\|Assertion failed\|ensure(" Saved/Logs/<Project>.log | tail -50
grep -n "Warning" Saved/Logs/<Project>.log | grep -v "LogTemp\|LogSlate" | tail -30
```

| Log pattern | Root cause |
|-------------|-----------|
| `LogScript: Error: Accessed None` | Blueprint variable/reference is null |
| `LogGarbage: Warning: Obj ... is not rooted` | UObject not protected from GC |
| `LogUObjectGlobals: Warning: Failed to find` | Asset path invalid or not cooked |
| `Assertion failed: IsInGameThread()` | Game-thread-only API called from task/thread |
| `check() failed` | Explicit assertion — read the message |
| `ensure() failed` | Soft assertion — non-fatal, but investigate |
| `LogPython: Error:` | Python automation script error |
