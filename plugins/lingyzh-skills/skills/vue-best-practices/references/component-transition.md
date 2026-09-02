---
title: Transition Component Guidance
impact: MEDIUM
impactDescription: Transition is useful for intentional enter/leave motion on supported targets; animation choices should follow project motion conventions
type: best-practice
tags: [vue3, transition, animation, keys, platform]
---

# Transition Component Guidance

Use `<Transition>` for intentional enter/leave or single-view swap motion when the target platform supports it.

## Task List

- Confirm platform support first in uni-app
- Use one direct transition child
- Add stable keys when identity changes must trigger a swap
- Use `mode="out-in"` only when sequential replacement is desired
- Prefer motion properties that do not force expensive layout when practical
- Reuse project motion durations/easing instead of inventing Skill-provided values
- Do not animate UI solely because Transition is available

## Single Child

```vue
<template>
    <Transition name="fade">
        <section v-if="isVisible">
            <h3>Title</h3>
            <p>Description</p>
        </section>
    </Transition>
</template>
```

## Identity During Swaps

```vue
<template>
    <Transition
        name="fade"
        mode="out-in"
    >
        <p
            v-if="isActive"
            key="active"
        >
            Active
        </p>

        <p
            v-else
            key="inactive"
        >
            Inactive
        </p>
    </Transition>
</template>
```

Use a key only when the UI should be treated as a different identity. Do not add keys blindly to force remounting.

## Motion CSS

Prefer the project's existing motion tokens/variables when available.

```css
.fade-enter-active,
.fade-leave-active {
    transition:
        opacity var(--motion-duration) var(--motion-easing),
        transform var(--motion-duration) var(--motion-easing);
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
    transform: translateY(var(--motion-distance));
}
```

The variable names are placeholders for project-owned conventions, not a requirement to introduce a design-system dependency.

## Platform Gate

For uni-app, load `uni-app-platform.md` first. Transition support differs between H5/App/mini-program targets, so Web Vue examples must not be copied into unsupported builds.
