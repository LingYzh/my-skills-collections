---
title: Composable Organization Patterns
impact: MEDIUM
impactDescription: Composables are useful for coherent reusable or stateful concerns, but excessive extraction can make volatile business code harder to follow
type: best-practice
tags: [vue3, composables, composition-api, code-organization, api-design, readonly, utilities, javascript, jsdoc, typescript]
---

# Composable Organization Patterns

Use composables when they create a meaningful state/behavior boundary. Do not extract logic merely to make a component shorter or to satisfy an arbitrary line-count rule.

## Task List

- Extract a composable when logic is reused or forms a coherent stateful/lifecycle concern
- Keep rapidly changing one-off business orchestration close to the feature when extraction would increase navigation overhead
- Choose JS / JSDoc / TS according to stability tiers
- Use options objects when multiple optional arguments would otherwise be ambiguous
- Return readonly state only when mutation ownership genuinely needs enforcement
- Keep pure utilities as plain utilities
- Avoid hidden global state and hidden side effects
- Apply async request/loading rules from `async-interface-ui.md`

## When to Extract a Composable

Good reasons include:

- the same behavior is reused
- a coherent concern owns state plus lifecycle/side effects
- a browser/platform integration needs isolated setup and cleanup
- a complex feature concern becomes easier to reason about as one named unit
- the logic has an independently meaningful API

Weak reasons include:

- the component passed an arbitrary line count
- the script section “looks long”
- every group of three refs can be given a `useXxx` name
- a one-off business workflow is being split across files without reuse or conceptual separation

For volatile business code, locality can be more maintainable than abstraction.

## Choose Language by Stability

### Tier A — Feature / volatile

```js
// composables/useOrderEditor.js
import { ref } from 'vue'

export function useOrderEditor() {
    const draft = ref(null)
    const saving = ref(false)

    function reset() {
        draft.value = null
    }

    return {
        draft,
        saving,
        reset
    }
}
```

### Tier B — Shared / moderately stable

Use JavaScript and add JSDoc only at useful boundaries.

```js
/**
 * @typedef {Object} UseCounterOptions
 * @property {number} [initial]
 * @property {number} [min]
 * @property {number} [max]
 * @property {number} [step]
 */

/**
 * @param {UseCounterOptions} [options]
 */
export function useCounter(options = {}) {
    const {
        initial = 0,
        min = -Infinity,
        max = Infinity,
        step = 1
    } = options

    return {
        initial,
        min,
        max,
        step
    }
}
```

### Tier C — Foundation / stable contract

TypeScript is appropriate for a low-change, broadly reused composable with a mature public contract. Do not migrate a feature composable to TypeScript merely because a second consumer appears.

## Compose Only When the Smaller Pieces Are Meaningful

A low-level composable can be valuable when its lifecycle cleanup is reusable:

```js
import { onMounted, onUnmounted, toValue } from 'vue'

export function useEventListener(target, event, callback) {
    onMounted(() => {
        toValue(target)?.addEventListener(event, callback)
    })

    onUnmounted(() => {
        toValue(target)?.removeEventListener(event, callback)
    })
}
```

This example is browser-specific. In uni-app non-H5 targets, load `uni-app-platform.md` and do not assume `window`, DOM nodes, or DOM event APIs exist.

Do not decompose one feature into many tiny composables when each one is used once and understanding the feature then requires opening several files.

## Use Options Objects for Ambiguous Optional Arguments

**BAD:**

```js
useRequest('/api/users', 'POST', null, 5000, 3, true)
```

**GOOD:**

```js
useRequest('/api/users', {
    method: 'POST',
    timeout: 5000,
    retries: 3,
    immediate: true
})
```

Do not wrap a function in an options object when it has only one or two obvious required parameters.

## Readonly State Is an Ownership Tool

Use `readonly()` when consumers should observe state but mutation should stay behind explicit actions.

```js
import { computed, readonly, ref } from 'vue'

export function useCart() {
    const items = ref([])

    const total = computed(() => {
        return items.value.reduce((sum, item) => {
            return sum + item.price * item.quantity
        }, 0)
    })

    function addItem(product, quantity = 1) {
        const existing = items.value.find((item) => item.id === product.id)

        if (existing) {
            existing.quantity += quantity
            return
        }

        items.value.push({
            ...product,
            quantity
        })
    }

    return {
        items: readonly(items),
        total,
        addItem
    }
}
```

Do not add readonly/action ceremony to trivial local state where direct mutation is already clear and contained.

## Keep Pure Utilities as Utilities

**BAD:**

```js
export function useFormatters() {
    function formatDate(date) {
        return new Intl.DateTimeFormat('en-US').format(date)
    }

    return {
        formatDate
    }
}
```

**GOOD:**

```js
// utils/formatDate.js
export function formatDate(date) {
    return new Intl.DateTimeFormat('en-US').format(date)
}
```

A function is not a composable merely because it can be named `useXxx`.

## Keep Feature Logic Local Until a Boundary Helps

A single feature component can legitimately contain several related refs/computed/functions when they form one rapidly changing workflow.

Extract only when a coherent concern emerges.

```vue
<script setup>
import { computed, ref } from 'vue'

const searchQuery = ref('')
const selectedId = ref(null)

const visibleItems = computed(() => {
    return items.value.filter((item) => {
        return item.name.includes(searchQuery.value)
    })
})

function selectItem(id) {
    selectedId.value = id
}
</script>
```

This is not automatically a “mega component”. Component/composable extraction should follow responsibility boundaries and maintenance cost, not a fixed count of refs or UI sections.

## Async Work Inside Composables

When a composable owns an API/interface request, prefer the Promise-chain convention from `async-interface-ui.md` and keep operation state explicit.

```js
import { ref } from 'vue'

export function useItems() {
    const items = ref([])
    const loading = ref(false)

    function fetchItems() {
        if (loading.value) {
            return Promise.resolve()
        }

        loading.value = true

        return fetchItemsApi()
            .then((result) => {
                items.value = result
            })
            .catch((error) => {
                handleItemsError(error)
            })
            .finally(() => {
                loading.value = false
            })
    }

    return {
        items,
        loading,
        fetchItems
    }
}
```

A composable-level loading flag does not automatically disable UI. The consuming component must still apply the appropriate interaction lock when user actions could conflict.
