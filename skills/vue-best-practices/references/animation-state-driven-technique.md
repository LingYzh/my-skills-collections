---
title: State-driven Animation Guidance
impact: LOW
impactDescription: Reactive style/class bindings can drive simple interactive motion without introducing animation dependencies
type: best-practice
tags: [vue3, animation, css, style-binding, state, interactive, platform]
---

# State-driven Animation Guidance

Use reactive style/class bindings when visual state directly follows Vue state. Keep the animation mechanism as simple as the requirement allows.

## Task List

- Bind only the dynamic values that truly come from state
- Reuse project motion durations/easing/tokens
- Prefer transform/opacity when they satisfy the visual requirement
- Avoid high-frequency reactive writes when CSS/native behavior can handle the interaction
- Do not add an animation/tween library from this reference
- Treat mouse/scroll/DOM examples as H5/browser-specific
- Apply `uni-app-platform.md` before using browser event geometry in uni-app

## Basic State-driven Style

```vue
<script setup>
import { computed, ref } from 'vue'

const progress = ref(0)

const progressStyle = computed(() => {
    return {
        transform: `scaleX(${progress.value / 100})`
    }
})
</script>

<template>
    <div class="progress-track">
        <div
            class="progress-bar"
            :style="progressStyle"
        />
    </div>
</template>

<style scoped>
.progress-bar {
    transform-origin: left center;
    transition: transform var(--motion-duration) var(--motion-easing);
}
</style>
```

The variables represent existing project conventions, not packages/tokens that this Skill requires you to add.

## Browser-only Pointer Example

```vue
<script setup>
import { ref } from 'vue'

const x = ref(0)
const y = ref(0)

function handlePointerMove(event) {
    const rect = event.currentTarget.getBoundingClientRect()

    x.value = event.clientX - rect.left
    y.value = event.clientY - rect.top
}
</script>

<template>
    <div
        class="interactive-area"
        @pointermove="handlePointerMove"
    >
        <div
            class="follower"
            :style="{
                transform: `translate(${x}px, ${y}px)`
            }"
        />
    </div>
</template>
```

This relies on browser DOM geometry and pointer events. Do not copy it into uni-app App/mini-program code without a target-specific implementation.

## Avoid Framework-side Tweening by Default

Do not reach for a watcher plus an animation library merely to interpolate a number. First consider:

- CSS transition/animation
- native/platform animation capability already used by the project
- an existing project animation abstraction

If a specialized animation engine is genuinely required, that dependency choice belongs to the project architecture or a dedicated Skill, not this generic Vue reference.

## High-frequency Input

For scroll/pointer/drag-driven effects, avoid assuming every event should update Vue reactive state at full frequency. Use the project's established performance pattern and profile the actual target.

Browser APIs such as `window.scrollY`, `requestAnimationFrame`, and direct DOM geometry are platform-specific and require the uni-app gate outside H5.
