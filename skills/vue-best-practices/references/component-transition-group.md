---
title: TransitionGroup Component Guidance
impact: MEDIUM
impactDescription: TransitionGroup animates keyed collection changes on supported targets; it should not introduce arbitrary timing or platform assumptions
type: best-practice
tags: [vue3, transition-group, animation, lists, keys, platform]
---

# TransitionGroup Component Guidance

Use `<TransitionGroup>` when individual keyed list items need enter/leave/move animation and the target runtime supports the component.

## Task List

- Confirm platform support first in uni-app
- Use stable keys that represent item identity
- Use `tag` only when a wrapper element is actually required
- Do not use the `<Transition>` `mode` prop on TransitionGroup
- Reuse the project's motion timing/easing conventions
- Avoid JavaScript stagger logic unless the product explicitly needs it

## Keyed List

```vue
<template>
    <TransitionGroup
        name="list"
        tag="ul"
    >
        <li
            v-for="item in items"
            :key="item.id"
        >
            {{ item.name }}
        </li>
    </TransitionGroup>
</template>
```

Do not use an array index as the key when list insertion/removal/reordering can occur and a stable item identity exists.

## Motion CSS

```css
.list-enter-active,
.list-leave-active,
.list-move {
    transition:
        opacity var(--motion-duration) var(--motion-easing),
        transform var(--motion-duration) var(--motion-easing);
}

.list-enter-from,
.list-leave-to {
    opacity: 0;
    transform: translateY(var(--motion-distance));
}
```

Use project-owned tokens/variables or existing animation classes. Do not copy arbitrary millisecond values from a Skill example.

## Staggered Motion

If staggered animation is an explicit product requirement, use the simplest existing project animation mechanism that supports it. Do not introduce a JavaScript animation package or complex timeout choreography solely because TransitionGroup supports JS hooks.

## Platform Gate

For uni-app, load `uni-app-platform.md` first. TransitionGroup support differs by target and should be treated as Web Vue guidance until compatibility is confirmed.
