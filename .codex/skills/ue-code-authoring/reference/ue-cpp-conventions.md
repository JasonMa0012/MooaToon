# UE5 C++ Conventions

Rules enforced by `get_file_problems` / `lint_files`. Match these before running diagnostics to minimize fix cycles.

---

## Naming

| Prefix | Applies To |
|--------|-----------|
| `A` | `AActor` subclasses |
| `U` | `UObject` / `UActorComponent` subclasses |
| `F` | Structs (`USTRUCT`) |
| `E` | Enums (`UENUM`) |
| `I` | Interfaces (`UINTERFACE`) + their implementation class |
| `T` | Template classes |

Files: drop the prefix → `AMyActor` → `MyActor.h` / `MyActor.cpp`.

---

## Class Skeleton

### Header (`.h`)

```cpp
#pragma once

#include "CoreMinimal.h"
#include "<ParentClass>.h"
#include "MyActor.generated.h"   // ALWAYS last include before class declaration

UCLASS(BlueprintType, Blueprintable)
class MYMODULE_API AMyActor : public AActor
{
    GENERATED_BODY()

public:
    AMyActor();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "MyActor")
    float MyValue = 0.f;

    UFUNCTION(BlueprintCallable, Category = "MyActor")
    void DoThing();

protected:
    virtual void BeginPlay() override;

private:
    UPROPERTY()
    TObjectPtr<USceneComponent> RootSceneComp;
};
```

### Source (`.cpp`)

```cpp
#include "MyActor.h"                                    // ALWAYS first
#include UE_INLINE_GENERATED_CPP_BY_NAME(MyActor)      // UE5: faster compile

AMyActor::AMyActor()
{
    PrimaryActorTick.bCanEverTick = false;

    RootSceneComp = CreateDefaultSubobject<USceneComponent>(TEXT("RootSceneComp"));
    SetRootComponent(RootSceneComp);
}

void AMyActor::BeginPlay()
{
    Super::BeginPlay();
}

void AMyActor::DoThing()
{
}
```

---

## Key Rules

### Reflection macros
- `UPROPERTY` on every member exposed to Blueprint, GC, or editor
- `UFUNCTION` on every callable exposed to Blueprint
- `UCLASS(BlueprintType, Blueprintable)` unless intentionally not exposable
- `GENERATED_BODY()` required inside every `UCLASS`/`USTRUCT`/`UENUM`

### Object pointers
- `TObjectPtr<UFoo>` for `UPROPERTY` references (UE5 convention; Rider warns on raw `UFoo*`)
- `TSoftObjectPtr<UFoo>` for optional/lazy asset references
- `TSoftClassPtr<UFoo>` for class references that should not hard-load on include
- Never `new` / `delete` UObjects

### Include order
1. Own generated header (`.h` files): `"<ClassName>.generated.h"` — **last**
2. Own header (`.cpp` files): `"<ClassName>.h"` — **first**
3. Then Engine/plugin headers, then project headers
4. Forward-declare in headers; include in `.cpp`

### API macro
Every class that crosses module boundaries needs `<MODULE>_API`:
```cpp
class MYMODULE_API AMyActor : public AActor
```
Missing this = linker error ("unresolved external symbol") when another module uses the class.

### Visuals belong in Blueprints
- DO declare component pointers: `TObjectPtr<UStaticMeshComponent> MeshComp`
- DO `CreateDefaultSubobject` in the constructor
- DO NOT assign meshes/materials/particles in C++ (`ConstructorHelpers::FObjectFinder` for assets)
- DO NOT use `FObjectFinder` unless the user explicitly requested it

### Replication (multiplayer)
- Add `DOREPLIFETIME(AMyActor, MyValue)` in `GetLifetimeReplicatedProps` for every `UPROPERTY(Replicated)`
- Authority guards: `if (!HasAuthority()) return;` before server-only logic
- Server RPCs: declare `UFUNCTION(Server, Reliable)` + implement `_Implementation` + add `_Validate`

### Thread safety
- Never access UObjects outside the game thread
- Wrap cross-thread access: `AsyncTask(ENamedThreads::GameThread, [this](){ ... })`

---

## Module Dependencies (`Build.cs`)

Add only what the file actually includes. Rider's `get_file_problems` will flag missing module deps.

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "Core", "CoreUObject", "Engine",
    // add as needed:
    "InputCore", "EnhancedInput",
    "UMG", "Slate", "SlateCore",
    "GameplayAbilities", "GameplayTags", "GameplayTasks",
    "AIModule", "NavigationSystem",
    "Niagara", "PhysicsCore",
    "NetCore",
});
```

---

## BuildSettingsVersion by Engine Version

When creating new `Target.cs` files, match these versions to the project's `EngineAssociation`:

| UE Version | `BuildSettingsVersion` | `IncludeOrderVersion` |
|------------|----------------------|----------------------|
| 5.5 | `V5` | `Unreal5_5` |
| 5.6 | `V5` | `Unreal5_6` |
| 5.7+ | `V6` | `Unreal5_7` |

Wrong versions → build failure. Read `.uproject` `EngineAssociation` first.

---

## Generated Header Errors — Common Causes

| Error | Cause | Fix |
|-------|-------|-----|
| `Cannot find generated.h` | File name doesn't match class name | Rename file to match class (e.g. `AMyActor` → `MyActor.h`) |
| `GENERATED_BODY() not in class` | Missing macro | Add inside class body |
| `BlueprintReadWrite on private` | UHT restriction | Move to `public` or change to `BlueprintReadOnly` |
| `Unresolved external symbol` | Missing `_API` or `Build.cs` dep | Add `<MODULE>_API` / add dep to `Build.cs` |

---

## File Placement

| Type | Header | Source |
|------|--------|--------|
| Actor | `Source/<Module>/Public/<Name>.h` | `Source/<Module>/Private/<Name>.cpp` |
| Component | `Source/<Module>/Public/Components/<Name>.h` | `Source/<Module>/Private/Components/<Name>.cpp` |
| Subsystem | `Source/<Module>/Public/Subsystems/<Name>.h` | `Source/<Module>/Private/Subsystems/<Name>.cpp` |
| Interface | `Source/<Module>/Public/<Name>.h` | `Source/<Module>/Private/<Name>.cpp` |
| Function Library | `Source/<Module>/Public/<Name>.h` | `Source/<Module>/Private/<Name>.cpp` |
| Plugin Module | `Plugins/<Plugin>/Source/<Module>/Public/` | `Plugins/<Plugin>/Source/<Module>/Private/` |

If the project uses a flat structure (`Source/Module/*.h` and `*.cpp` together), follow that instead. Check with `list_directory_tree` first.
