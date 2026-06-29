---
name: unreal cpp developer
description: Instructions and architectural standards for Unreal Engine 5 C++ development
---

# Unreal Engine 5 C++ Modern Development

This skill defines strict development standards for Unreal Engine 5 C++ code.
The goal is to enforce high-quality, performant Unreal Engine code that follows official recommendations.

## When to Use

Use this skill when:
- Writing C++ code for Unreal Engine 5.x
- Developing gameplay systems
- Writing Actors, Components, or Subsystems
- Exposing APIs to Blueprint
- Optimizing performance
- Building reusable engine systems

Do NOT use when:
- Working with Blueprint-only logic
- Writing non-Unreal code
- Working in other engines

---

# Custom Project Rules

Before generating or modifying any code, you **MUST** first check for project-specific rules in `custom_rules.md` within this skill directory.
If `custom_rules.md` exists, its rules override and take priority over any rule in this file.

---

# Class Templates

When asked to generate a **NEW** C++ class from scratch, you **must** use the provided templates as your starting point:
- Header Template: `templates/TemplateClass.h`
- Source Template: `templates/TemplateClass.cpp`

**Never** invent a new class structure if templates are provided. Always start from the templates.
Substitute `TEMPLATE_CLASS_NAME` and `YOURMODULE_API` with the appropriate names.

---

# Core Philosophy

## C++ First Architecture

Core gameplay logic should be implemented in C++ whenever possible.

Blueprints should mainly be used for:
- configuration and asset references
- UI layout and animation (UMG)
- simple event wiring and visual effects

**Avoid implementing complex state machines, heavy math, or core gameplay loops purely in Blueprints.**

---

# Modern Unreal Code Structure

## Include What You Use (IWYU) & Headers

Always follow the IWYU principle to optimize compile times.
- Never include unnecessary headers.
- Use forward declarations for classes and structs in headers whenever possible.

```cpp
#pragma once
#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "MyComponent.generated.h"

class UHealthComponent; // Forward Declaration
```

## Class Layout

Classes must be organized by access level and functionality.

```cpp
UCLASS()
class MYMODULE_API UMyComponent : public UActorComponent
{
    GENERATED_BODY()
public:
    UMyComponent();
    virtual void TickComponent(...) override; // 1. Virtuals
    void Heal(float Amount); // 2. Public API
protected:
    virtual void BeginPlay() override; // 3. Protected Lifecycle
private:
    void UpdateState(); // 4. Internal Logic

    UPROPERTY(VisibleAnywhere, Category = "Health")
    TObjectPtr<UHealthComponent> HealthComponent; // 5. UProperties

    int32 InternalCounter = 0; // 6. Native Variables
};
```

---

# Modern UE5 C++ & Memory

## UObjects & Garbage Collection

Always track UObject references dynamically allocated or exposed to the editor.

Preferred pointer types:
- `TObjectPtr<T>`: For class members pointing to UObjects (replaces raw pointers in UE5).
- `TWeakObjectPtr<T>`: To observe UObjects without preventing garbage collection.
- `TSoftObjectPtr<T>`: For lazy-loading asynchronous assets.

**Never store unmanaged raw `UObject*` as class members without `UPROPERTY()`.**

## Standard C++ vs Unreal Types

- **Standard Containers**: Avoid using `std::` containers (`std::vector`, `std::string`) in gameplay code. Always prefer Unreal equivalents (`TArray`, `TMap`, `FString`). `std::` is only acceptable in standalone editor tools or isolated third-party wrappers.
- **No C++ Exceptions**: Unreal builds with exceptions disabled. Do not use `try/catch`.
- **Auto keyword**: Only use `auto` when the type is strictly obvious from the right side of the assignment, or for complex iterator types. Do not use it blindly.

## Const Correctness

Use `const` extensively.
- Pass parameters by `const Type&` when not modifying them.
- Mark getter functions as `const`.
- Use `const` pointers when the pointed-to object shouldn't be modified.

---

# Performance Guidelines

## Tick

Tick **must** be disabled by default in constructors:
```cpp
PrimaryActorTick.bCanEverTick = false;
PrimaryComponentTick.bCanEverTick = false;
```
Only enable Tick for continuous visual updates, interpolation, or custom physics. 
For logic state checks, use **Timers** or **Delegates**. If Tick is required, reduce frequency (`TickInterval = 0.1f`).

## Casting & Component Lookup

- **Avoid casting inside loops or Tick.**
- **Avoid string-based or class-based lookups (`FindComponentByClass`) in loops or Tick.**
- When you need to retrieve multiple components without allocating heap memory, use `TInlineComponentArray`:

```cpp
TInlineComponentArray<UPrimitiveComponent*> PrimitiveComponents(TargetActor);
for (UPrimitiveComponent* PrimComp : PrimitiveComponents) { ... }
```

Cache essential component references during initialization:

```cpp
void AMyActor::PostInitializeComponents()
{
    Super::PostInitializeComponents();

    HealthComponent = FindComponentByClass<UHealthComponent>();
    check(HealthComponent);
}
```

## Array Memory Preallocation

When populating arrays/maps and the final size is known (or roughly known), **always** use `Reserve()` to avoid hidden memory allocations.

```cpp
TArray<AActor*> ValidActors;
ValidActors.Reserve(SourceActors.Num());
```

---

# Assertions & Validation

Fail fast during development. Use Unreal's assertion macros.

- `check(Condition)`: Halts execution if false (stripped in Shipping).
- `checkf(Condition, TEXT("Message"))`: Halts with formatted log.
- `ensure(Condition)`: Logs a callstack the first time it fails, but continues execution.
- `ensureAlways(Condition)`: Like ensure, but logs every time it fails.

**Pointer Validation:**
```cpp
if (IsValid(TargetActor)) // preferred for Actors/UObjects (checks PendingKill)
{ ... }
```

---

# Strings & Text

Understand the difference between Unreal string types:
- **`FName`**: Fast, lightweight, immutable string used for IDs, tags, and map lookups. **Never use `FString` as a key in a `TMap`; always use `FName`.**
- **`FText`**: Localizable text. Used for all UI and player-facing text.
- **`FString`**: Mutable string for general manipulation and logging. Heavy.

---

# Asset References

Avoid unnecessary hard references that cause chain-loading.

**Bad** (Loads `AWeapon` into memory as soon as this class loads):
```cpp
UPROPERTY(EditDefaultsOnly)
TSubclassOf<AWeapon> WeaponClass;
```

**Good** (Loads only when explicitly requested):
```cpp
UPROPERTY(EditDefaultsOnly)
TSoftClassPtr<AWeapon> WeaponClass;
```

**Asynchronous Loading:**
For heavy assets, use the `FStreamableManager` from `UAssetManager` to load `TSoftObjectPtr` or `TSoftClassPtr` asynchronously, preventing hitches/freezing on the main thread.

## Hardcoded Paths
**Avoid** hardcoding asset paths in gameplay systems using `ConstructorHelpers::FObjectFinder` (e.g., `TEXT("/Game/P_Explosion")`). 
This is brittle and forces synchronous loading. Expose `UPROPERTY(EditDefaultsOnly)` on the class and assign the asset in Blueprint. Exception: Hardcoded paths are acceptable for core UI or developer tools.

---

# Interfaces & Subsystems

Use modern Epic paradigms for architecture decoupling.

## Interfaces & Loose Coupling
Avoid direct `Cast<T>` to specific classes for gameplay events. Hardcasting creates rigid dependencies and forces headers to be included across modules. 
Instead, use `UINTERFACE` to decouple systems.

```cpp
if (TargetActor->Implements<UInteractable>())
{
    IInteractable::Execute_OnInteract(TargetActor, Instigator);
}
```

**Rule of thumb for Interfaces:**
- Create interfaces based on **shared behavior** (e.g., `IDamageable`, `IInteractable`), not specific objects.
- Do not create hyper-specific micro-interfaces (`IDoorInterface`, `IChestInterface`).
- First check if an existing engine interface (like `IGameplayTaskOwnerInterface`) or `GameplayTags` can solve the problem before creating a new `UINTERFACE`.

## Subsystems
Use `UGameInstanceSubsystem`, `UWorldSubsystem`, or `ULocalPlayerSubsystem` for global managers instead of Singletons or massive Managers on the GameMode.

## Data-Driven Architecture (Data Assets)
Avoid hardcoding parameters or configurations purely into `UPROPERTY()` instance variables on Actors if those values describe a "type" or "definition" of an object (like Weapon stats, Character stats, Item data).
Instead, move those definitions into a `UPrimaryDataAsset` or `UDataAsset`.

```cpp
// GOOD: Data-Driven paradigm
UPROPERTY(EditDefaultsOnly, Category = "Config")
TObjectPtr<UWeaponDataAsset> WeaponConfig;
```

**Gameplay Tags:** Prefer `GameplayTags` over hardcoded enums or booleans when defining gameplay categories, states, or events.

## Static Functions & GetWorld()
Do not rely on implicit `GetWorld()` access within generic utility classes. 
When creating Blueprint macro libraries or static C++ helper functions, always ask for a `const UObject* WorldContextObject` to accurately trace the execution context.

```cpp
UFUNCTION(BlueprintCallable, meta = (WorldContext = "WorldContextObject"))
static void SpawnCustomEffect(const UObject* WorldContextObject);
```

---

# Logging & Debugging

Define custom log categories for systems.

```cpp
DEFINE_LOG_CATEGORY_STATIC(LogInventory, Log, All);
UE_LOG(LogInventory, Warning, TEXT("Inventory is full for %s!"), *GetName());
```

Use **Visual Logger** (`UE_VLOG`) for spatial, timeline-based debugging of AI and gameplay systems.

**Avoid excessive logging** in `Tick` or tight loops. Logging should never execute every frame unless protected by a flag.

---

# Delegates & Cleanup

Always remove delegates when objects are destroyed.

```cpp
void UMyComponent::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    Super::EndPlay(EndPlayReason);
    
    SomeDelegate.RemoveAll(this);
}
```

This prevents fatal crashes during shutdown or map transitions.

---

# Blueprint API & Event Handling

Expose Blueprint APIs intentionally and safely.
- `BlueprintCallable`: For functions that change state.
- `BlueprintPure`: For getter functions that do NOT modify state. Add `const`.
- `BlueprintReadOnly`: For properties that BP can read but only C++ should change.

## Enhanced Input System
UE5 utilizes the Enhanced Input System. **Never** use deprecated `Action/Axis Mappings` or `UPlayerInputComponent::BindAction`.
Always use `UEnhancedInputComponent` and `UInputAction` / `UInputMappingContext`.

```cpp
if (UEnhancedInputComponent* EnhancedInputComponent = Cast<UEnhancedInputComponent>(PlayerInputComponent))
{
    EnhancedInputComponent->BindAction(JumpAction, ETriggerEvent::Started, this, &ACharacter::Jump);
}
```

## Event Handling
When C++ needs to trigger logic that *might* be implemented in Blueprint, use:
- `BlueprintImplementableEvent`: C++ calls it, BP implements it. (No native C++ body).
- `BlueprintNativeEvent`: C++ provides a default implementation (via `*_Implementation()`), BP can override it.

Avoid exposing too much internal implementation detail.

---

# Constructor & Lifecycle Rules

**Do not execute heavy logic in constructors.**
Constructors must only be used for:
- Initializing default variables.
- Creating default subobjects (`CreateDefaultSubobject<T>`).

For object initialization and runtime logic, use the appropriate lifecycle hooks:
- **Actors**: `PostInitializeComponents()`, `BeginPlay()`.
- **Components**: `InitializeComponent()`, `OnRegister()`, `BeginPlay()`.

```cpp
// Constructor: Setup only
UMyComponent::UMyComponent()
{
    PrimaryComponentTick.bCanEverTick = false;
}

// Runtime logic
void UMyComponent::BeginPlay()
{
    Super::BeginPlay();
    // Cache references and start logic here
}
```

---

# Strict Module Isolation (Plugin-First)

All dependencies on other modules must be minimized.
- **Never** include headers from project game modules inside the plugin. (The plugin must not know about the game).
- Use **Interfaces** and **Delegates** to communicate outwards.
- Use **Forward Declarations** wherever possible instead of `#include`ing headers from other plugin modules.

---

# Unreal Naming Conventions

Follow Epic Games naming standards rigidly:

| Type | Prefix | Example |
| ---- | ------ | ------- |
| **Template** | `T` | `TArray` |
| **UObject** | `U` | `UHealthComponent` |
| **Actor** | `A` | `AWeapon` |
| **Struct** | `F` | `FVector` |
| **Enum** | `E` | `EEndPlayReason` |
| **Interface** | `I` | `IInteractable` |
| **Slate Widget** | `S` | `SButton` |
| **Boolean** | `b` | `bIsInitialized` |

---

# Multi-threading & Async Safety

**Never access, modify, or spawn `UObject`s or `AActor`s outside the Game Thread.**
Unreal Engine's Garbage Collector and UObject systems are strictly single-threaded.

- Always verify the current thread before complex UObject operations: `check(IsInGameThread());`
- Use `AsyncTask`, `FRunnable`, or `ParallelFor` strictly for abstract mathematical computations, data processing, or backend logic.
- When an async thread finishes, dispatch the result back to the Game Thread to update the game state safely:

```cpp
AsyncTask(ENamedThreads::GameThread, [this]()
{
    // Safe to modify UObjects here
});
```

---

# General Coding Style & Formatting

- **No Magic Numbers**: Never embed gameplay tuning values directly in code. Expose them via `UPROPERTY` or `UDataAsset`. For pure math constants, extract them to `constexpr` or `const` variables with meaningful names.
- **Braces**: Always use braces `{}` for control flow (`if`, `for`, `while`), even for single lines, to prevent macro expansion issues and maintain clean visual structure.
- **Enums**: Always prefer `enum class EnumName : uint8`. Use `TEnumAsByte<EEnumName>` **only** when interfacing with legacy APIs, specific unmanaged arrays for memory, or older serialization formats.

## Code Formatting

- **Unreal Engine C++ Style Guide**: All code must strictly follow the official Epic Games coding standards (indentation, naming, bracket placement).
- **clang-format**: Automate style enforcement using `.clang-format` based on the official Unreal Style.
- Format code locally in the IDE (Visual Studio, Rider, VSCode) before every commit.
- **Limit line length**: Keep horizontal columns readable (typically max 120 characters) and break logic vertically to aid Code Review parsing.

---

# Comments & Documentation

In the body of functions and methods, **DO NOT write comments**. The code must be entirely self-documenting.

**Mandatory comments** are allowed *only* for `UPROPERTY` and `UFUNCTION` declarations using Javadoc format (`/** ... */`) for Editor tooltips. No inline logic comments. No variable comments.

```cpp
// BAD: Inline comment explaining logic
float Health = 100.f; // The starting health

// GOOD: Editor-facing Tooltip
/** The maximum health value this character can have. */
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Health")
float MaxHealth;
```

---

# Code Generation Checklist

Before generating or modifying code, verify:
- [ ] Uses IWYU and Forward Declarations.
- [ ] Logic stays out of constructors (deferred to `BeginPlay`/`InitializeComponent`).
- [ ] Strict Module Isolation (Plugin doesn't depend on Game logic).
- [ ] Tick disabled unless absolutely required.
- [ ] Code avoids heavy logic or operations in `Tick`.
- [ ] Safe pointer usage (`TObjectPtr`, `UPROPERTY()`).
- [ ] Validation macros (`check`, `ensure`, `IsValid`) used appropriately.
- [ ] `const` correctness applied to types and methods.
- [ ] Enums use `enum class` and `ENUM_CLASS_FLAGS` for bitmasks.
- [ ] Soft references used for assets with `FStreamableManager` for async loading.
- [ ] Asset references exposed through `UPROPERTY` instead of hardcoded paths.
- [ ] Memory preallocated (`Reserve`) where possible for `TArray`/`TMap`/`TSet`.
- [ ] Subsystems and Interfaces used to decouple logic (Gameplay logic separated from presentation logic).
- [ ] Blueprint APIs safely and minimally exposed.
- [ ] BP Events explicitly use `BlueprintImplementableEvent` or `BlueprintNativeEvent`.
- [ ] No magic numbers; constants and constexpr used instead.
- [ ] UObject modifications strictly confined to the Game Thread.
- [ ] No inline comments; Javadoc Tooltips used exclusively for UPROPERTY/UFUNCTION.
- [ ] Code formatted automatically via `clang-format` or strict adherence to the Unreal Style Guide.
- [ ] Code remains modular and maintainable.

---

# Code Quality Goals

Generated code should prioritize:
- strict adherence to Unreal architecture
- fast compile times (IWYU)
- memory safety and garbage collection compliance
- performance (No tick, Reserved Memory, Enum/FName over strings)
- readability

---

# Priority

Rules defined in this skill override generic coding suggestions when developing Unreal Engine C++ systems.