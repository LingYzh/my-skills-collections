---
name: vue-best-practices
description: MUST be used for Vue.js and uni-app Vue tasks. Defaults to Vue 3 Composition API with `<script setup>` for new code while respecting existing project architecture. Chooses JavaScript, optional JSDoc, or TypeScript by code stability; enforces four-space indentation; uses task-scoped reference loading; treats Pinia and Axios as approved ecosystem dependencies; prefers layered request wrappers/API modules; and applies explicit uni-app platform gates plus async UI loading locks.
license: MIT
metadata:
    author: github.com/vuejs-ai
    customized_by: github.com/LingYzh
    upstream_version: "18.0.0"
    version: "18.6.0-personal.6"
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
- **Layer request code deliberately:** configured request transport -> semantic API functions -> business/UI Promise chains.
- **Platform comes before assumptions:** uni-app targets must pass the platform compatibility gate before browser-oriented Vue guidance is applied.
- **Async UI must be guarded:** user-triggered requests need operation-level loading/interaction locks.
- **Dependencies remain deliberate:** examples are not general authorization to install packages, with explicit approved exceptions for Pinia and Axios under the rules below.
- **Performance is evidence-driven:** optimize measured hot paths, not magic thresholds from examples.

## 1. Confirm Context Before Coding

For a small localized edit, keep this quick. For a new feature or multi-file change, inspect enough surrounding code to understand the existing pattern.

Determine:

1. Vue version / relevant runtime constraints when they affect the task.
2. Whether this is normal Web Vue, SSR, uni-app H5, uni-app App, mini program, or another compiled target.
3. Existing API style: Composition API / Options API / JSX where relevant.
4. Existing language and formatting conventions in the files being edited.
5. Existing project utilities, stores, request wrappers, API-module organization, UI/loading patterns, and dependencies that should be reused.

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

## 1.3 Dependency Discipline and Approved Ecosystem Exceptions

The default rule is dependency-conservative: do not install or replace packages merely because an example mentions a capability.

Prefer, in order:

1. existing project infrastructure
2. native Vue/platform capabilities
3. an approved ecosystem dependency when it clearly fits the requirement
4. another new dependency only with an explicit technical reason

### Approved: Pinia

Pinia is treated as the preferred/default Vue app-level state-management solution when a real global state boundary exists.

- If the project already uses Pinia, follow its existing conventions.
- For a new Vue app that genuinely needs app-level shared state, Pinia may be introduced directly.
- Do not globalize local/feature state merely because Pinia is available.
- Do not replace another established store solution incidentally.
- Apply the normal JS/JSDoc/TS language tiers to stores.

Load `references/state-management.md` when this decision matters.

### Approved: Axios

Axios is an approved request-layer dependency for Vue and uni-app projects when it fits the actual runtime/project architecture.

Preferred architecture when Axios is used:

```text
utils/request.js
    -> configured Axios instance + interceptors
api/<feature>.js
    -> named semantic endpoint functions
page/component
    -> business Promise chain + UI loading/interaction lock
```

Rules:

- If the project already has an Axios-based `request` wrapper, reuse it.
- Keep `baseURL`, token/header logic, common interceptors, transport error normalization, serialization, and similar cross-request concerns in the configured request layer.
- Define endpoint URL/method/params in API/domain modules instead of scattering raw Axios/request configs through pages/components.
- Business pages/components should normally import semantic API functions and call `listXxx(...).then(...).catch(...).finally(...)`.
- Respect the request wrapper's resolved response shape. If the interceptor already returns `response.data`, do not unwrap `.data` again in the business layer.
- Keep operation-specific UI loading locks in the page/component/business layer rather than burying them in a global request interceptor.
- Do not replace a working request architecture incidentally.

Axios approval is **not limited to H5/Web**. In uni-app, do not reject Axios merely because the target is App or a mini program. Reuse/choose Axios when the actual target/project setup is verified compatible.

Use `uni.request` or a project wrapper around it when a concrete runtime/network capability requires it, when the current Axios setup is actually incompatible, or when multi-target compatibility has not been verified.

Load `references/async-interface-ui.md` and, for uni-app, `references/uni-app-platform.md`.

### Other third-party libraries

For libraries other than the approved exceptions above:

- do not install them merely because a Skill example could use them
- reuse an existing project dependency when appropriate
- make a new dependency an explicit technical decision
- keep library-specific deep guidance in a dedicated Skill/project document rather than turning this generic Vue Skill into a package catalog

## 1.4 Load References by Task — Do Not Preload Everything

Do **not** load all core references for every Vue task. Load only references that materially affect the current work.

### Common routing

- reactive state / computed / watch -> `references/reactivity.md`
- SFC/template/style / refs / `v-if` / `v-for` / `v-html` -> `references/sfc.md`
- props / emits / `v-model` / provide/inject / component refs -> `references/component-data-flow.md`
- composable design/extraction -> `references/composables.md`
- UI-triggered API/interface request / Axios / request wrapper -> `references/async-interface-ui.md`
- shared/global state architecture / Pinia -> `references/state-management.md`
- uni-app task or platform-sensitive Vue API in uni-app -> **always first** `references/uni-app-platform.md`

Load several references only when the task genuinely spans several concerns. For a tiny edit, do not consume unrelated references.

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

### State management

When state crosses page/feature boundaries, load `references/state-management.md`.

- Keep local state local.
- Use feature composables for feature-scoped ownership.
- Use Pinia as the preferred default when a genuine app-level store boundary exists and no competing established architecture should be preserved.

### Async API/interface calls

When UI triggers an asynchronous request, load `references/async-interface-ui.md`.

- Prefer configured request layer -> named API function -> business/UI call chain.
- Prefer `.then().catch().finally()` for ordinary interface/API request flow.
- Keep endpoint strings/methods/params out of volatile UI code when a semantic API module is appropriate.
- Respect normalized response values returned by request interceptors.
- Guard duplicate handler entry.
- Lock conflicting UI while pending.
- Keep unrelated UI available when safe.
- Release application-level reactive/business locks in `.finally()`.
- In uni-app, choose Axios vs `uni.request` from actual compatibility instead of a blanket platform split.

### uni-app

For **every uni-app task**, load `references/uni-app-platform.md` before browser-oriented optional references.

- Identify actual target(s).
- Do not assume browser DOM outside H5.
- Do not introduce ordinary Vue Router/`RouterView` architecture into normal uni-app page routing.
- Do not assume App/mini-program means Axios is unavailable.
- Reuse a working Axios request layer when the actual target is compatible.
- Switch to `uni.request` / platform transport when a concrete compatibility or platform-network capability requires it.
- Gate Vue built-ins and refs by target compatibility.

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
- State management / Pinia -> `references/state-management.md`

### Experimental

- Suspense -> `references/component-suspense.md`

Do not introduce Suspense by default; it requires explicit architectural intent plus platform compatibility.

## 4. Performance Comes After Correctness and Evidence

Do not optimize based on generic thresholds.

- very large/expensive mounted list -> `references/perf-virtualize-large-lists.md`
- known static subtree update issue -> `references/perf-v-once-v-memo-directives.md`
- measured list component-overhead hot path -> `references/perf-avoid-component-abstraction-in-lists.md`
- expensive update hook -> `references/updated-hook-performance.md`

Rules:

- reproduce/measure the problem first when practical
- do not use arbitrary “N items” or “N components” cutoffs from examples
- do not install an unapproved performance package automatically
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
- app-level shared state uses the existing solution or an intentional Pinia boundary
- Axios/request code follows the existing request-layer/API-module/business-layer organization where applicable
- business code respects the request wrapper's resolved response contract
- UI-triggered async operations have correct loading/interaction locks
- uni-app transport choice is based on actual compatibility instead of a blanket H5/non-H5 assumption
- non-approved third-party dependencies were not added merely because an example suggested a capability
- experimental/optional Vue features were introduced only with explicit need
- performance work is supported by a real requirement or measured bottleneck
