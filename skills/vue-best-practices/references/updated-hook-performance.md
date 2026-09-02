---
title: Avoid Expensive Work in Updated Hooks
impact: MEDIUM
impactDescription: Updated hooks run after component updates and are easy to misuse for broad side effects or feedback loops
type: capability
tags: [vue3, lifecycle, updated, performance, reactivity, platform]
---

# Avoid Expensive Work in Updated Hooks

Use `onUpdated()` only for post-render work that genuinely needs to observe the rendered result. Do not use it as a generic “something changed” callback.

## Task List

- Do not start ordinary API synchronization from `onUpdated()`
- Do not mutate reactive state unconditionally inside the hook
- Prefer `watch()` / `computed()` when the trigger is known reactive data
- Keep DOM/post-render work narrow and guarded
- Reuse an existing project debounce/throttle helper if rate limiting is required; do not install one from this reference
- Apply the uni-app platform gate before writing browser DOM synchronization

## Prefer a Targeted Watcher

If the behavior is triggered by a particular source value, watch that source directly.

```vue
<script setup>
import { ref, watch } from 'vue'

const items = ref([])

watch(
    items,
    (nextItems) => {
        queueSync(nextItems)
    },
    {
        deep: true
    }
)
</script>
```

If `queueSync()` performs an API request, it must follow `async-interface-ui.md` when the operation has user-visible/conflicting UI behavior.

## Do Not Mutate State Unconditionally in `onUpdated()`

**BAD:**

```vue
<script setup>
import { onUpdated, ref } from 'vue'

const renderCount = ref(0)

onUpdated(() => {
    renderCount.value += 1
})
</script>
```

That mutation can trigger another update and create a feedback loop.

## Valid Post-render Work

A narrow browser example:

```vue
<script setup>
import { onUpdated, useTemplateRef } from 'vue'

const listRef = useTemplateRef('list')

onUpdated(() => {
    const element = listRef.value

    if (!element) {
        return
    }

    maintainScrollPosition(element)
})
</script>

<template>
    <div ref="list">
        <slot />
    </div>
</template>
```

This is browser DOM-oriented. In uni-app non-H5 targets, load `uni-app-platform.md` and use a compatible project/platform approach instead.

## Derived Data Belongs in `computed()`

```js
const total = computed(() => {
    return numbers.value.reduce((sum, number) => {
        return sum + number
    }, 0)
})
```

Do not assign derived data from an update hook.

## Rate Limiting

If a legitimate watched/post-render operation is too frequent:

1. verify the operation itself is necessary
2. reduce the trigger scope first
3. reuse the project's existing throttle/debounce helper if one exists
4. add custom timing/dependencies only as an explicit requirement

This generic Skill intentionally does not recommend a debounce/throttle package or universal delay value.
