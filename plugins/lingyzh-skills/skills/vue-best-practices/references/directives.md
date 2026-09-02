---
title: Custom Directive Guidance
impact: MEDIUM
impactDescription: Directives are low-level element behavior and should stay small, local, and compatible with the actual rendering target
type: best-practice
tags: [vue3, directives, custom-directives, dom, platform]
---

# Custom Directive Guidance

Use a custom directive for a small piece of low-level element behavior that fits poorly as a normal prop/component/composable API.

## Task List

- Use directives sparingly
- Treat binding values/arguments as inputs, not mutable storage
- Clean up listeners, timers, observers, or other resources in `unmounted`
- Prefer declarative attributes/bindings when they already express the behavior
- Do not enable TypeScript solely for a directive
- Treat DOM-oriented directives as browser guidance unless the target exposes equivalent element behavior
- In uni-app, load `uni-app-platform.md` first

## Small Directive

```vue
<script setup>
const vFocus = {
    mounted(element) {
        element.focus()
    }
}
</script>

<template>
    <input v-focus />
</template>
```

This example assumes the runtime exposes an element with a browser-style `focus()` method. Do not assume that on uni-app non-H5 targets.

## Cleanup

```js
const vClickOutside = {
    mounted(element, binding) {
        function handlePointerDown(event) {
            if (!element.contains(event.target)) {
                binding.value(event)
            }
        }

        element.__handlePointerDown = handlePointerDown
        document.addEventListener('pointerdown', handlePointerDown)
    },

    unmounted(element) {
        document.removeEventListener(
            'pointerdown',
            element.__handlePointerDown
        )

        delete element.__handlePointerDown
    }
}
```

This is explicitly browser-only. A cross-platform project should use a platform-compatible existing pattern instead of adding a DOM shim.

## Avoid Directives on Component Roots for Hidden DOM Coupling

A directive attached to a component can depend on that component's current root element. Prefer an explicit component API when the behavior is really part of the component contract.

## Directives vs Other Abstractions

- attribute/binding -> simple declarative element state
- directive -> small low-level element behavior
- component -> owns UI structure/interaction contract
- composable -> reusable state/lifecycle logic without rendered structure

Choose the simplest mechanism that matches ownership. Do not migrate working code merely to replace one abstraction with another.

## Stability Tier

JavaScript is appropriate for ordinary Tier A/B directives. Use TypeScript only when a stable Tier C directive API materially benefits from a typed public contract.
