# UE Test Patterns — Framework Reference

## Framework Selection

Pick the minimal framework that covers the testing need. Over-engineering leads to slow, fragile tests.

| Need | Framework |
|------|-----------|
| Pure C++ logic, no UObject | **LowLevelTestsRunner** (Catch2 — fastest startup) |
| Chaos physics (collision, constraints) | **ChaosTestHarness** |
| C++ class/subsystem with shared setup & teardown | **CQTest** `TEST_CLASS` |
| Simple one-off C++ assertion | `IMPLEMENT_SIMPLE_AUTOMATION_TEST` or CQTest `TEST` |
| BDD-style grouped behaviors | Automation `DEFINE_SPEC` |
| Multi-frame async sequences in C++ | **CQTest** `TestCommandBuilder` |
| Server + client replication in PIE | **CQTest** `PIENetworkComponent` |
| Actor behavior in a real level | **Functional Tests** (`AFunctionalTest` in a test map) |
| Full game startup, stability, or performance CI | **Gauntlet** |

---

Ready-to-use patterns for each UE testing framework. Each section includes the minimal correct boilerplate, the Rider steps to validate it, and common pitfalls specific to that framework.

---

## Automation Framework — `IMPLEMENT_SIMPLE_AUTOMATION_TEST`

Use for: one-off C++ assertions, quick regression tests, no shared setup needed.

### Boilerplate

```cpp
#include "CoreMinimal.h"
#include "Misc/AutomationTest.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FMyFeatureTest,                          // C++ class name
    "MyProject.MyFeature.BasicBehavior",     // test registry path (dots = hierarchy)
    EAutomationTestFlags::EditorContext |    // must include EditorContext for editor runs
    EAutomationTestFlags::ProductFilter      // must include a product or engine filter
)

bool FMyFeatureTest::RunTest(const FString& Parameters)
{
    // Arrange
    int32 Result = MyFunctionUnderTest(42);

    // Assert
    TestEqual(TEXT("Expected result"), Result, 84);

    return true; // MUST return true on success, false on failure
}
```

**Rider validation after writing:** run `get_file_problems` on the file.  
Rider will flag: wrong return type on `RunTest`, missing `AutomationTest.h`, invalid flags combination.

### Common pitfalls
- Returning `false` from `RunTest` always marks failure — even if all assertions passed
- Using `ApplicationContext` when running from the editor → test invisible in Session Frontend
- Registering in a `Runtime` module → test never appears

---

## Automation Framework — `DEFINE_SPEC` (BDD-style)

Use for: grouped behaviors with shared describe/context blocks.

```cpp
#include "CoreMinimal.h"
#include "Misc/AutomationTest.h"

BEGIN_DEFINE_SPEC(
    FMyFeatureSpec,
    "MyProject.MyFeature",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter
)
    // shared state as member fields
    int32 SharedValue = 0;
END_DEFINE_SPEC(FMyFeatureSpec)

void FMyFeatureSpec::Define()
{
    Describe("When input is positive", [this]()
    {
        BeforeEach([this]()
        {
            SharedValue = 10;
        });

        It("should double the value", [this]()
        {
            int32 Result = MyFunctionUnderTest(SharedValue);
            TestEqual(TEXT("doubled"), Result, 20);
        });
    });
}
```

**Rider validation:** run `get_file_problems` on the file.

### Common pitfalls
- `BeforeEach` lambda captures `this` but `SharedValue` is reset per-spec — don't capture by value
- Async work inside `It` blocks requires latent commands (see latent section below)

---

## CQTest — `TEST_CLASS` and `TEST_METHOD`

Use for: C++ classes/subsystems needing shared setup/teardown with auto state reset.

In UE5.5+, `CQTest` is a built-in Engine module. Add `"CQTest"` to `PrivateDependencyModuleNames` — **do not add a CQTest plugin**.

```cpp
#include "CoreMinimal.h"
#include "CQTest.h"

TEST_CLASS(FMySubsystemTests, "MyProject.MySubsystem")
{
    // Shared state — reset automatically between test methods
    UMySubsystem* Subsystem = nullptr;

    BEFORE_EACH()
    {
        Subsystem = GEngine->GetEngineSubsystem<UMySubsystem>();
        ASSERT_THAT(IsNotNull(Subsystem));
    }

    TEST_METHOD(ProcessItem_WithValidInput_ReturnsTrue)
    {
        bool Result = Subsystem->ProcessItem(TEXT("ValidInput"));
        ASSERT_THAT(IsTrue(Result));
    }

    TEST_METHOD(ProcessItem_WithEmptyInput_ReturnsFalse)
    {
        bool Result = Subsystem->ProcessItem(TEXT(""));
        ASSERT_THAT(IsFalse(Result));
    }
};
```

**Rider validation after writing:** run `get_file_problems` on the file. Use `get_symbol_info` to confirm the subsystem's API contract before writing assertions.

### Common pitfalls
- `ASSERT_THAT` inside a `.Do(lambda)` only exits the lambda — the command sequence continues; check `HasAnyErrors()` if subsequent commands must stop
- Cannot add latent commands from inside an executing latent command — queue all commands upfront in `BEFORE_EACH` or `TEST_METHOD`
- `MapTestSpawner` requires `AddWaitUntilLoadedCommand` in `BEFORE_EACH`, not the constructor

---

## CQTest — Async Sequences with `TestCommandBuilder`

Use for: multi-frame sequences, timer-based behaviors, or anything that requires multiple ticks.

```cpp
TEST_CLASS(FMyAsyncTests, "MyProject.AsyncBehavior")
{
    TSharedPtr<FTestCommandBuilder> Builder;

    BEFORE_EACH()
    {
        Builder = MakeShared<FTestCommandBuilder>(this);
    }

    TEST_METHOD(TimerFires_AfterDelay)
    {
        bool bFired = false;

        Builder->Do([this, &bFired]()
        {
            // Trigger the timer
            GetTestActor()->StartTimer(0.1f, [&bFired](){ bFired = true; });
        })
        .Until([&bFired](){ return bFired; })   // wait until condition is true
        .Do([&bFired]()
        {
            // Assert after the timer fired
        });

        AddCommand(Builder->Build());
    }
};
```

### Common pitfalls
- Never assert immediately after `Do` that queues async work — use `.Until()` or `FDoneDelegate`
- `.Until()` has a default timeout — long operations may need an explicit `TimeoutSeconds`

---

## CQTest — Network Tests with `PIENetworkComponent`

Use for: verifying replication, RPCs, authority checks in PIE.

```cpp
TEST_CLASS(FMyNetworkTests, "MyProject.Network")
{
    FPIENetworkComponent Network;

    BEFORE_EACH()
    {
        Network.StartPIE(2); // 1 server + 1 client
        AddCommand(Network.WaitForConnected());
    }

    AFTER_EACH()
    {
        Network.StopPIE();
    }

    TEST_METHOD(ServerRPC_ReplicatesToClient)
    {
        AddCommand(Network.OnServer([this]()
        {
            Network.GetServerActor<AMyActor>()->ServerRPC();
        }));
        AddCommand(Network.OnClient(0, [this]()
        {
            ASSERT_THAT(IsTrue(Network.GetClientActor<AMyActor>(0)->bWasNotified));
        }));
    }
};
```

---

## Functional Tests — `AFunctionalTest`

Use for: in-world actor behavior, gameplay sequences, screenshot comparison.

**Two-file requirement:** a C++ class AND a test map with the actor placed.

```cpp
// MyFunctionalTest.h
#pragma once
#include "FunctionalTest.h"
#include "MyFunctionalTest.generated.h"

UCLASS()
class MYGAMETESTS_API AMyFunctionalTest : public AFunctionalTest
{
    GENERATED_BODY()

public:
    virtual void StartTest() override;
};
```

```cpp
// MyFunctionalTest.cpp
#include "MyFunctionalTest.h"

void AMyFunctionalTest::StartTest()
{
    // Perform gameplay sequence
    // Call FinishTest(EFunctionalTestResult::Succeeded, TEXT("")) when done
    // or FinishTest(EFunctionalTestResult::Failed, TEXT("reason"))

    // Example: check an actor exists in the level
    AActor* TargetActor = FindActorByTag(TEXT("Target"));
    if (!TargetActor)
    {
        FinishTest(EFunctionalTestResult::Failed, TEXT("Target actor not found"));
        return;
    }

    FinishTest(EFunctionalTestResult::Succeeded, TEXT(""));
}
```

**After writing:** use `get_symbol_info` to confirm the API contract, then run `get_file_problems` on the file.

### Common pitfalls
- Functional test class without a test map = test never executes
- `FinishTest` not called on every code path = test times out
- Using `GetWorld()` without verifying it is non-null (it is valid in functional tests, but guard it)

---

## LowLevel Tests — Catch2 (no editor startup)

Use for: pure C++ logic with no UObject dependency. Fastest possible startup.

```cpp
// MyMathTests.cpp
#include "TestHarness.h"   // LowLevelTestsRunner header

TEST_CASE("MyMath - Clamp returns min when below range", "[MyMath]")
{
    int32 Result = FMath::Clamp(-5, 0, 10);
    REQUIRE(Result == 0);
}

TEST_CASE("MyMath - Clamp returns max when above range", "[MyMath]")
{
    int32 Result = FMath::Clamp(15, 0, 10);
    REQUIRE(Result == 10);
}
```

**Build.cs for LowLevel test module:**
```csharp
public class MyMathTests : TestModuleRules
{
    public MyMathTests(ReadOnlyTargetRules Target) : base(Target)
    {
        PrivateDependencyModuleNames.Add("MyMath");
    }
}
```

**Rider validation:** run `get_file_problems` on the file.

### Common pitfalls
- Inheriting from `TestModuleRules`, not `ModuleRules` (LowLevel tests have a different base)
- Trying to use UObject types — LowLevel tests don't initialize the UObject system

---

## Latent Command Patterns (Automation Framework)

For async work in non-CQTest tests:

```cpp
// Define a latent command class
DEFINE_LATENT_AUTOMATION_COMMAND_ONE_PARAMETER(FWaitForCondition, TFunction<bool()>, Condition);

bool FWaitForCondition::Update()
{
    return Condition(); // return true when done, false to keep waiting
}

// Use in RunTest:
bool FMyAsyncTest::RunTest(const FString& Parameters)
{
    bool bDone = false;
    TriggerAsyncOperation([&bDone](){ bDone = true; });

    ADD_LATENT_AUTOMATION_COMMAND(FWaitForCondition([&bDone](){ return bDone; }));

    // Add assertion AFTER the latent command — it runs after bDone is true
    ADD_LATENT_AUTOMATION_COMMAND(FFunctionLatentCommand([this, &bDone]() -> bool
    {
        TestTrue(TEXT("Operation completed"), bDone);
        return true;
    }));

    return true; // RunTest itself just queues commands and returns
}
```

---

## Using Rider to Understand the Code Under Test

Before writing test assertions, verify the actual API:

1. Use `search_symbol` to find where the class is declared
2. Read the header using the standard Read tool to understand the public interface
3. Use `get_symbol_info` to check if a method can return null or has preconditions
4. Use `analyze_calls` to trace what the method calls and what state it needs

This prevents writing tests that assert on behavior the code never had, or that call methods requiring state the test never sets up.

---

## New Test Module Setup

When creating a test module from scratch:

### 1. Create `<FeatureName>Tests.Build.cs`

```csharp
public class MyFeatureTests : ModuleRules
{
    public MyFeatureTests(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
        PrivateDependencyModuleNames.AddRange(new string[]
        {
            "Core",
            "CoreUObject",
            "Engine",
            "MyFeature",         // module under test
            "UnrealEd",          // for editor automation utilities
            "AutomationUtils",   // for FAutomationTestBase helpers
            // "CQTest",         // UE5.5+ only — built-in, not a plugin
            // "FunctionalTesting", // if using AFunctionalTest
        });
    }
}
```

### 2. Add the module to `.uproject` or `.uplugin`

```json
{
    "Name": "MyFeatureTests",
    "Type": "Editor",
    "LoadingPhase": "Default"
}
```

### 3. Create the module stub

```cpp
// MyFeatureTests.cpp
#include "Modules/ModuleManager.h"
IMPLEMENT_MODULE(FDefaultModuleImpl, MyFeatureTests);
```

### 4. Verify registration after building

Run `get_project_problems` after a successful build.

---

## Critical Pitfalls

1. **Test class must be in `Type = Editor` or `Type = Test` module** — `Runtime` modules are never scanned.

2. **Wrong `EAutomationTestFlags` = test never appears** — always include `EditorContext` for editor-run tests and a product filter (`ProductFilter` or `EngineFilter`).

3. **`RunTest` must return `true` on success** — returning `false` early marks failure even before assertions run.

4. **Latent commands don't block** — `ADD_LATENT_AUTOMATION_COMMAND` queues for next tick; assert after `FDoneDelegate`, not immediately after queuing.

5. **`GetWorld()` returns null in bare tests** — use `AutomationOpenMap`, `UWorld::CreateWorld`, or `FAutomationEditorCommonUtils::CreateNewMap()`.

6. **Asset paths must use `/Game/` prefix** — relative paths work in-editor but break at cook time.

7. **CQTest `ASSERT_THAT` inside a lambda only exits the lambda** — the test continues; check `HasAnyErrors()` if subsequent commands must stop.

8. **CQTest: cannot add latent commands from within an executing latent command** — queue all commands upfront in `BEFORE_EACH` or `TEST_METHOD`.

9. **CQTest `MapTestSpawner` requires `AddWaitUntilLoadedCommand` in `BEFORE_EACH`**, not the constructor — calling in the constructor silently does nothing.

10. **CQTest is a built-in Engine module in UE5.5+** — adding it as a plugin causes duplicate symbol errors. Just add `"CQTest"` to `PrivateDependencyModuleNames`.
