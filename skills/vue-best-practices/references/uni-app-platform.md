---
title: uni-app Platform Compatibility Gate
impact: HIGH
impactDescription: uni-app compiles Vue code to multiple runtimes whose component, DOM, routing, networking, and platform capabilities differ materially
type: platform-gate
tags: [vue3, uni-app, h5, app, mini-program, platform, compatibility, routing, dom, request]
---

# uni-app Platform Compatibility Gate

Load this reference for **every uni-app task before applying browser-oriented Vue guidance**.

A `.vue` file in uni-app is not evidence that browser DOM APIs, Vue Router patterns, Axios/browser networking assumptions, or every Vue built-in component is available on the target runtime.

## Task List

- Identify the actual build target(s) before selecting Vue APIs
- Treat H5/Web, App, and mini-program targets as different runtimes
- Do not assume `window`, `document`, browser DOM nodes, XHR, or browser event APIs outside H5
- Do not introduce Vue Router / `RouterView` patterns into ordinary uni-app page routing
- Check target support before using dynamic components, transition built-ins, keep-alive, teleport, suspense, or DOM-oriented template refs
- Prefer `uni.request` / the project's existing cross-platform request wrapper for shared App/mini-program networking
- Use Axios in uni-app only for H5/Web-only code or when the project already has a tested compatible adapter/wrapper for all required targets
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

## 3. Networking Is Platform-Sensitive Too

Ordinary Web Vue can use browser-oriented HTTP clients such as Axios. Shared uni-app App/mini-program code should not assume a browser/XHR runtime.

For cross-platform uni-app networking, prefer:

1. the project's existing request wrapper if one is established
2. `uni.request` or a project wrapper around it
3. Axios only when the code is H5/Web-only or the project already has a tested adapter/wrapper compatible with every required target

Do not replace a working `uni.request` abstraction with Axios merely to standardize syntax.

Vue 3 uni-app APIs support Promise-style invocation, so chain-oriented request flow does not require Axios.

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

The optional feature references in this Skill are **Web Vue guidance unless this platform gate confirms applicability**.

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
- `async-interface-ui.md` Axios example -> Web Vue/H5 only unless project compatibility is already established
- `component-transition.md` -> load only when target supports the transition built-in
- `component-keep-alive.md` -> load only when target supports the built-in and the architecture actually needs it
- `component-teleport.md` -> verify target support before use
- `component-suspense.md` -> experimental plus platform-sensitive; never assume availability

## 10. Dependency Discipline Still Applies

Platform incompatibility is **not automatic permission to install a compatibility package**.

Prefer, in order:

1. capabilities already provided by uni-app / the target platform
2. abstractions already present in the project
3. a simple platform-specific implementation when necessary
4. a new dependency only as an explicit architectural choice with a concrete benefit

Pinia remains an approved Vue ecosystem state solution when the project needs app-level shared state and the target/project setup supports it.

Axios is an approved ordinary Web Vue HTTP client, but it is **not** a universal uni-app transport. In cross-platform uni-app networking, the platform gate overrides the generic Axios allowance.
