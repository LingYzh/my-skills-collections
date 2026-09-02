---
title: uni-app Platform Compatibility Gate
impact: HIGH
impactDescription: uni-app compiles Vue code to multiple runtimes whose component, DOM, routing, and platform capabilities differ materially
type: platform-gate
tags: [vue3, uni-app, h5, app, mini-program, platform, compatibility, routing, dom]
---

# uni-app Platform Compatibility Gate

Load this reference for **every uni-app task before applying browser-oriented Vue guidance**.

A `.vue` file in uni-app is not evidence that browser DOM APIs, Vue Router patterns, or every Vue built-in component is available on the target runtime.

## Task List

- Identify the actual build target(s) before selecting Vue APIs
- Treat H5/Web, App, and mini-program targets as different runtimes
- Do not assume `window`, `document`, browser DOM nodes, or browser event APIs outside H5
- Do not introduce Vue Router / `RouterView` patterns into ordinary uni-app page routing
- Check target support before using dynamic components, transition built-ins, keep-alive, teleport, suspense, or DOM-oriented template refs
- Prefer uni-app/project-native navigation and platform APIs when the target requires them
- Preserve multi-platform compatibility when the feature is shared across targets
- Apply `async-interface-ui.md` for `uni.showLoading()` / `uni.showToast()` ordering

## 1. Identify the Target First

Before implementing a platform-sensitive feature, determine whether the project/feature targets:

- H5 / Web
- App
- WeChat mini program
- another mini-program target
- multiple targets from the same source

Look at the project's existing configuration, conditional compilation, scripts, platform-specific files, and surrounding code. Do not invent a target from assumptions.

If the same code is compiled to several targets, choose the portable solution first or isolate platform-specific behavior explicitly.

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

Do not add a browser polyfill or third-party DOM abstraction as an incidental fix.

## 3. Template Refs Are Platform-Sensitive

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

Do not assume this object shape on non-H5 uni-app targets. Official uni-app compatibility documentation notes that non-H5 refs have different access limitations, especially for built-in/native components.

Before calling DOM/element methods from a ref, verify that the target actually exposes the required capability.

## 4. Vue Built-ins Require a Platform Gate

Do not treat these as universally portable in uni-app:

- dynamic `<component :is="...">`
- `<Transition>`
- `<TransitionGroup>`
- `<KeepAlive>`
- `<Teleport>`
- `<Suspense>`

Their availability differs by target and runtime version. Some are H5-only on common uni-app targets; some are supported only by selected mini-program runtimes; experimental Vue features can have additional limitations.

Therefore:

1. Check the current target/runtime support.
2. Reuse an existing project pattern if one already solves the problem.
3. Do not import a Web Vue architecture into a cross-platform feature merely because the source syntax compiles as Vue.

The optional feature references in this Skill are **Web Vue guidance unless this platform gate confirms applicability**.

## 5. uni-app Page Routing Is Not Ordinary Vue Router Routing

Normal uni-app pages are registered/configured through `pages.json`, and navigation uses the project's uni-app navigation pattern / `uni.*` routing APIs.

Do not introduce patterns such as:

```vue
<RouterView />
```

or browser Vue Router guards/routes into an ordinary uni-app page flow unless the existing project explicitly has an H5-specific/custom routing architecture that requires them.

When adding a new page, first follow the project's existing `pages.json` / subpackage organization and navigation conventions.

## 6. Preserve Cross-Platform CSS Assumptions

Do not assume every browser CSS behavior, unit, selector, or layout trick works identically on every uni-app target.

When editing cross-platform UI:

- prefer existing project layout/style conventions
- avoid adding Web-only CSS solely because it works in H5 preview
- verify platform-specific behavior when the feature depends on unsupported or unusual CSS
- do not add a CSS/UI dependency to mask a platform mismatch without explicit architectural approval

## 7. Async Prompt Ordering

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

## 8. Platform Compatibility Overrides Generic References

If another reference conflicts with this platform gate, **this platform gate wins for uni-app**.

Examples:

- `sfc.md` DOM-ref example -> H5/browser only unless target support is confirmed
- `composables.md` window event example -> H5/browser only
- `component-transition.md` -> load only when target supports the transition built-in
- `component-keep-alive.md` -> load only when target supports the built-in and the architecture actually needs it
- `component-teleport.md` -> verify target support before use
- `component-suspense.md` -> experimental plus platform-sensitive; never assume availability

## 9. Dependency Discipline Still Applies

Platform incompatibility is **not automatic permission to install a compatibility package**.

Prefer, in order:

1. capabilities already provided by uni-app / the target platform
2. abstractions already present in the project
3. a simple platform-specific implementation when necessary
4. a new dependency only as an explicit architectural choice with a concrete benefit

Third-party-specific patterns belong in a dedicated Skill or project documentation, not in this generic Vue/uni-app compatibility reference.
