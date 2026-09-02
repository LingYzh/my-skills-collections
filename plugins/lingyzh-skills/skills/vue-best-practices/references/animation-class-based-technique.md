---
title: Class-based Animation Guidance
impact: LOW
impactDescription: State-controlled CSS classes are a simple way to animate mounted elements without adding JavaScript timing dependencies
type: best-practice
tags: [vue3, animation, css, class-binding, state, platform]
---

# Class-based Animation Guidance

For an element that stays mounted, a reactive class plus project-owned CSS animation is usually simpler than introducing component enter/leave transitions or an animation dependency.

## Task List

- Toggle animation classes from state
- Prefer `animationend` / `transitionend` when code must know when CSS motion ends
- Reuse project motion tokens/classes
- Avoid hard-coded timeout values that duplicate CSS duration
- Do not extract a reusable animation composable unless the behavior is genuinely reused
- Apply the uni-app platform gate when CSS/event support differs by target

## Basic Pattern

```vue
<script setup>
import { ref } from 'vue'

const invalidFeedback = ref(false)

function showInvalidFeedback() {
    invalidFeedback.value = true
}
</script>

<template>
    <div
        :class="{ 'form--invalid-feedback': invalidFeedback }"
        @animationend="invalidFeedback = false"
    >
        <button @click="showInvalidFeedback">
            Validate
        </button>
    </div>
</template>

<style scoped>
.form--invalid-feedback {
    animation: form-invalid var(--motion-duration) var(--motion-easing);
}

@keyframes form-invalid {
    from {
        opacity: 0.6;
    }

    to {
        opacity: 1;
    }
}
</style>
```

The CSS variables are placeholders for the project's existing motion convention. Do not add a motion/design dependency solely for this example.

## Prefer Events over Matching Timers

**Avoid:**

```js
isAnimating.value = true

setTimeout(() => {
    isAnimating.value = false
}, 820)
```

when the only reason for `820` is to mirror a CSS animation duration. CSS duration can change independently and make the timer stale.

Prefer the animation/transition completion event when supported by the target runtime.

## When a Timer Is Legitimate

A timer can still be correct when the **product behavior itself** has a duration independent of CSS, such as “keep success state visible for N seconds”. That duration should come from the product requirement/project constant, not an arbitrary value embedded by this Skill.

## Platform Gate

For uni-app, load `uni-app-platform.md` before assuming browser CSS animation events or DOM behavior are identical on every target.
