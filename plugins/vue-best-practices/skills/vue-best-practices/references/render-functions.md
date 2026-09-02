---
title: Render Function Guidance
impact: MEDIUM
impactDescription: Render functions are lower-level than templates and should be reserved for requirements that benefit from programmatic VNode construction
type: best-practice
tags: [vue3, render-function, h, v-model, directives, jsx, platform]
---

# Render Function Guidance

Prefer Vue templates for ordinary application UI. Use render functions when programmatic VNode construction is genuinely clearer or required by a low-level reusable abstraction.

## Task List

- Prefer templates for normal business components
- Use stable keys for programmatically rendered collections
- Keep explicit component model/update contracts
- Use Vue render helpers rather than manually emulating template behavior
- Keep render-function code small and well-contained
- Do not convert templates to render functions as an incidental refactor
- Apply the uni-app platform gate before assuming every Web Vue render pattern compiles/behaves identically

## Prefer a Template When It Is Clearer

```vue
<script setup>
import { ref } from 'vue'

const count = ref(0)
</script>

<template>
    <div>
        Count: {{ count }}
    </div>
</template>
```

Do not replace this with `h()` merely for abstraction consistency.

## Programmatic List

```js
import { h, ref } from 'vue'

export default {
    setup() {
        const items = ref([
            {
                id: 1,
                name: 'Apple'
            }
        ])

        return () => {
            return h(
                'ul',
                items.value.map((item) => {
                    return h(
                        'li',
                        {
                            key: item.id
                        },
                        item.name
                    )
                })
            )
        }
    }
}
```

## Explicit Model Contract

When rendering a component programmatically, wire its model contract explicitly.

```js
return () => {
    return h(CustomInput, {
        modelValue: text.value,
        'onUpdate:modelValue': (value) => {
            text.value = value
        }
    })
}
```

## Directives and Event Helpers

If a render function truly needs directive/event-modifier behavior, use the corresponding Vue render helpers. Avoid manually reimplementing framework semantics when a built-in helper already exists.

## Stability Tier

Render functions used in volatile business code should stay JavaScript unless the surrounding project/file is already TypeScript. A stable low-level Tier C renderer may use TypeScript when its VNode/public contract benefits from it.

## Platform Gate

For uni-app, load `uni-app-platform.md` first. Render functions are lower-level framework behavior and should not be assumed portable across all compiled targets without checking the project's/runtime's supported patterns.
