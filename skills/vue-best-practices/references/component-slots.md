---
title: Component Slot Guidance
impact: MEDIUM
impactDescription: Slots are useful public composition contracts, but unnecessary slot APIs can make simple components harder to maintain
type: best-practice
tags: [vue3, slots, components, javascript, typescript]
---

# Component Slot Guidance

Use slots when the parent genuinely needs to control child content/layout while the child still owns the surrounding structure or behavior.

## Task List

- Prefer the `#name` shorthand for named slots
- Give optional slots sensible fallback content when appropriate
- Render optional wrappers conditionally when an empty wrapper would affect layout/semantics
- Type slot props only in Tier C TypeScript components where the stable public contract benefits from it
- Do not convert a simple prop-based component to slots without a real customization need
- Do not replace a renderless component with a composable automatically; choose the abstraction that best matches UI vs logic composition

## Named Slots

```vue
<PanelCard>
    <template #header>
        <h2>Profile</h2>
    </template>

    <p>Main content</p>
</PanelCard>
```

## Optional Wrappers

If the wrapper itself adds layout, spacing, or semantics, avoid rendering it when the slot is absent.

```vue
<template>
    <article class="card">
        <header
            v-if="$slots.header"
            class="card__header"
        >
            <slot name="header" />
        </header>

        <section class="card__body">
            <slot />
        </section>

        <footer
            v-if="$slots.footer"
            class="card__footer"
        >
            <slot name="footer" />
        </footer>
    </article>
</template>
```

Do not add `$slots` checks when an empty wrapper is harmless and the check only adds noise.

## Fallback Content

```vue
<template>
    <button type="submit">
        <slot>Submit</slot>
    </button>
</template>
```

Fallback content is useful when the component has a clear default. Do not invent fallback UI that hides a missing required contract.

## Scoped Slots

Use scoped slots when the child owns data/behavior but the parent needs to control rendering.

```vue
<template>
    <ul>
        <li
            v-for="(item, index) in items"
            :key="item.id"
        >
            <slot
                :item="item"
                :index="index"
            />
        </li>
    </ul>
</template>
```

For Tier A/B JavaScript components, runtime behavior is sufficient unless a shared contract needs JSDoc.

For a stable Tier C TypeScript foundation component, `defineSlots()` may be used to type the slot contract. Do not enable TypeScript solely because scoped slots exist.

## Slots vs Props vs Composables

Choose based on responsibility:

- prop -> parent supplies a value/configuration
- slot -> parent supplies UI/content
- event -> child reports an action/change
- composable -> reusable stateful/behavior logic without owning rendered structure
- renderless component -> can still be valid when slot-driven UI composition is itself the intended API

Do not force one mechanism to replace another based only on style preference.
