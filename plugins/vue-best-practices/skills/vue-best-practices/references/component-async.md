---
title: Async Component Guidance
impact: MEDIUM
impactDescription: Async components can reduce initial JavaScript work, but lazy loading and hydration timing should follow real product and runtime needs
type: best-practice
tags: [vue3, async-components, ssr, hydration, performance, ux]
---

# Async Component Guidance

Use async components for clearly non-critical, heavy, or rarely visited UI when lazy loading materially improves the application. Do not convert ordinary components to async components by default.

## Task List

- Confirm lazy loading has a real bundle/runtime benefit
- Preserve a stable loading/error UX when the delay is user-visible
- Keep Vue defaults unless product data or measured behavior justifies tuning
- Use lazy hydration only when SSR and the current Vue version/runtime support it
- Do not copy fixed timing values from examples as universal performance rules
- Do not introduce a third-party loader/helper dependency from this reference
- Apply uni-app platform gating before assuming browser/SSR hydration behavior exists

## Basic Async Component

```vue
<script setup>
import { defineAsyncComponent } from 'vue'

const AsyncReportPanel = defineAsyncComponent(() => {
    return import('./ReportPanel.vue')
})
</script>
```

Do not make a small, frequently needed component async merely because `defineAsyncComponent()` exists.

## Loading and Error UI

When a component can take long enough for the user to notice, use existing project loading/error components.

```vue
<script setup>
import { defineAsyncComponent } from 'vue'
import ErrorDisplay from './ErrorDisplay.vue'
import LoadingState from './LoadingState.vue'

const AsyncDashboard = defineAsyncComponent({
    loader: () => import('./Dashboard.vue'),
    loadingComponent: LoadingState,
    errorComponent: ErrorDisplay
})
</script>
```

Keep Vue's default timing behavior unless there is a concrete UX reason to change it. If a custom `delay` or `timeout` is required, choose it from the application's product requirements, telemetry, or realistic testing rather than a Skill-provided table.

## Lazy Hydration in SSR

Modern Vue versions provide lazy hydration strategies for SSR async components. Use them only when:

- the application actually uses SSR/hydration
- the installed Vue version supports the selected strategy
- the component is non-critical enough to defer hydration
- deferred interactivity will not surprise the user

```vue
<script setup>
import {
    defineAsyncComponent,
    hydrateOnVisible
} from 'vue'

const AsyncComments = defineAsyncComponent({
    loader: () => import('./Comments.vue'),
    hydrate: hydrateOnVisible()
})
</script>
```

Do not add hydration strategies to ordinary client-rendered SPA/uni-app code where they are irrelevant.

## Avoid Fake Timing Precision

Do not encode generic rules such as:

- “heavy components should use 100ms”
- “background components should use 300–500ms”
- “all async components need a custom 30-second timeout”

Network speed, chunk size, device performance, caching, and product UX all change the correct behavior. Prefer framework defaults and tune only when the project has evidence.

## Platform Gate

Browser SSR/hydration APIs are not universal Vue semantics. For uni-app, load `uni-app-platform.md` first and use only capabilities supported by the current target/runtime.
