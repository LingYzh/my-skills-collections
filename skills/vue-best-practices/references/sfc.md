---
title: Single-File Component Structure, Styling, and Template Patterns
impact: MEDIUM
impactDescription: Consistent SFC structure, appropriate language choice, and platform-aware template patterns improve maintainability
type: best-practice
tags: [vue3, sfc, javascript, typescript, jsdoc, scoped-css, styles, template, v-html, v-for, computed, v-if, v-show, uni-app]
---

# Single-File Component Structure, Styling, and Template Patterns

Use Vue SFCs as the normal component format in build-based Vue projects. Keep language, styling, and platform assumptions aligned with the component's real responsibility.

## Task List

- Keep template, script, and component-local styles together in the SFC by default
- Choose JS / JS + JSDoc / TS according to the main Skill's stability tiers
- Use four-space indentation in all SFC sections
- Use PascalCase component filenames and component tags unless the existing project has an explicit incompatible convention
- Keep templates declarative and extract non-trivial derivation to script
- Prefer component-scoped styling for application components
- Prefer stable class-based or module-based style contracts for reusable foundation/library components when external override is expected
- Use stable primitive keys in `v-for`
- Avoid `v-if` and `v-for` on the same element
- Never render untrusted HTML without an existing trusted sanitization boundary
- Choose `v-if` vs `v-show` based on lifecycle and toggle behavior
- Apply the uni-app platform gate before using DOM-specific assumptions

## Choose Script Language by Stability

### Business / volatile

```vue
<script setup>
const draft = ref('')
</script>
```

### Shared / moderately stable

Use JavaScript and add JSDoc only where a shared boundary materially benefits from it.

```vue
<script setup>
/**
 * @typedef {{ id: string, label: string }} Option
 */

const props = defineProps({
    options: {
        type: Array,
        required: true
    }
})
</script>
```

### Foundation / stable contract

```vue
<script setup lang="ts">
interface Props {
    modelValue: string | number | null
    disabled?: boolean
}

defineProps<Props>()
</script>
```

Do not change a file's language as an incidental refactor.

## Keep SFC Concerns Colocated by Default

**GOOD:**

```vue
<script setup>
import { computed } from 'vue'

const props = defineProps({
    user: {
        type: Object,
        required: true
    }
})

const displayName = computed(() => {
    return `${props.user.firstName} ${props.user.lastName}`
})
</script>

<template>
    <article class="user-card">
        <h3 class="user-card__name">
            {{ displayName }}
        </h3>
    </article>
</template>

<style scoped>
.user-card {
    padding: 1rem;
}

.user-card__name {
    margin: 0;
}
</style>
```

Separate files only when there is a concrete reason such as a shared stylesheet, generated code, or an intentionally reusable plain module.

## Component Naming

Prefer PascalCase for component filenames and imported component names.

```vue
<script setup>
import UserProfile from './UserProfile.vue'
</script>

<template>
    <UserProfile :user="currentUser" />
</template>
```

Do not rename an established component tree solely to enforce naming during an unrelated maintenance task.

## Styling Strategy Follows Component Responsibility

### Application/business components

Component-scoped styling is a good default when styles are local implementation details.

```vue
<style scoped>
.profile-card {
    display: grid;
    gap: 1rem;
}
</style>
```

Prefer class selectors over broad element selectors in scoped styles.

### Foundation/library-style components

When a broadly reused component intentionally exposes styling hooks to consumers, prefer the project's established stable class convention, CSS modules, design tokens, or another explicit style contract instead of assuming `<style scoped>` is always best.

The goal is predictable override behavior, not one universal CSS mechanism.

### Global styles

Keep resets, application-wide tokens, typography foundations, and truly global rules in the project's established global style entry.

Do not create a new styling dependency because an example mentions a technique.

## Template Refs Are Platform-Sensitive

On browser Vue 3.5+, `useTemplateRef()` is a clear way to access template refs.

```vue
<script setup>
import { onMounted, useTemplateRef } from 'vue'

const inputRef = useTemplateRef('input')

onMounted(() => {
    inputRef.value?.focus()
})
</script>

<template>
    <input ref="input" />
</template>
```

This is a **browser DOM example**. In uni-app non-H5 targets, refs can expose different objects/capabilities. Load `uni-app-platform.md` before using DOM methods such as `focus()`, `getBoundingClientRect()`, or direct element mutation.

Do not enable TypeScript solely for a template ref.

## Keep Style Bindings Readable

Use camelCase property keys in object-style bindings unless the existing codebase has another clear convention.

```vue
<template>
    <div :style="{ fontSize: fontSize + 'px', backgroundColor: background }">
        Content
    </div>
</template>
```

If a style expression becomes large or is reused, move it to a computed value. Do not extract trivial one-off bindings only to satisfy abstraction rules.

## Use Stable Keys in `v-for`

Prefer stable primitive IDs or other stable primitive values.

```vue
<template>
    <li
        v-for="item in items"
        :key="item.id"
    >
        {{ item.name }}
    </li>
</template>
```

Avoid using object identity or an unstable/random value as the key.

## Avoid `v-if` and `v-for` on the Same Element

For filtered lists, derive the list first when filtering is non-trivial.

```vue
<script setup>
import { computed } from 'vue'

const activeUsers = computed(() => {
    return users.value.filter((user) => user.active)
})
</script>

<template>
    <li
        v-for="user in activeUsers"
        :key="user.id"
    >
        {{ user.name }}
    </li>
</template>
```

To conditionally show the entire list, place the condition on a parent/container instead.

## Treat `v-html` as a Trust Boundary

Never put untrusted/user-controlled HTML directly into `v-html`.

Prefer escaped interpolation whenever rich HTML is not required:

```vue
<template>
    <p>{{ userProvidedText }}</p>
</template>
```

If rich HTML is required, pass it through a **sanitization mechanism that already exists in the project** or a deliberately reviewed security boundary before rendering it.

```vue
<script setup>
import { computed } from 'vue'
import { sanitizeTrustedHtml } from '@/security/html'

const props = defineProps({
    html: {
        type: String,
        required: true
    }
})

const safeHtml = computed(() => {
    return sanitizeTrustedHtml(props.html)
})
</script>

<template>
    <article v-html="safeHtml" />
</template>
```

`sanitizeTrustedHtml` is a project-owned abstraction placeholder, **not a recommendation to install a package**. If no reviewed sanitizer exists and rich HTML is not an explicit requirement, do not invent one or add a dependency as an incidental change.

## Choose `v-if` vs `v-show` by Behavior

Use `v-show` when content is mounted safely and toggles frequently. Use `v-if` when conditional content is infrequent, expensive to mount initially, or should not exist while inactive.

```vue
<template>
    <FrequentlyToggledPanel v-show="isPanelOpen" />
    <RareAdminPanel v-if="isAdmin" />
</template>
```

This is a heuristic, not a reason to refactor working code without a measured or maintainability benefit.
