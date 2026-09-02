---
title: Vue Plugin Guidance
impact: MEDIUM
impactDescription: Plugins are app-wide installation boundaries and should be used only when behavior genuinely belongs at application scope
type: best-practice
tags: [vue3, plugins, provide-inject, dependency-injection, javascript, typescript]
---

# Vue Plugin Guidance

Use a Vue plugin when a capability genuinely needs application-wide installation/configuration. Do not wrap ordinary feature code in a plugin merely because `app.use()` exists.

## Task List

- Keep plugin installation explicit
- Register only app-wide capabilities in `install()`
- Prefer provide/inject for service/config exposure when appropriate
- Use collision-resistant keys for broadly shared injection contracts
- Follow JS/JSDoc/TS stability tiers
- Do not add a third-party plugin/package because this reference demonstrates plugin architecture
- Do not migrate project initialization architecture during unrelated feature work

## Basic JavaScript Plugin

```js
const serviceKey = Symbol('service')

export const servicePlugin = {
    install(app, options = {}) {
        const service = createService(options)

        app.provide(serviceKey, service)
    }
}
```

Use an install function instead of an object when that is simpler:

```js
export function installFeature(app, options = {}) {
    app.provide(featureKey, createFeatureService(options))
}
```

## Keep Installation Scope Honest

Plugins are appropriate for things such as:

- application-wide service/config initialization
- intentionally global components/directives
- app-level provide/inject setup
- framework integration that must run once during app creation

A feature-local helper or one-page service usually does not need an app plugin.

## Avoid Excessive `globalProperties`

`app.config.globalProperties` can be useful for legacy or intentionally global helpers, but it hides dependencies from component imports/setup.

Prefer explicit imports or provide/inject when they make dependencies easier to trace.

## Required Injection Helpers

When a plugin-installed service is mandatory, a small helper can fail early with a clear message.

```js
import { inject } from 'vue'

export function useRequiredService() {
    const service = inject(serviceKey)

    if (!service) {
        throw new Error('Required application service is not installed')
    }

    return service
}
```

## Stability Tier

JavaScript is the normal choice for changing application plugins. TypeScript is appropriate when a plugin exposes a stable Tier C public contract used across many modules/apps.

Do not enable TypeScript solely because the code uses `app.use()` or provide/inject.

## Dependency Discipline

This reference describes how to structure a Vue plugin that the project owns. It is not a catalog of third-party plugins and does not authorize package installation.
