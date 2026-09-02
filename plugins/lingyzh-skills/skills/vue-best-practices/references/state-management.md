---
title: State Management Strategy
impact: HIGH
impactDescription: State scope should match ownership and runtime lifetime; Pinia is the preferred app-level store when a real global state boundary exists
type: best-practice
tags: [vue3, state-management, composables, pinia, provide-inject, ssr, dependency-discipline]
---

# State Management Strategy

Use the lightest state ownership model that fits the actual sharing boundary. Do not move local or feature state into a global store preemptively.

**Pinia is an approved ecosystem dependency in this Skill.** It is Vue's current default/recommended state-management solution and may be selected directly when the application genuinely needs app-level shared state, SSR-safe store ownership, DevTools/action tracing, or a stable cross-feature store contract.

## Task List

- Keep state local until multiple consumers genuinely need shared ownership
- Prefer feature-scoped composables for feature state
- Prefer Pinia when state genuinely crosses feature/page boundaries or requires application-level lifetime
- Reuse the project's existing state-management solution instead of introducing a competing pattern
- Do not replace an established store solution as part of an unrelated task
- Avoid mutable module-level singleton state in SSR/request-scoped runtimes
- Keep shared mutations easy to locate
- Apply the JS / JSDoc / TS stability tiers from the main Skill

## Choose State Scope Before Choosing a Tool

Use this progression as a decision guide:

1. **Component-local state** — owned by one component or one small subtree.
2. **Feature composable** — shared inside one feature or by a small set of related components.
3. **Pinia / existing app store** — state genuinely crosses feature/page boundaries, must survive independent component lifetimes, or benefits from store tooling and explicit actions.
4. **Request-scoped store instance** — SSR or another multi-request runtime must isolate mutable state per request/application instance.

The first question is **who owns the state and how long must it live**. Pinia is not a reason to globalize state that is naturally local.

## Keep Local State Local

```vue
<script setup>
import { ref } from 'vue'

const isOpen = ref(false)
const draft = ref('')
</script>
```

If only this component or its immediate children need the state, a global store adds navigation and ownership cost without a clear benefit.

## Use a Feature Composable for Feature-Level State

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

Do not make a composable global merely by declaring mutable state at module scope unless global lifetime is intentional.

## Prefer Pinia for Genuine App-Level Shared State

For new Vue applications that actually need a global store, Pinia is the preferred default in this Skill.

A JavaScript business-oriented store can stay JavaScript:

```js
// stores/session.js
import { defineStore } from 'pinia'

export const useSessionStore = defineStore('session', {
    state: () => ({
        user: null,
        permissions: []
    }),

    actions: {
        setUser(user) {
            this.user = user
        },

        clearSession() {
            this.user = null
            this.permissions = []
        }
    }
})
```

Do not convert a business store to TypeScript merely because Pinia supports strong type inference. Apply the normal language-tier rules.

Use Pinia especially when one or more of these are true:

- several unrelated pages/features consume the same state
- state must survive independent component lifetimes
- actions/getters make mutation flow easier to trace
- DevTools/HMR/store inspection materially help development
- SSR needs a standard per-app store container
- the project already uses Pinia

## Do Not Overuse Pinia

Avoid moving these into Pinia without a concrete reason:

- one component's modal visibility
- transient form fields used by one page
- local hover/selection state
- data that is naturally owned by one feature component tree

The availability of Pinia does not make every reactive value global.

## Existing Project Infrastructure Wins

If the project already uses Pinia, follow its existing store naming, file placement, setup-store/options-store style, and mutation conventions.

If the project uses another established store solution:

- maintain that solution for ordinary feature work
- do not introduce Pinia beside it merely because Pinia is preferred for new architecture
- migrate only when migration itself is an explicit task with a concrete benefit

## SSR / Request Isolation

Do not put user/request state in a mutable module singleton shared across requests.

When using Pinia in SSR, create/use the store container according to the application's SSR framework/bootstrap so each application/request gets the correct isolated state lifetime.

The same principle applies without Pinia: mutable request/user state must not accidentally live for the whole server process.

## Keep Shared Mutations Traceable

For shared app state, prefer explicit actions when they make ownership and mutation flow easier to understand.

Do not turn every trivial local assignment into an action merely for ceremony.

## Dependency Policy for Pinia

Pinia is an explicit exception to the generic dependency-neutral policy:

- it may be named directly in this Vue Skill
- it may be added to a new/existing project when a genuine app-level store requirement exists and no equivalent store is already established
- adding it does **not** require inventing an extra architecture problem merely to justify the package
- it still must not be introduced as an incidental replacement for working local state or another established store architecture

For deep Pinia-specific patterns beyond ordinary store use, prefer dedicated Pinia documentation/Skill rather than expanding this generic reference indefinitely.
