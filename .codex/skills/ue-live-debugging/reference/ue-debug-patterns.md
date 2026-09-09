# UE Debugging Patterns

Root cause → fix mappings and breakpoint strategies for common Unreal Engine bugs. Use Rider MCP tools alongside these patterns to locate and verify each issue.

---

## Nullptr Lifecycle Bugs

### Pattern: Pointer Valid at Assign, Null at Use

**Symptom:** Object was non-null when cached, crashes later. Classic GC or ownership issue.

**Rider investigation:**
```
1. get_symbol_info on the pointer's type — is it a UObject? Does the type have UPROPERTY()?
2. search_text for the member variable name without "UPROPERTY" on the same line
3. analyze_calls direction="callers" on the function that assigns the pointer — who sets it?
4. analyze_calls direction="callers" on the function that uses the pointer — does any caller destroy the owner?
```

**Breakpoint strategy:**
- Break on the **assignment** (not the dereference) — confirm the pointer is valid at assign
- Use a conditional breakpoint on the use site: condition = `MyPtr == nullptr`
- In Rider: right-click gutter → Edit Breakpoint → Condition: `MyPtr == nullptr`

**Fix:** Mark member with `UPROPERTY()`, or switch to `TWeakObjectPtr<T>` with an `IsValid()` guard.

---

### Pattern: GetWorld() Returns Nullptr

**Symptom:** `GetWorld()` returns nullptr; usually an access violation when the result is used.

**Rider investigation:**
```
1. get_file_problems on the file — Rider often warns about this
2. analyze_calls direction="callers" on the constructor — is anything calling it during CDO creation?
3. search_text for "GetWorld()" in the file — find ALL call sites, not just the crashing one
```

**Breakpoint strategy:** Set breakpoint at the constructor entry. Check call stack in Rider — if `CDO` appears in the stack, this is the CDO construction path.

**Fix:** Move `GetWorld()` calls to `BeginPlay()`, `InitializeComponent()`, or `PostInitializeComponents()`.

---

## GC-Related Crashes

### Pattern: Object Collected While Referenced

**Symptom:** Crash with address pattern `0xDDDDDDDD` (debug-fill freed memory), or inside `FGCArrayPool` / `GUObjectArray`.

**Rider investigation:**
```
1. search_text for the struct/class name without "UPROPERTY" — find untracked raw pointers
2. search_text for "TArray<U" — TArrays of UObject* must also be UPROPERTY
3. get_file_problems on the owning class — Rider sometimes flags untracked UObject members
4. analyze_calls direction="callers" on the function that stores the pointer — does any caller destroy the source?
```

**Breakpoint strategy:**
- Override `BeginDestroy()` on the suspect class and add a breakpoint there
- In the debugger, check the callstack when `BeginDestroy` fires — the call origin reveals what triggered collection

**Fix:** Add `UPROPERTY()` to the member, or convert to `TWeakObjectPtr<T>`.

---

### Pattern: Lambda Capturing Raw UObject Pointer

**Symptom:** Intermittent crash inside a timer, delegate, or async callback.

**Rider investigation:**
```
1. search_text for "BindLambda" and "AddLambda" in suspect files
2. get_file_problems — Rider may flag captured raw pointers
3. analyze_calls direction="callers" on the lambda's host function — can the captured object be destroyed before the callback fires?
```

**Breakpoint strategy:** Break at the lambda capture site. In Rider's debugger, add a watch on the captured pointer — then let the code run and check the watch when the crash occurs.

**Fix:**
```cpp
// WRONG
SomeDelegate.BindLambda([this]() { this->Foo(); });  // "this" may be GC'd

// CORRECT
TWeakObjectPtr<UMyClass> WeakThis(this);
SomeDelegate.BindLambda([WeakThis]()
{
    if (UMyClass* Self = WeakThis.Get())
    {
        Self->Foo();
    }
});
```

---

## Timer and Async Callback Bugs

### Pattern: Timer Fires After Owner Is Destroyed

**Symptom:** Crash in a timer callback — the bound object no longer exists.

**Rider investigation:**
```
1. search_text for "SetTimer" in the suspect class
2. analyze_calls direction="callers" on EndPlay — verify it calls ClearAllTimersForObject
3. get_file_problems on the .cpp — look for missing EndPlay override warnings
```

**Breakpoint strategy:** Break at `EndPlay` entry. Check whether the timer handle is cleared. If `EndPlay` is never reached before the crash, the object is being destroyed by a path that bypasses `EndPlay` (direct deletion instead of `Destroy()`).

**Fix:**
```cpp
void AMyActor::EndPlay(EEndPlayReason::Type Reason)
{
    Super::EndPlay(Reason);
    GetWorldTimerManager().ClearAllTimersForObject(this);
}
```

---

## Threading Bugs

### Pattern: Game-Thread-Only API Called from Background Thread

**Symptom:** Assertion `IsInGameThread()` fails, or crash inside `FSlateApplication` / `UWorld` from a thread-pool job.

**Rider investigation:**
```
1. analyze_calls direction="callers" on the crashing function — find the caller chain
2. get_symbol_info on each caller — look for FRunnable, AsyncTask, FQueuedThreadPool, TaskGraph
3. search_text for "Async(" and "AsyncTask(" near the suspect code
```

**Breakpoint strategy:** In Rider, add a conditional breakpoint with condition `!IsInGameThread()` at the entry of the suspect function. When it breaks, the call stack shows the thread origin.

**Fix:**
```cpp
// Dispatch back to game thread for UObject access
AsyncTask(ENamedThreads::GameThread, [WeakThis]()
{
    if (UMyClass* Self = WeakThis.Get())
    {
        Self->UpdateUI();  // safe on game thread
    }
});
```

---

## Blueprint / C++ Interface Bugs

### Pattern: UFUNCTION Not Accessible from Blueprint

**Symptom:** Blueprint can't find a C++ function, or calling it has no effect.

**Rider investigation:**
```
1. get_symbol_info on the function — check if BlueprintCallable/BlueprintImplementableEvent is present
2. get_file_problems on the header — UFUNCTION macro errors often surface here
3. search_text for the function name with "BlueprintCallable" to find similar working examples in the project
```

**Fix:** Ensure correct specifiers:
```cpp
UFUNCTION(BlueprintCallable, Category="MyCategory")
void MyFunction();         // callable from Blueprint

UFUNCTION(BlueprintImplementableEvent, Category="MyCategory")
void OnMyEvent();          // Blueprint must implement; no C++ body

UFUNCTION(BlueprintNativeEvent, Category="MyCategory")
void OnMyEvent();          // Blueprint CAN override; C++ provides default via _Implementation
```

---

## Hot Reload / Live Coding Corruption

### Pattern: Blueprint Pins Disconnected After C++ Change

**Symptom:** After Live Coding or hot reload, Blueprint graphs show disconnected pins or "accessed none" on valid references.

**Rider investigation:**
```
1. analyze_calls direction="callers" on the changed function — find all Blueprint call sites
2. search_symbol for the changed class — check if any Blueprint subclasses exist
```

**This is not a code bug** — it's an editor state issue. No code fix needed. The fix is always:
1. Close the editor
2. Delete `Intermediate/` and `Binaries/` (NOT Content or Source)
3. Rebuild from Rider: `build_solution_start(rebuild: false)` — incremental is enough
4. Reopen the editor — Blueprint pins restore from the saved graph on a clean reload

**Rider breakpoint strategy for structural changes:** None needed. This is deterministic — structural C++ changes + hot reload = corrupted editor state 100% of the time. Advise the user to restart.

---

## Call Hierarchy Analysis — What to Look For

When reading `analyze_calls` results, focus on:
- Callers that pass nullptr, uninitialized data, or wrong object types
- Callees that return `void`/`bool` but the result is unchecked
- Unexpected call depth — functions reached through many indirections are harder to guard
- Cross-thread callers (class names like `FRunnable`, `AsyncTask`, `FQueuedThreadPool`)

---

## Instrumentation Rules

When adding temporary `UE_LOG`/`ensure` to locate a bug:
- Log the values that matter, not just presence — use `%p` for pointers, actual enum values, not "entered function"
- Use `ensure(expr)` to log + continue rather than `check(expr)` which crashes in dev builds
- Instrument both the caller and the callee when the handoff is suspect
- Remove all instrumentation after the bug is confirmed; do not leave debug logs in source

---

## Fix: Root Cause vs Symptom

Common pitfalls when applying a fix:
- Adding a null check where the pointer should never be null = masking a bug, not fixing it
- Moving code to `BeginPlay` without understanding why it was in the constructor
- Adding `UPROPERTY()` without understanding the ownership model

See individual patterns above for the correct root-cause fix for each category.

---

## Breakpoint Placement Strategies

### "Break at the origin, not the crash"

The crash site is a symptom. The useful breakpoint is at the last point of **known-good state** before the bad state is introduced.

| Crash Location | Useful Breakpoint |
|---------------|-------------------|
| Dereference of ptr | Assignment of ptr (find with `analyze_calls callers`) |
| GC-collected object access | `BeginDestroy()` of the object's class |
| Timer callback crash | Timer setup call site (`SetTimer`) |
| Wrong value used | The function that produced the wrong value |
| "accessed none" in Blueprint | The C++ function that provides the value to Blueprint |

### Conditional Breakpoints for Intermittent Bugs

Always use conditions for intermittent crashes — unconditional breaks on frequently-called functions halt the editor on every call.

Examples:
```
MyPtr == nullptr                          // break only when nullptr
Health <= 0.0f && !bIsDead               // break on unexpected state combination
ActorCount > ExpectedMax                 // break on count anomaly
FString(TEXT("MyLevel")) == CurrentLevel // break only in specific level
```

In Rider: right-click the breakpoint gutter icon → "Edit Breakpoint" → enter condition.

### Log-Point (Non-Breaking Breakpoint)

For cases where stopping execution changes the bug behavior (Heisenbugs):
- In Rider: Edit Breakpoint → uncheck "Suspend" → check "Log message"
- Message template: `"[LiveDebug] {MyPtr} Health={Health} Frame={GFrameCounter}"`
- Output appears in the Debug Console without pausing execution

---

## Instrumentation Recipes

### Minimal Null Guard with Logging

```cpp
if (!ensure(MyPtr != nullptr))
{
    UE_LOG(LogTemp, Error, TEXT("[%s] MyPtr is null in %s"), *GetName(), ANSI_TO_TCHAR(__FUNCTION__));
    return;
}
```

Use `ensure` not `check` — `ensure` logs and continues; `check` crashes in Development.

### Object Validity Check

```cpp
if (!IsValid(MyActor))
{
    UE_LOG(LogTemp, Warning, TEXT("[%s] MyActor invalid (IsPendingKill=%d IsUnreachable=%d)"),
        *GetName(),
        MyActor ? (int32)MyActor->IsPendingKillPending() : -1,
        MyActor ? (int32)MyActor->IsUnreachable() : -1);
    return;
}
```

### Thread Assertion

```cpp
check(IsInGameThread());  // crashes in dev if called from wrong thread — intentional
// OR
if (!ensureAlwaysMsgf(IsInGameThread(), TEXT("[%s] Called from non-game thread"), *GetName()))
{
    return;
}
```

### Timer State Dump

```cpp
// Verify timer is active before relying on it
FTimerManager& TM = GetWorldTimerManager();
UE_LOG(LogTemp, Log, TEXT("[%s] TimerHandle active=%d remaining=%.2f"),
    *GetName(),
    (int32)TM.IsTimerActive(MyTimerHandle),
    TM.GetTimerRemaining(MyTimerHandle));
```
