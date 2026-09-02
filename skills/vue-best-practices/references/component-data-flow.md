---
title: Component Data Flow Best Practices
impact: HIGH
impactDescription: Explicit ownership and communication boundaries prevent hidden coupling without forcing unnecessary abstraction
type: best-practice
tags: [vue3, props, emits, v-model, provide-inject, data-flow, javascript, jsdoc, typescript]
---

# Component Data Flow Best Practices

Use the simplest communication mechanism that keeps state ownership obvious. Props down / events up is the normal default, not a rule that forbids every other Vue mechanism.

## Task List

- Treat props as read-only inputs
- Use props/events for ordinary parent-child communication
- Use `v-model` for intentional two-way component contracts
- Use component refs only for genuinely imperative APIs
- Use provide/inject for contextual dependencies that would otherwise be mechanically forwarded through unrelated intermediates
- Keep shared mutations owned by the provider or exposed through explicit actions when useful
- Express contracts according to the selected JS / JSDoc / TS stability tier
- Do not migrate component architecture as part of an unrelated edit

## Props Are Read-Only Inputs

**BAD:**

```vue
<script setup>
const props = defineProps({
    count: Number
})

function increment() {
    props.count += 1
}
</script>
```

Prefer an event, an intentional `v-model` contract, or a local derived/copy value depending on ownership.

## Prefer Props and Events for Ordinary Parent-Child Flow

```vue
<!-- Child.vue -->
<script setup>
const emit = defineEmits(['save'])

function save(formData) {
    emit('save', formData)
}
</script>
```

```vue
<!-- Parent.vue -->
<script setup>
function handleSave(formData) {
    submitForm(formData)
}
</script>

<template>
    <Child @save="handleSave" />
</template>
```

Component events do not automatically bubble through arbitrary ancestor levels. Re-emit only when that component is intentionally part of the event contract; do not build long chains of pass-through events when the data actually belongs to a broader context.

## Use `v-model` for Real Two-Way Contracts

On modern Vue versions, `defineModel()` is appropriate when the child represents an editable value owned by the parent.

```vue
<script setup>
const model = defineModel({
    type: String
})
</script>

<template>
    <input v-model="model" />
</template>
```

Do not introduce `v-model` merely to avoid writing one explicit event when the relationship is not conceptually two-way.

For older Vue versions, follow the project's existing `modelValue` / `update:modelValue` convention rather than rewriting unrelated components.

## Keep Imperative Component Refs Narrow

Use a component ref when the parent genuinely needs to call an imperative child API such as focus, open, close, reset, or scroll.

```vue
<!-- DialogPanel.vue -->
<script setup>
function open() {
    // ...
}

defineExpose({
    open
})
</script>
```

```vue
<!-- Parent.vue -->
<script setup>
import { onMounted, useTemplateRef } from 'vue'

const panelRef = useTemplateRef('panelRef')

onMounted(() => {
    panelRef.value?.open()
})
</script>

<template>
    <DialogPanel ref="panelRef" />
</template>
```

Expose only the intended imperative surface. Do not convert a JavaScript component to TypeScript solely because one template ref exists.

### Platform gate for element refs

Browser DOM assumptions do not automatically apply to uni-app targets. In non-H5 uni-app builds, template refs can have different capabilities and may not expose native/built-in elements like browser DOM nodes. Load `uni-app-platform.md` before writing DOM-oriented ref logic for uni-app.

## Use Provide/Inject for Context, Not a Layer Count

Do **not** use a magic threshold such as “more than three component layers”. The real signal is whether intermediate components are being forced to forward data/actions they do not otherwise care about.

Good provide/inject candidates include:

- form or field-group context
- theme/config context
- feature-level services/actions used by descendants
- parent-controlled compound component context

Avoid provide/inject when a direct prop/event relationship is already clear and local.

```js
import { inject, provide, readonly } from 'vue'

const themeKey = Symbol('theme')
const themeActionsKey = Symbol('theme-actions')

const theme = reactive({
    dark: false
})

function toggleTheme() {
    theme.dark = !theme.dark
}

provide(themeKey, readonly(theme))
provide(themeActionsKey, {
    toggleTheme
})
```

Use symbol keys when collision resistance or library-like isolation is useful. For very small local contexts, do not add ceremony that makes the code harder to follow.

## Express Public Contracts According to Stability

### Tier A — Business / volatile JavaScript

Use runtime declarations that are quick to update with changing requirements.

```vue
<script setup>
const props = defineProps({
    userId: {
        type: String,
        required: true
    },
    editable: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits([
    'save',
    'cancel'
])
</script>
```

### Tier B — Shared / moderately stable JavaScript

Keep runtime declarations and add JSDoc only where a non-obvious shared contract benefits from it.

```js
/**
 * @typedef {{ id: string, draft: boolean }} SavePayload
 */

/**
 * @param {SavePayload} payload
 */
function save(payload) {
    emit('save', payload)
}
```

### Tier C — Foundation / stable TypeScript

Use type-based component contracts when the component is low-change, broadly reused, and contract breakage would affect many consumers.

```vue
<script setup lang="ts">
interface Props {
    userId: string
    editable?: boolean
}

interface Emits {
    save: [payload: { id: string, draft: boolean }]
    cancel: []
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()
</script>
```

Do not treat a typed contract as inherently more maintainable when the business contract itself is still changing quickly.

## Respect Existing Architecture During Maintenance

When editing existing code:

- keep the existing props/events/model/provide pattern if it is working and the task does not require architectural change
- do not replace refs with events, or events with provide/inject, solely because this reference describes another option
- do not migrate Options API to Composition API as an incidental refactor
- make architecture migration an explicit task with a concrete benefit
