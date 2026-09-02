---
title: State Management Strategy
impact: HIGH
impactDescription: State scope should match ownership and runtime lifetime without introducing unnecessary dependencies or SSR leakage
type: best-practice
tags: [vue3, state-management, composables, provide-inject, ssr, dependency-discipline]
---

# State Management Strategy

Use the lightest state ownership model that fits the actual sharing boundary. Do not install or introduce a state-management dependency merely because state crosses one component boundary.

## Task List

- Keep state local until multiple consumers genuinely need shared ownership
- Prefer feature-scoped composables for feature state
- Reuse the project's existing state-management solution when one is already established
- Do not add a new runtime dependency solely because this reference mentions shared/global state
- Avoid mutable module-level singleton state in SSR/request-scoped runtimes
- Keep mutations easy to locate; expose explicit actions when shared state becomes complex
- Apply the JS / JSDoc / TS stability tiers from the main Skill

## Choose State Scope Before Choosing a Tool

Use this progression as a decision guide, not as a mandatory migration ladder:

1. **Component-local state** — owned by one component or one small component subtree.
2. **Feature composable** — shared inside one feature or reused by a small set of related components.
3. **App-level shared state** — genuinely crosses feature boundaries or must survive independent component lifetimes.
4. **Request-scoped/server state container** — required when SSR or another multi-request runtime must isolate state per request.

The question is **who owns the state and how long it must live**, not which library can be installed.

## Keep Local State Local

Do not promote state to a global store preemptively.

```vue
<script setup>
import { ref } from 'vue'

const isOpen = ref(false)
const draft = ref('')
</script>
```

If only this component or its immediate children need the state, local ownership is usually easier to understand and change.

## Use a Feature Composable for Feature-Level Shared State

```js
// composables/useCart.js
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

Do not make a composable global merely by declaring mutable state at module scope unless global lifetime is explicitly intended.

## Reuse Existing Project Infrastructure

If the project already has an established state-management solution:

- follow its existing store/module conventions
- avoid creating a second competing global-state pattern
- do not replace it as part of an unrelated feature change
- use the dedicated Skill or project documentation for that state solution when available

This generic Vue Skill should not prescribe or install a particular third-party state library.

## Avoid Accidental Module Singletons

A module-level reactive object has process/module lifetime, which may be broader than the component or request lifetime.

**RISKY when global lifetime is not explicitly intended:**

```js
import { reactive } from 'vue'

export const state = reactive({
    user: null,
    permissions: []
})
```

For client-only applications, an intentional singleton can be valid, but make that lifetime explicit. For SSR or multi-request runtimes, do not share user/request state through one module singleton.

## Use Request-Scoped State in SSR

Create mutable state per app/request, or use the request-safe state mechanism already established by the project.

```js
import { reactive, readonly } from 'vue'

export function createRequestState() {
    const state = reactive({
        user: null,
        permissions: []
    })

    function setUser(user) {
        state.user = user
    }

    return {
        state: readonly(state),
        setUser
    }
}
```

The important property is **new mutable state per request/app instance**. Do not introduce a package solely to satisfy this example; integrate with the runtime architecture that already exists.

## Keep Shared Mutations Traceable

When many consumers can change shared state, prefer explicit actions over arbitrary deep mutation from every consumer.

```js
function setCurrentWorkspace(workspace) {
    state.currentWorkspace = workspace
}

function clearCurrentWorkspace() {
    state.currentWorkspace = null
}
```

This is a maintainability rule, not a requirement to wrap every trivial local assignment in an action.

## Dependency Discipline

Examples in this Skill are conceptual. They are **not permission to add dependencies**.

Before adding any new runtime package for state management:

1. Confirm the project does not already have an equivalent solution.
2. Confirm native Vue primitives and existing project infrastructure are insufficient for the requirement.
3. Make the dependency addition an explicit, justified change rather than an incidental refactor.
4. Keep third-party-specific usage rules in a dedicated Skill or project-level documentation instead of expanding this generic Vue Skill.
