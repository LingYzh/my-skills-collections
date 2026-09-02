---
title: KeepAlive Component Guidance
impact: MEDIUM
impactDescription: KeepAlive preserves component instances; use it only when preserving state is an intentional product behavior
type: best-practice
tags: [vue3, keepalive, cache, lifecycle, performance, platform]
---

# KeepAlive Component Guidance

Use `<KeepAlive>` when preserving a component instance across switches is explicitly useful. Do not add caching merely to avoid remounting without understanding freshness and lifetime requirements.

## Task List

- Confirm the target platform supports KeepAlive
- Decide whether state should persist or reset when the view becomes inactive
- Handle activation/deactivation lifecycle when background work must pause or refresh
- Add cache bounds only when the application can actually accumulate enough cached instances to require them
- Define a freshness/invalidation strategy for data that can become stale
- Do not copy arbitrary cache-size numbers from examples

## Basic Use

```vue
<template>
    <KeepAlive>
        <component :is="currentPanel" />
    </KeepAlive>
</template>
```

This is appropriate only when `currentPanel` switching and instance preservation are supported by the current runtime.

## Activation Lifecycle

```vue
<script setup>
import {
    onActivated,
    onDeactivated
} from 'vue'

onActivated(() => {
    refreshIfNeeded()
})

onDeactivated(() => {
    pauseBackgroundWork()
})
</script>
```

Do not refresh automatically on every activation unless the feature actually requires fresh data each time.

## Cache Bounds Are Requirement-Driven

`max` can limit cached instances, but there is no universal correct value.

```vue
<template>
    <KeepAlive :max="cacheLimit">
        <component :is="currentPanel" />
    </KeepAlive>
</template>
```

`cacheLimit` should come from the application's view set, memory behavior, and UX expectations. Do not hard-code a Skill-provided value such as `5` simply because it appeared in documentation.

## Invalidation

When a cached view must be recreated, use an existing project pattern such as changing the rendered key or changing which components are included in the cache.

```vue
<template>
    <KeepAlive>
        <component
            :is="currentPanel"
            :key="panelKey"
        />
    </KeepAlive>
</template>
```

Do not build a custom cache manager unless the product actually needs one.

## Do Not Cache by Default

Avoid KeepAlive when:

- each visit should intentionally start fresh
- the component owns large/native resources that should be released
- background activity cannot be paused safely
- sensitive temporary state should disappear on exit
- preserving stale UI would confuse users

## uni-app Platform Gate

For uni-app, load `uni-app-platform.md` first. KeepAlive support differs by target; do not copy a Web Vue caching pattern into App/mini-program code unless the target compatibility is confirmed.

This generic reference intentionally avoids router-specific caching recipes. Follow the project's existing routing architecture instead of introducing a routing dependency or pattern from an example.
