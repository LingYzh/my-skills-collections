---
name: vue-best-practices
description: MUST be used for Vue.js and uni-app Vue tasks. Defaults to Vue 3 Composition API with `<script setup>` for new code while respecting existing project architecture. Chooses JavaScript, optional JSDoc, or TypeScript by code stability; enforces four-space indentation; uses task-scoped reference loading; avoids incidental dependencies/refactors; and applies explicit uni-app platform gates plus async UI loading locks.
license: MIT
metadata:
    author: github.com/vuejs-ai
    customized_by: github.com/LingYzh
    upstream_version: "18.0.0"
    version: "18.4.0-personal.4"
---

# Vue Best Practices Workflow

Use this Skill as a decision framework, not as permission to rewrite unrelated project architecture.

## Core Principles

- **Respect the task boundary:** solve the requested problem before pursuing cleanup or architecture changes.
- **Respect existing architecture:** do not migrate working patterns incidentally.
- **Language follows stability:** JS for volatile business code, JS + optional JSDoc for moderately stable shared code, TS for stable contract-heavy foundation code.
- **Four-space indentation is mandatory:** normalize every edited hand-maintained code/config file to four ASCII spaces.
- **Prefer locality for volatile business code:** extraction is useful only when it creates a meaningful responsibility/reuse/lifecycle boundary.
- **Keep state ownership predictable:** minimize duplicated source state and derive values when practical.
- **Make data flow understandable:** use the simplest communication mechanism that keeps ownership clear.
- **Platform comes before Web assumptions:** uni-app targets must pass the platform compatibility gate before browser-oriented Vue guidance is applied.
- **Async UI must be guarded:** user-triggered requests need operation-level loading/interaction locks.
- **Dependencies are explicit architecture decisions:** examples are never authorization to install third-party packages.
- **Performance is evidence-driven:** optimize measured hot paths, not magic thresholds from examples.

## 1. Confirm Context Before Coding

For a small localized edit, keep this quick. For a new feature or multi-file change, inspect enough surrounding code to understand the existing pattern.

Determine:

1. Vue version / relevant runtime constraints when they affect the task.
2. Whether this is normal Web Vue, SSR, uni-app H5, uni-app App, mini program, or another compiled target.
3. Existing API style: Composition API / Options API / JSX where relevant.
4. Existing language and formatting conventions in the files being edited.
5. Existing project utilities, stores, request wrappers, UI/loading patterns, and dependencies that should be reused.

### Existing architecture beats incidental migration

- New Vue 3 code defaults to Composition API + `<script setup>`.
- If an existing component uses Options API, **do not migrate it to Composition API as part of an unrelated edit**.
- Do not migrate JSX/templates, state-management patterns, router patterns, styling systems, JS/TS, or dependency choices incidentally.
- Architecture migration should be an explicit task with a concrete benefit.

## 1.1 Choose the Language Tier

### Tier A — Business / volatile: JavaScript

Default to plain JavaScript for frequently changing product code:

- pages / route views
- CRUD, forms, dashboards, admin/business screens
- feature-specific components
- feature-specific composables
- orchestration / glue code
- prototypes and rapidly evolving requirements

```vue
<script setup>
// volatile business logic
</script>
```

### Tier B — Shared / moderately stable: JavaScript + optional JSDoc

Use JavaScript for shared code that still changes regularly. Add JSDoc only where a non-obvious shared contract benefits from editor help.

Do not imitate TypeScript by annotating every local variable/function.

### Tier C — Foundation / stable contract: TypeScript

Prefer TypeScript for low-change, broadly reused, contract-heavy code such as stable base UI/design-system primitives, mature shared modules, and library-like composables.

### Language decision order

1. Existing language in the file/module being edited.
2. Expected change frequency.
3. Reuse scope / number of consumers.
4. Contract stability.
5. Cost of breaking consumers.

Rules:

- New uncertain business code -> choose JavaScript.
- Do not migrate JS -> TS or TS -> JS incidentally.
- A second consumer is not sufficient reason to convert code to TypeScript.
- TypeScript being installed is not a reason to use it for every file.
- Explicit user/project requirements override this tier policy.

## 1.2 Mandatory Four-Space Formatting

Use **four ASCII spaces per indentation level** in every hand-maintained code/config file you create or edit.

Applies to Vue template/script/style, JavaScript, TypeScript, JSON, YAML, CSS, and similar files.

- Never use tabs for indentation.
- When editing a legacy 2-space/mixed-indentation file, normalize the **entire edited file** to four spaces.
- Do not reformat generated, vendored, minified, lock, or machine-managed files unless the task explicitly requires it.
- This policy intentionally overrides upstream examples and an existing 2-space convention for hand-maintained files that are edited under this Skill.

Keep project-controlled formatting tools aligned when they would otherwise revert edited source:

- EditorConfig: `indent_style = space`, `indent_size = 4`
- Prettier: `tabWidth: 4`, `useTabs: false`
- ESLint / Vue indentation rules: configure the applicable indentation width to `4`
- If one formatter is authoritative, disable conflicting formatting rules instead of making tools fight each other

## 1.3 Global Dependency Discipline

This generic Skill should be **dependency-neutral**.

- Do not install, replace, or migrate to a third-party package merely because a reference/example mentions a capability.
- Prefer native Vue/platform capabilities and dependencies/utilities already present in the project.
- If the project already uses a third-party library, maintain it according to the project's established conventions; do not promote that library into a generic recommendation.
- If a new dependency is genuinely required, make it an explicit architectural change with a concrete reason and user/task justification.
- Third-party-specific best practices belong in a dedicated Skill or project documentation, not in this generic Vue Skill.
- Placeholder names such as `ProjectVirtualList` or `sanitizeTrustedHtml` represent existing/project-owned abstractions, not packages to install.

## 1.4 Load References by Task — Do Not Preload Everything

Do **not** load all core references for every Vue task. Load only the references that materially affect the current work.

### Common routing

- reactive state / computed / watch -> `references/reactivity.md`
- SFC/template/style / refs / `v-if` / `v-for` / `v-html` -> `references/sfc.md`
- props / emits / `v-model` / provide/inject / component refs -> `references/component-data-flow.md`
- composable design/extraction -> `references/composables.md`
- UI-triggered API/interface request -> `references/async-interface-ui.md`
- shared/global state architecture -> `references/state-management.md`
- uni-app task or platform-sensitive Vue API in uni-app -> **always first** `references/uni-app-platform.md`

### When to load multiple references

Load several references when the task genuinely spans several concerns, such as creating a new feature with state, child components, async requests, and composables.

For a tiny edit (text, one condition, one CSS fix), do not consume unrelated references.

Keep only currently relevant references in active working context.

## 1.5 Plan Component Boundaries Only When the Change Needs It

For a simple/local edit, do not produce a component architecture exercise.

For a new non-trivial feature or a change spanning multiple components, briefly identify responsibilities and communication boundaries before implementation.

### Split components when a meaningful boundary exists

Good split signals:

- an independently meaningful/reusable UI or behavior unit
- a distinct lifecycle/side-effect boundary
- state ownership becomes clearer in a child
- a stable public component contract exists
- a section has enough independent complexity that isolation reduces maintenance cost
- the same meaningful block is reused

### Do not split based on arbitrary thresholds

Do **not** require splitting because:

- a component has 3+ visual sections
- a file passed a line count
- a CRUD page “should” have container/form/list/footer components
- a template block could theoretically be reusable someday
- a route view is assumed to be only a thin composition shell

A cohesive business page may intentionally keep related volatile logic/UI together when that makes frequent changes easier.

Do not turn one maintainable feature into many one-use files without a clear boundary.

## 2. Apply Relevant Vue Foundations

### Reactivity

When reactive choices matter, load `references/reactivity.md`.

- `ref()` is the normal primitive/default ref.
- `shallowRef()` is for intentionally shallow/opaque/large root-replacement state, not a primitive micro-optimization.
- Prefer `computed()` for meaningful derived state.
- Keep computed getters pure.
- Use watchers for side effects/synchronization.

### SFC / template / styling

When template/SFC structure matters, load `references/sfc.md`.

- Keep SFC sections readable and use four-space indentation.
- Apply the JS/JSDoc/TS tier.
- Treat `v-html` as a trust boundary.
- Application components can prefer scoped/local styles; stable foundation/library components may expose class/module/token style contracts according to the project.
- DOM-oriented examples are browser guidance, not universal uni-app guidance.

### Component data flow

When component communication matters, load `references/component-data-flow.md`.

- Props/events are the ordinary parent-child default.
- `v-model` is for intentional two-way contracts.
- Provide/inject is chosen by contextual ownership / pass-through pain, **not by a fixed component-depth number**.
- Component refs are for genuine imperative APIs.

### Composables

When extraction/design matters, load `references/composables.md`.

- Reuse/coherent responsibility/lifecycle are good extraction reasons.
- File length, ref count, or “clean architecture” aesthetics alone are not.
- Prefer locality for volatile one-off business workflows when extraction would increase navigation cost.

### Async API/interface calls

When UI triggers an asynchronous request, load `references/async-interface-ui.md`.

- Prefer `.then().catch().finally()` for ordinary interface/API request flow.
- Guard duplicate handler entry.
- Lock conflicting UI while pending.
- Keep unrelated UI available when safe.
- Release application-level reactive/business locks in `.finally()`.
- In uni-app, native loading/toast ordering follows the platform-specific rule in that reference.

### uni-app

For **every uni-app task**, load `references/uni-app-platform.md` before browser-oriented optional references.

- Identify actual target(s).
- Do not assume browser DOM outside H5.
- Do not introduce ordinary Vue Router/`RouterView` architecture into normal uni-app page routing.
- Gate Vue built-ins and refs by target compatibility.
- Platform compatibility overrides generic Web Vue references.

## 3. Optional Features — Load Only When Required

### Common optional features

- Slots -> `references/component-slots.md`
- Fallthrough attrs -> `references/component-fallthrough-attrs.md`
- KeepAlive -> `references/component-keep-alive.md` (platform gate in uni-app)
- Teleport -> `references/component-teleport.md` (platform gate in uni-app)
- Transition -> `references/component-transition.md` (platform gate in uni-app)
- TransitionGroup -> `references/component-transition-group.md` (platform gate in uni-app)
- Class/state-driven animation -> matching animation reference

### Less-common / architecture-sensitive

- Directives -> `references/directives.md`
- Async components -> `references/component-async.md`
- Render functions -> `references/render-functions.md`
- Plugins -> `references/plugins.md`
- State management -> `references/state-management.md`

### Experimental

- Suspense -> `references/component-suspense.md`

Do not introduce Suspense by default; it remains an experimental Vue feature and requires explicit architectural intent plus platform compatibility.

## 4. Performance Comes After Correctness and Evidence

Do not optimize based on generic thresholds.

- very large/expensive mounted list -> `references/perf-virtualize-large-lists.md`
- known static subtree update issue -> `references/perf-v-once-v-memo-directives.md`
- measured list component-overhead hot path -> `references/perf-avoid-component-abstraction-in-lists.md`
- expensive update hook -> `references/updated-hook-performance.md`

Rules:

- reproduce/measure the problem first when practical
- do not use arbitrary “N items” or “N components” cutoffs from examples
- do not install a performance package automatically
- preserve maintainability unless measurement shows the abstraction is materially costly

## 5. Final Self-Check

Before finishing, verify only what is relevant to the task:

- requested behavior is correct
- no unrelated architecture/language/dependency migration was introduced
- edited hand-maintained files use four-space indentation consistently
- formatter/linter/editor settings will not immediately undo the indentation rule
- selected references matched the actual task instead of being loaded mechanically
- reactive primitives are appropriate (`ref()` is not replaced by `shallowRef()` without reason)
- component/composable splitting has a real responsibility/reuse/lifecycle benefit
- data ownership/communication is understandable
- UI-triggered async operations have correct loading/interaction locks
- uni-app platform-sensitive code passed the platform gate
- no third-party dependency was added merely because a Skill example suggested a capability
- experimental/optional Vue features were introduced only with explicit need
- performance work is supported by a real requirement or measured bottleneck
