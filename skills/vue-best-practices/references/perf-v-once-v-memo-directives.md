---
title: v-once and v-memo Performance Guidance
impact: MEDIUM
impactDescription: Manual template memoization can skip updates, but incorrect use can freeze UI and should be justified by a real hot path
type: efficiency
tags: [vue3, performance, v-once, v-memo, optimization, profiling]
---

# v-once and v-memo Performance Guidance

Use `v-once` / `v-memo` only when a real rendering hot path benefits from skipping updates. Vue's normal renderer should remain the default.

## Task List

- Apply `v-once` only to content that truly must never update after initial render
- Apply `v-memo` only when the memo dependency list fully describes when the subtree must update
- Verify child/component interaction is not accidentally frozen
- Profile before and after when this is a performance optimization
- Do not add memoization to trivial templates without evidence
- Do not rely on fake “1000 items -> 2 updates” performance tables as universal behavior

## `v-once`

```vue
<template>
    <section v-once>
        <h2>{{ immutableHeading }}</h2>
        <p>{{ immutableDescription }}</p>
    </section>
</template>
```

Use this only when those values are intentionally fixed for the component instance. If they can change, `v-once` is incorrect.

## `v-memo`

```vue
<template>
    <div
        v-for="item in items"
        :key="item.id"
        v-memo="[
            item.id === selectedId,
            item.id === editingId
        ]"
    >
        <ItemCard
            :item="item"
            :selected="item.id === selectedId"
            :editing="item.id === editingId"
        />
    </div>
</template>
```

This is valid only if no other value affecting the subtree needs to trigger an update. Missing a dependency can create stale UI.

## Do Not Memoize Interactive State Blindly

Be cautious around:

- form controls / `v-model`
- child components with independent reactive state
- slots whose visible output depends on changing parent state
- accessibility state
- frequently changing data not represented in the memo array

Correctness is more important than skipped updates.

## Performance Rule

Do not add `v-once` / `v-memo` as a routine cleanup. Use them after identifying a meaningful render-update cost or when the content's immutability is an explicit design property.

If a list is genuinely large, also check whether the real issue is mounted-tree size (`perf-virtualize-large-lists.md`) or component overhead (`perf-avoid-component-abstraction-in-lists.md`) rather than memoization.
