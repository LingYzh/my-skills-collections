---
title: Reactivity Core Patterns (ref, reactive, shallowRef, computed, watch)
impact: HIGH
impactDescription: Clear reactivity choices keep state predictable and avoid both accidental deep tracking and unnecessary complexity
type: best-practice
tags: [vue3, reactivity, ref, reactive, shallowRef, computed, watch, watchEffect, external-state, best-practice]
---

# Reactivity Core Patterns

Use the simplest reactive primitive that matches the data shape and update pattern. Do not micro-optimize ordinary primitive state.

## Task List

- Use `ref()` as the normal default for primitive values and ordinary replaceable state
- Use `reactive()` when an object is primarily mutated in place
- Use `shallowRef()` only when deep reactivity is intentionally unwanted or materially expensive
- Avoid destructuring directly from `reactive()` when reactivity must be preserved
- Prefer `computed()` for derived state
- Keep computed getters pure
- Use watchers for side effects, synchronization, and request orchestration
- Clean up stale asynchronous watcher work when inputs change rapidly

## Choose the Reactive Primitive by Behavior

### `ref()` — normal default

Use `ref()` for primitive state and for ordinary values that are replaced as a whole.

```js
import { ref } from 'vue'

const count = ref(0)
const query = ref('')
const isOpen = ref(false)
const selectedUser = ref(null)
```

Do **not** replace primitive `ref()` values with `shallowRef()` merely for theoretical performance. Primitive values do not contain a nested object graph to deep-convert.

For object/array values, `ref()` is also appropriate when root replacement is common and nested mutations should remain reactive:

```js
const user = ref({
    name: 'Alice',
    age: 30
})

user.value.age = 31
user.value = {
    name: 'Bob',
    age: 25
}
```

### `reactive()` — mutation-oriented object state

Use `reactive()` when a cohesive object is mainly updated by mutating its properties and replacing the entire object is uncommon.

```js
import { reactive } from 'vue'

const form = reactive({
    name: '',
    email: '',
    submitting: false
})

form.name = 'Alice'
form.submitting = true
```

Avoid designs that require repeatedly replacing the `reactive()` root. If root replacement is the natural operation, use `ref()` instead.

### `shallowRef()` — intentionally shallow or opaque state

Use `shallowRef()` when nested values should remain raw and only root replacement should trigger updates.

Typical cases:

- large deeply nested data where immutable/root-replacement updates are used
- external SDK/client/class instances that should not be proxied
- editor/chart/map/media handles or other opaque objects
- integration with an external state system that already owns nested reactivity

```js
import { shallowRef } from 'vue'

const externalInstance = shallowRef(null)
const largeSnapshot = shallowRef([])

largeSnapshot.value = nextSnapshot
```

Do not mutate nested data and expect a shallow ref to trigger an update:

```js
const user = shallowRef({
    name: 'Alice',
    age: 30
})

user.value.age = 31 // does not trigger a shallow-ref update

user.value = {
    name: 'Alice',
    age: 31
} // root replacement triggers the update
```

### `shallowReactive()` — rare root-only container

Use `shallowReactive()` only when root properties should be reactive while nested objects intentionally remain raw.

```js
import { shallowReactive } from 'vue'

const state = shallowReactive({
    status: 'idle',
    payload: {
        items: []
    }
})

state.status = 'ready'
```

Avoid mixing shallow and deep reactive structures without a clear reason because inconsistent nested behavior makes maintenance harder.

## Preserve Reactivity When Accessing `reactive()` State

Direct destructuring disconnects primitive properties from the reactive proxy.

**BAD:**

```js
import { reactive } from 'vue'

const state = reactive({
    count: 0
})

const { count } = state
```

When a destructured ref is actually useful, use `toRefs()` / `toRef()` deliberately:

```js
import { reactive, toRefs } from 'vue'

const state = reactive({
    count: 0
})

const { count } = toRefs(state)
```

Do not introduce `toRefs()` automatically when direct property access is already clearer.

## Prefer `computed()` for Derived State

Do not maintain duplicated derived state with a watcher when it can be expressed directly.

**BAD:**

```js
import { ref, watchEffect } from 'vue'

const items = ref([
    { price: 10 },
    { price: 20 }
])
const total = ref(0)

watchEffect(() => {
    total.value = items.value.reduce((sum, item) => sum + item.price, 0)
})
```

**GOOD:**

```js
import { computed, ref } from 'vue'

const items = ref([
    { price: 10 },
    { price: 20 }
])

const total = computed(() => {
    return items.value.reduce((sum, item) => sum + item.price, 0)
})
```

### Keep filtering and sorting out of templates when it is non-trivial

```vue
<script setup>
import { computed, ref } from 'vue'

const items = ref([
    { id: 1, name: 'B', active: true },
    { id: 2, name: 'A', active: false }
])

const visibleItems = computed(() => {
    return items.value
        .filter((item) => item.active)
        .toSorted((a, b) => a.name.localeCompare(b.name))
})
</script>

<template>
    <li
        v-for="item in visibleItems"
        :key="item.id"
    >
        {{ item.name }}
    </li>
</template>
```

Avoid turning every tiny expression into a computed property. Extract it when the expression is reused, non-trivial, expensive, or materially clearer outside the template.

## Keep Computed Getters Pure

Computed values are derivations, not side-effect hooks.

**BAD:**

```js
const doubled = computed(() => {
    if (count.value > 10) {
        console.warn('Too big')
    }

    return count.value * 2
})
```

**GOOD:**

```js
const doubled = computed(() => count.value * 2)

watch(count, (value) => {
    if (value > 10) {
        console.warn('Too big')
    }
})
```

No API calls, persistence writes, event emits, or unrelated mutations inside computed getters.

## Watch Reactive Sources Correctly

Pass a ref, reactive object, getter, or array of supported sources to `watch()`.

**BAD:**

```js
watch(state.count, () => {
    // ...
})
```

**GOOD:**

```js
watch(() => state.count, (count) => {
    // ...
})
```

Use `immediate: true` when the same watcher logic genuinely needs an initial run:

```js
watch(
    userId,
    (id) => {
        loadUser(id)
    },
    {
        immediate: true
    }
)
```

Do not use `immediate: true` merely to avoid writing clearer initialization code when the initial action and later reaction have different responsibilities.

## Clean Up Stale Async Watcher Work

Rapidly changing sources such as search input can make older requests obsolete. Cancel or invalidate stale work when the underlying API supports it.

Browser-only example with a cancellable request:

```js
watch(query, (value, _previousValue, onCleanup) => {
    const controller = new AbortController()

    onCleanup(() => {
        controller.abort()
    })

    fetch(`/api/search?q=${encodeURIComponent(value)}`, {
        signal: controller.signal
    })
        .then((response) => response.json())
        .then((data) => {
            results.value = data
        })
        .catch((error) => {
            if (error.name !== 'AbortError') {
                handleSearchError(error)
            }
        })
})
```

Platform-specific request cancellation differs. In uni-app or other non-browser targets, follow the target request API instead of assuming `AbortController`, `fetch`, or browser DOM behavior exists.
