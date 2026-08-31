---
name: vue-best-practices
description: MUST be used for Vue.js tasks. Strongly recommends Vue 3 Composition API with `<script setup>` as the standard approach. Choose JavaScript or TypeScript by code stability and reuse scope: JavaScript for volatile business code, JavaScript with optional JSDoc for moderately stable shared code, and TypeScript for stable contract-heavy foundation code. Uses mandatory four-space indentation and prefers Promise chaining plus UI loading locks for async API/interface calls. Covers Vue 3, SSR, Volar, vue-tsc. Load for any Vue, .vue files, Vue Router, Pinia, or Vite with Vue work. ALWAYS use Composition API unless the project explicitly requires Options API.
license: MIT
metadata:
    author: github.com/vuejs-ai
    customized_by: github.com/LingYzh
    upstream_version: "18.0.0"
    version: "18.2.0-personal.2"
---

# Vue Best Practices Workflow

Use this skill as an instruction set. Follow the workflow in order unless the user explicitly asks for a different order.

## Core Principles
- **Keep state predictable:** one source of truth, derive everything else.
- **Make data flow explicit:** Props down, Events up for most cases.
- **Favor small, focused components:** easier to test, reuse, and maintain.
- **Avoid unnecessary re-renders:** use computed properties and watchers wisely.
- **Readability counts:** write clear, self-documenting code.
- **Language follows stability:** do not default all Vue code to TypeScript; choose JS, JS + JSDoc, or TS according to expected change frequency, reuse scope, API stability, and the cost of breaking consumers.
- **Four-space indentation is mandatory:** use four ASCII spaces per indentation level in all authored or edited code; never use tabs for indentation.
- **Async UI must be guarded:** prefer Promise chaining for API/interface calls and lock conflicting UI actions while the request is pending.

## 1) Confirm architecture before coding (required)

- Default framework style: Vue 3 + Composition API + `<script setup>`.
- Do **not** assume `<script setup lang="ts">` is the default.
- Respect the existing project's local language conventions when editing existing code, except for the mandatory four-space indentation policy in section `1.2`.
- If the project explicitly uses Options API, load `vue-options-api-best-practices` skill if available.
- If the project explicitly uses JSX, load `vue-jsx-best-practices` skill if available.

### 1.1 Choose the language tier before creating or substantially rewriting code (required)

Classify the code by expected stability and responsibility before choosing JavaScript or TypeScript.

#### Tier A — Business / volatile: default to JavaScript

Use plain JavaScript for code that is expected to change frequently with product requirements:

- pages and route views
- CRUD, forms, dashboards, admin/business pages
- feature-specific components
- feature-specific composables
- business orchestration / glue code
- prototypes and rapidly evolving features

Default SFC form:

```vue
<script setup>
// business logic
</script>
```

The primary optimization goal here is low editing friction and easy maintenance during frequent requirement changes.

#### Tier B — Shared / moderately stable: default to JavaScript + optional JSDoc

Use JavaScript for shared code that is reused across multiple features but still evolves regularly. Add JSDoc only at boundaries where it materially improves editor hints or clarifies a non-obvious contract.

Typical examples:

- shared components used by several pages
- common but still evolving composables
- shared utilities
- feature-family abstractions

Do not add JSDoc to every local variable or obvious function merely to imitate TypeScript syntax.

#### Tier C — Foundation / stable contract: prefer TypeScript

Use TypeScript when code is low-change, broadly reused, and has a stable public contract where breaking consumers is costly.

Typical examples:

- base / UI-library components
- stable design-system primitives
- library-like shared composables
- infrastructure wrappers
- long-lived reusable modules with important props/emits/slots or generic contracts

TypeScript is valuable here because the interface is expected to stay stable enough for the type maintenance cost to pay back over many consumers.

#### Language decision rules

Use these signals in order:

1. Existing local convention in the file/module being edited.
2. Expected change frequency.
3. Reuse scope and number of consumers.
4. API/contract stability.
5. Cost of breaking downstream consumers.

Additional rules:

- When uncertain for **new business code**, choose JavaScript.
- Do **not** migrate JavaScript to TypeScript as an incidental refactor.
- Do **not** migrate TypeScript to JavaScript incidentally either; language migration must be an explicit task or have a concrete technical reason.
- A file becoming reusable once is not enough reason to convert it to TypeScript.
- TypeScript availability in the project is not, by itself, a reason to use it for every new file.
- Explicit project requirements or user instructions override this tier policy.

### 1.2 Mandatory formatting policy (required)

Use **four ASCII spaces per indentation level** in all code you create or edit.

- Apply four-space indentation consistently to Vue templates, `<script>`, `<style>`, JavaScript, TypeScript, JSON, YAML, CSS, and other hand-maintained source/config files.
- Never use tabs for indentation.
- When editing a pre-existing file that uses 2-space or mixed indentation, normalize the **entire edited file** to four-space indentation before finishing. Do not leave mixed indentation behind.
- Formatting cleanup caused by this rule is intentional and belongs in the same task/patch.
- Do not reformat generated, vendored, minified, lock, or machine-managed files unless the task explicitly requires editing them.
- This personal formatting rule overrides indentation shown in upstream examples or the surrounding project when a hand-maintained source/config file is edited.

### 1.3 Must-read core references (required)

- Before implementing any Vue task, make sure to read and apply these core references:
    - `references/reactivity.md`
    - `references/sfc.md`
    - `references/component-data-flow.md`
    - `references/composables.md`
- Keep these references in active working context for the entire task, not only when a specific issue appears.

### 1.4 Plan component boundaries before coding (required)

Create a brief component map before implementation for any non-trivial feature.

- Define each component's single responsibility in one sentence.
- Keep entry/root and route-level view components as composition surfaces by default.
- Move feature UI and feature logic out of entry/root/view components unless the task is intentionally a tiny single-file demo.
- Define props/emits contracts for each child component in the map.
- Prefer a feature folder layout (`components/<feature>/...`, `composables/use<Feature>.js`) for volatile business features; use `.ts` for the composable when it clearly belongs to Tier C or the existing project convention requires it.

## 2) Apply essential Vue foundations (required)

These are essential, must-know foundations. Apply all of them in every Vue task using the core references already loaded in section `1.3`.

### Reactivity

- Must-read reference from `1.3`: [reactivity](references/reactivity.md)
- Keep source state minimal (`ref`/`reactive`), derive everything possible with `computed`.
- Use watchers for side effects if needed.
- Avoid recomputing expensive logic in templates.

### SFC structure and template safety

- Must-read reference from `1.3`: [sfc](references/sfc.md)
- Keep SFC sections in this order: `<script>` → `<template>` → `<style>`.
- Apply the language tier from section `1.1` when choosing `<script setup>` vs `<script setup lang="ts">`.
- Apply four-space indentation from section `1.2` to the entire edited SFC, including template, script, and style blocks.
- Keep SFC responsibilities focused; split large components.
- Keep templates declarative; move branching/derivation to script.
- Apply Vue template safety rules (`v-html`, list rendering, conditional rendering choices).

### Keep components focused

Split a component when it has **more than one clear responsibility** (e.g. data orchestration + UI, or multiple independent UI sections).

- Prefer **smaller components + composables** over one “mega component”.
- Move **UI sections** into child components (props in, events out).
- Move **state/side effects** into composables (`useXxx()`).

Apply objective split triggers. Split the component if **any** condition is true:

- It owns both orchestration/state and substantial presentational markup for multiple sections.
- It has 3+ distinct UI sections (for example: form, filters, list, footer/status).
- A template block is repeated or could become reusable (item rows, cards, list entries).

Entry/root and route view rule:

- Keep entry/root and route view components thin: app shell/layout, provider wiring, and feature composition.
- Do not place full feature implementations in entry/root/view components when those features contain independent parts.
- For CRUD/list features (todo, table, catalog, inbox), split at least into:
    - feature container component
    - input/form component
    - list (and/or item) component
    - footer/actions or filter/status component
- Allow a single-file implementation only for very small throwaway demos; if chosen, explicitly justify why splitting is unnecessary.

### Component data flow

- Must-read reference from `1.3`: [component-data-flow](references/component-data-flow.md)
- Use props down, events up as the primary model.
- Use `v-model` only for true two-way component contracts.
- Use provide/inject only for deep-tree dependencies or shared context.
- Keep contracts explicit using runtime props/emits in JavaScript, optional JSDoc for Tier B shared code, and type-based `defineProps` / `defineEmits` / `InjectionKey` when TypeScript is appropriate for Tier C.

### Composables

- Must-read reference from `1.3`: [composables](references/composables.md)
- Extract logic into composables when it is reused, stateful, or side-effect heavy.
- Keep composable APIs small and predictable.
- Use JavaScript for volatile feature composables, JavaScript + optional JSDoc for moderately stable shared composables, and TypeScript for stable library-like composables.
- Do not introduce TypeScript solely for editor hints when JSDoc or runtime contracts are sufficient.
- Separate feature logic from presentational components.

### Async API/interface calls and UI loading locks

When a Vue UI triggers an asynchronous API/interface request, load and apply [async-interface-ui](references/async-interface-ui.md).

- Prefer Promise chaining (`.then().catch().finally()`) for API/interface calls by default.
- Use `async` / `await` only when chaining would make the control flow materially harder to read or when an external API requires it.
- Set an operation-specific loading state before starting the request.
- Guard handlers against duplicate invocation while loading.
- Block duplicate or conflicting user actions while the request is pending.
- Reflect the lock in the UI with `disabled`, loading indicators, or equivalent interaction guards.
- Release the lock in `.finally()` so both success and failure paths restore the UI.
- Keep unrelated UI usable when it is safe; prefer operation-scoped locks over freezing the whole page.

## 3) Consider optional features only when requirements call for them

### 3.1 Standard optional features

Do not add these by default. Load the matching reference only when the requirement exists.

- Slots: parent needs to control child content/layout -> [component-slots](references/component-slots.md)
- Fallthrough attributes: wrapper/base components must forward attrs/events safely -> [component-fallthrough-attrs](references/component-fallthrough-attrs.md)
- Built-in component `<KeepAlive>` for stateful view caching -> [component-keep-alive](references/component-keep-alive.md)
- Built-in component `<Teleport>` for overlays/portals -> [component-teleport](references/component-teleport.md)
- Built-in component `<Suspense>` for async subtree fallback boundaries -> [component-suspense](references/component-suspense.md)
- Animation-related features: pick the simplest approach that matches the required motion behavior.
    - Built-in component `<Transition>` for enter/leave effects -> [transition](references/component-transition.md)
    - Built-in component `<TransitionGroup>` for animated list mutations -> [transition-group](references/component-transition-group.md)
    - Class-based animation for non-enter/leave effects -> [animation-class-based-technique](references/animation-class-based-technique.md)
    - State-driven animation for user-input-driven animation -> [animation-state-driven-technique](references/animation-state-driven-technique.md)

### 3.2 Less-common optional features

Use these only when there is explicit product or technical need.

- Directives: behavior is DOM-specific and not a good composable/component fit -> [directives](references/directives.md)
- Async components: heavy/rarely-used UI should be lazy loaded -> [component-async](references/component-async.md)
- Render functions only when templates cannot express the requirement -> [render-functions](references/render-functions.md)
- Plugins when behavior must be installed app-wide -> [plugins](references/plugins.md)
- State management patterns: app-wide shared state crosses feature boundaries -> [state-management](references/state-management.md)

## 4) Run performance optimization after behavior is correct

Performance work is a post-functionality pass. Do not optimize before core behavior is implemented and verified.

- Large list rendering bottlenecks -> [perf-virtualize-large-lists](references/perf-virtualize-large-lists.md)
- Static subtrees re-rendering unnecessarily -> [perf-v-once-v-memo-directives](references/perf-v-once-v-memo-directives.md)
- Over-abstraction in hot list paths -> [perf-avoid-component-abstraction-in-lists](references/perf-avoid-component-abstraction-in-lists.md)
- Expensive updates triggered too often -> [updated-hook-performance](references/updated-hook-performance.md)

## 5) Final self-check before finishing

- Core behavior works and matches requirements.
- All must-read references were read and applied.
- The chosen JS/JSDoc/TS tier matches the code's stability and responsibility.
- No incidental JavaScript ↔ TypeScript migration was introduced.
- Every edited hand-maintained code/config file uses four-space indentation consistently.
- Reactivity model is minimal and predictable.
- SFC structure and template rules are followed.
- Components are focused and well-factored, splitting when needed.
- Entry/root and route view components remain composition surfaces unless there is an explicit small-demo exception.
- Component split decisions are explicit and defensible (responsibility boundaries are clear).
- Data flow contracts are explicit and expressed appropriately for the selected language tier.
- Composables are used where reuse/complexity justifies them.
- Moved state/side effects into composables if applicable.
- Async API/interface calls prefer Promise chaining and have a correct loading/interaction lock when they can be triggered from the UI.
- Optional features are used only when requirements demand them.
- Performance changes were applied only after functionality was complete.
