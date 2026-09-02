---
title: Suspense Component Guidance
impact: MEDIUM
impactDescription: Suspense can coordinate async dependencies but remains experimental and should not become a default loading architecture
type: experimental-guidance
tags: [vue3, suspense, async-components, async-setup, loading, experimental]
---

# Suspense Component Guidance

`<Suspense>` is an **experimental Vue feature**. Do not introduce it as a generic best-practice replacement for explicit application loading states.

Load this reference only when the project already uses Suspense or the requirement explicitly calls for coordinated async dependency boundaries.

## Task List

- Confirm the target Vue/platform supports the required behavior
- Treat Suspense as opt-in experimental architecture
- Keep the boundary small and easy to remove
- Provide a clear fallback
- Do not replace ordinary button/form/API loading locks with Suspense
- Do not introduce router/transition/keep-alive nesting patterns solely because an example shows them
- In uni-app, load `uni-app-platform.md` first and do not assume browser Vue built-ins are portable

## Basic Boundary

```vue
<template>
    <Suspense>
        <AsyncPanel />

        <template #fallback>
            <PageLoadingState />
        </template>
    </Suspense>
</template>
```

Keep the default and fallback branches structurally clear. Avoid building deeply nested Suspense trees unless the application already relies on them and their behavior is understood.

## Re-Pending Behavior

After a boundary has resolved, fallback behavior for later changes depends on root replacement and timing. If the application depends on a specific re-pending UX, verify it against the Vue version actually used instead of relying on an old copied pattern.

```vue
<template>
    <Suspense :timeout="0">
        <component
            :is="currentView"
            :key="viewKey"
        />

        <template #fallback>
            <PageLoadingState />
        </template>
    </Suspense>
</template>
```

Do not choose a timeout from a Skill-provided magic number. Use the default or a product/UX requirement backed by actual behavior testing.

## Events

Suspense events can coordinate UI outside the boundary when that architecture already exists.

```vue
<script setup>
import { ref } from 'vue'

const isPending = ref(false)

function handlePending() {
    isPending.value = true
}

function handleResolve() {
    isPending.value = false
}
</script>

<template>
    <PageProgress v-if="isPending" />

    <Suspense
        @pending="handlePending"
        @resolve="handleResolve"
    >
        <AsyncPage />

        <template #fallback>
            <PageLoadingState />
        </template>
    </Suspense>
</template>
```

## Do Not Confuse Suspense with Interaction Locks

A Suspense fallback does not replace the explicit loading/disabled lock required for user-triggered asynchronous actions described in `async-interface-ui.md`.

Examples that still need their own business lock include:

- submit/save/delete buttons
- checkout/payment-like operations
- mutable forms during an in-flight save
- actions where duplicate requests or state changes can conflict

## Platform Gate

Before using Suspense in uni-app or another compiled multi-platform target:

1. Identify the actual target (H5/Web, App, mini program, etc.).
2. Check that the built-in is supported by that target/runtime.
3. Prefer the target's established loading architecture when compatibility is uncertain.

Do not assume a browser Vue example is portable merely because the source file is `.vue`.

## Production Rule

Because Suspense is experimental, introducing it to production code should be an explicit architectural choice. Do not add it during an unrelated refactor, and do not make other components depend on it unless the requirement justifies that coupling.
