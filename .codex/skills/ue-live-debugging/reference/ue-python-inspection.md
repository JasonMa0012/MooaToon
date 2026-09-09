# UE Python Inspection — Runtime State Queries

Reference for inspecting live game state via `execute_tool` + `ue_execute_python`. All patterns are valid single-liners (use `;` not `\n`).

---

## Single-Line Rules

| Do | Don't |
|----|-------|
| Separate statements with `;` | Use `\n` or backslash-newline |
| `[x for x in items]` | `for x in items: ...` (multi-line) |
| `{k: f(k) for k in keys}` | `for k in keys: d[k] = f(k)` |
| `x if cond else y` | `if cond: ...` blocks |
| `next((x for x in lst if pred(x)), None)` | `for` + `break` |

Multi-statement example:
```
import unreal; w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world(); pc=unreal.GameplayStatics.get_player_controller(w,0); p=pc.get_controlled_pawn(); print(p.get_class().get_name())
```

---

## World and Player Access

```python
# Game world (PIE must be running)
w = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()

# Player controller (index 0 = first local player)
pc = unreal.GameplayStatics.get_player_controller(w, 0)

# Player state
ps = pc.player_state

# Controlled pawn
p = pc.get_controlled_pawn()
```

One-liner to confirm PIE is active and player exists:
```
import unreal; w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world(); pc=unreal.GameplayStatics.get_player_controller(w,0) if w else None; print('world:', w.get_name() if w else None, 'pc:', pc.get_class().get_name() if pc else None)
```

---

## Component Queries

```python
# Get a component by class (positional class argument)
asc  = ps.get_component_by_class(unreal.AbilitySystemComponent)
eq   = p.get_component_by_class(unreal.LyraEquipmentManagerComponent)
inv  = ps.get_component_by_class(unreal.LyraInventoryManagerComponent)

# All components of a class from an actor
instances = eq.get_equipment_instances_of_type(unreal.LyraEquipmentInstance)
```

---

## GAS — Ability System Component

```python
# ASC lives on PlayerState in Lyra
asc = ps.get_component_by_class(unreal.AbilitySystemComponent)

# Granted abilities (list of FGameplayAbilitySpec)
specs = asc.get_activatable_abilities()
print([s.ability.get_class().get_name() for s in specs])

# Active gameplay tags on the ASC
tags = asc.get_owned_gameplay_tags()

# Tag count on the ASC (for tag stacks)
n = asc.get_gameplay_tag_count(unreal.GameplayTag("Lyra.ShooterGame.Weapon.MagazineAmmo"))
```

### GameplayTag Construction

**Always positional — keyword `tag_name=` throws TypeError.**

```python
# CORRECT
tag = unreal.GameplayTag("Lyra.ShooterGame.Weapon.MagazineAmmo")

# WRONG — TypeError
tag = unreal.GameplayTag(tag_name="Lyra.ShooterGame.Weapon.MagazineAmmo")
```

### Stat Tag Stacks (weapon ammo, etc.)

Stat tag stacks live on the instigator (`LyraInventoryItemInstance`), not on the ASC directly.

```python
# Get weapon instigator and query ammo stats
import unreal; w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world(); pc=unreal.GameplayStatics.get_player_controller(w,0); p=pc.get_controlled_pawn(); eq=p.get_component_by_class(unreal.LyraEquipmentManagerComponent); wpn=eq.get_equipment_instances_of_type(unreal.LyraEquipmentInstance)[0]; inst=wpn.get_instigator(); print({t: inst.get_stat_tag_stack_count(unreal.GameplayTag(t)) for t in ['Lyra.ShooterGame.Weapon.MagazineAmmo','Lyra.ShooterGame.Weapon.MagazineSize','Lyra.ShooterGame.Weapon.SpareAmmo']})
```

---

## Inventory

```python
# Inventory items on PlayerState
inv = ps.get_component_by_class(unreal.LyraInventoryManagerComponent)
items = inv.get_all_items()
print([(i.get_class().get_name(), i.get_instigator_tag().tag_name) for i in items])
```

---

## Actors in World

```python
# All actors of a class
actors = unreal.GameplayStatics.get_all_actors_of_class(w, unreal.LyraCharacter)
print([a.get_name() for a in actors])

# Actor at a location
hit = unreal.SystemLibrary.line_trace_single(w, start, end, ...)
```

---

## Debug Output

```python
# Print to Output Log (visible in editor)
unreal.log("my message")
unreal.log_warning("warning")
unreal.log_error("error")

# Or just print() — captured in execute_tool output field
print("value:", value)
```

---

## Common Failure Modes

| Error | Cause | Fix |
|-------|-------|-----|
| `SyntaxError: unexpected character after line continuation` | `\n` in script string | Replace with `;` and comprehensions |
| `TypeError: call() 'tag_name' is an invalid keyword argument` | `unreal.GameplayTag(tag_name=...)` | Use positional: `unreal.GameplayTag("...")` |
| `AttributeError: 'NoneType' object has no attribute ...` | PIE not running or player not spawned | Start PIE first; check `w` and `pc` are not `None` |
| `IndexError: list index out of range` | Equipment list is empty | Verify weapon is equipped before querying index `[0]` |
| `TypeError: ... is not a Subclass of ...` | Wrong class passed to `get_component_by_class` | Use the exact `unreal.ClassName`, not a string |
