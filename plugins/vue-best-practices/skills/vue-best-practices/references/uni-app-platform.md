---
title: uni-app Platform Compatibility Gate
impact: HIGH
impactDescription: uni-app compiles Vue code to multiple runtimes whose component, DOM, routing, networking, and platform capabilities differ materially
type: platform-gate
tags: [vue3, uni-app, h5, app, mini-program, platform, compatibility, routing, dom, request, axios]
---

# uni-app Platform Compatibility Gate

Load this reference for **every uni-app task before applying browser-oriented Vue guidance**.

A `.vue` file in uni-app is not evidence that browser DOM APIs, Vue Router patterns, or every Vue built-in component is available on the target runtime. Networking must also be selected from the actual project/target behavior rather than a blanket H5/non-H5 rule.

## Task List

- Identify the actual build target(s) before selecting Vue APIs
- Treat H5/Web, App, and mini-program targets as different runtimes
- Do not assume `window`, `document`, browser DOM nodes, or browser event APIs outside H5
- Do not introduce Vue Router / `RouterView` patterns into ordinary uni-app page routing
- Check target support before using dynamic components, transition built-ins, keep-alive, teleport, suspense, or DOM-oriented template refs
- Reuse an existing Axios/request layer when it is already proven compatible with the actual target
- Do not force `uni.request` merely because the target is App or a mini program
- Use `uni.request` / an existing uni request wrapper when there is a concrete compatibility or platform-capability reason
- Preserve multi-platform compatibility when the feature is shared across targets
- Apply `async-interface-ui.md` for request layering and `uni.showLoading()` / `uni.showToast()` ordering

## 1. Identify the Target First

Before implementing a platform-sensitive feature, determine whether the project/feature targets:

- H5 / Web
- App
- WeChat mini program
- another mini-program target
- multiple targets from the same source

Look at the project's existing configuration, conditional compilation, scripts, platform-specific files, and surrounding code. Do not invent a target from assumptions.

If the same code is compiled to several targets, choose a solution already verified across those targets or isolate target-specific behavior explicitly.

## 2. Do Not Assume Browser DOM Outside H5

Browser-only APIs include patterns such as:

```js
window.addEventListener('resize', handleResize)
document.querySelector('.panel')
element.getBoundingClientRect()
```

These must not be copied into App/mini-program code merely because they are valid in normal Vue Web applications.

For non-H5 targets:

- reuse the project's existing uni-app/platform abstraction
- use supported uni/platform APIs when required
- isolate H5-only behavior with the project's established conditional-compilation strategy when the feature is intentionally platform-specific

Do not add a browser polyfill or DOM abstraction as an incidental fix.

## 3. Networking: Verify Compatibility Instead of Assuming Incompatibility

Do **not** use this simplistic rule:

```text
H5 -> Axios
App/mini-program -> uni.request
```

That is too strict.

Axios can be a normal choice in uni-app when the actual target/project setup supports it. A mini-program target by itself is not proof that Axios is unusable.

Prefer this decision order:

1. **Existing project request layer** — if the project already has a working Axios-based `request` wrapper on the target, keep using it.
2. **Verified Axios on the target** — for a single-target App/mini-program project, Axios can remain the preferred transport when the required request features work correctly.
3. **Existing `uni.request` wrapper** — keep it when the project already standardizes on it.
4. **`uni.request` fallback/platform transport** — use it when there is a concrete compatibility gap or a uni-specific capability is required.

Use `uni.request` / a wrapper around it when, for example:

- the current Axios setup actually fails on the target
- an Axios adapter/runtime feature required by the project is unavailable or unreliable
- the request needs uni-app/platform-specific options or `RequestTask` capabilities that the current Axios layer does not expose correctly
- upload/download/network behavior depends on target-specific uni APIs
- one shared implementation must cover several targets and the Axios setup has not been verified across all of them

Do **not** install an Axios adapter solely because the project is uni-app. First check whether the existing Axios version/setup already works for the actual target and required features.

Conversely, do not replace a working Axios request architecture with raw `uni.request` simply to appear more cross-platform.

The request layering rules in `async-interface-ui.md` still apply. When Axios is used, prefer:

```text
utils/request.js -> api/<feature>.js -> page/component
```

When `uni.request` is used, keep the same separation through a project-owned request wrapper where practical.

## 4. Template Refs Are Platform-Sensitive

A normal browser Vue example may expect a template ref to expose a DOM element:

```vue
<script setup>
import { onMounted, useTemplateRef } from 'vue'

const inputRef = useTemplateRef('input')

onMounted(() => {
    inputRef.value?.focus()
})
</script>
```

Do not assume this object shape on non-H5 uni-app targets. Before calling DOM/element methods from a ref, verify that the target actually exposes the required capability.

## 5. Vue Built-ins Require a Platform Gate

Do not treat these as universally portable in uni-app:

- dynamic `<component :is="...">`
- `<Transition>`
- `<TransitionGroup>`
- `<KeepAlive>`
- `<Teleport>`
- `<Suspense>`

Their availability differs by target and runtime version. Therefore:

1. Check current target/runtime support.
2. Reuse an existing project pattern if one already solves the problem.
3. Do not import a Web Vue architecture into a cross-platform feature merely because the source syntax compiles as Vue.

The optional feature references in this Skill are Web Vue guidance unless this platform gate confirms applicability.

## 6. uni-app Page Routing Is Not Ordinary Vue Router Routing

Normal uni-app pages are registered/configured through `pages.json`, and navigation uses the project's uni-app navigation pattern / `uni.*` routing APIs.

Do not introduce patterns such as:

```vue
<RouterView />
```

or browser Vue Router guards/routes into an ordinary uni-app page flow unless the existing project explicitly has an H5-specific/custom routing architecture that requires them.

When adding a new page, first follow the project's existing `pages.json` / subpackage organization and navigation conventions.

## 7. Preserve Cross-Platform CSS Assumptions

Do not assume every browser CSS behavior, unit, selector, or layout trick works identically on every uni-app target.

When editing cross-platform UI:

- prefer existing project layout/style conventions
- avoid adding Web-only CSS solely because it works in H5 preview
- verify platform-specific behavior when the feature depends on unsupported or unusual CSS
- do not add a CSS/UI dependency to mask a platform mismatch without explicit architectural approval

## 8. Async Prompt Ordering

For asynchronous uni-app UI flows, load `async-interface-ui.md`.

When a request uses both native loading and a toast, the required order is:

```text
request success/failure
    -> uni.hideLoading()
    -> uni.showToast(...)
    -> Promise .finally()
        -> release reactive/business loading lock
```

Do not put the only `uni.hideLoading()` after the toast in `.finally()`.

## 9. Platform Compatibility Overrides Generic References

If another reference conflicts with this platform gate, **this platform gate wins for uni-app**.

Examples:

- `sfc.md` DOM-ref example -> H5/browser only unless target support is confirmed
- `composables.md` window event example -> H5/browser only
- `async-interface-ui.md` Axios architecture -> valid in uni-app when the actual target/project Axios layer is compatible
- `component-transition.md` -> load only when target supports the transition built-in
- `component-keep-alive.md` -> load only when target supports the built-in and the architecture actually needs it
- `component-teleport.md` -> verify target support before use
- `component-suspense.md` -> experimental plus platform-sensitive; never assume availability

## 10. Dependency Discipline Still Applies

Pinia remains an approved Vue ecosystem state solution when the project needs app-level shared state and the target/project setup supports it.

Axios is also an approved request-layer dependency in uni-app **when the actual target compatibility is verified**. The platform gate is not an Axios ban; it only prevents assuming compatibility where the runtime/network features are known to differ.

Other new compatibility packages or adapters remain explicit architecture choices. Use them only when a real compatibility requirement justifies them.
