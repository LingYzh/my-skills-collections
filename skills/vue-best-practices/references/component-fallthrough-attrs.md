---
title: Component Fallthrough Attributes Guidance
impact: MEDIUM
impactDescription: Correct fallthrough-attribute handling keeps wrapper components predictable without assuming attrs are reactive state
type: best-practice
tags: [vue3, attrs, fallthrough-attributes, composition-api, reactivity]
---

# Component Fallthrough Attributes Guidance

Use fallthrough attributes for wrapper/base components that intentionally pass ordinary attributes or listeners to an internal root/target element.

## Task List

- Access hyphenated attr keys with bracket notation
- Access listeners through their `onXxx` keys
- Remember that `useAttrs()` exposes current attrs but is not normal watcher-tracked reactive state
- Promote an attr to a real prop when the component needs to observe/use it as part of its explicit API
- Use `inheritAttrs: false` only when the component needs deliberate forwarding control
- Keep contracts explicit instead of turning important behavior into hidden `$attrs` coupling

## Access Attr Keys Correctly

```vue
<script setup>
import { useAttrs } from 'vue'

const attrs = useAttrs()

console.log(attrs['data-testid'])
console.log(attrs['aria-label'])
console.log(attrs.onClick)
console.log(attrs['onUpdate:modelValue'])
</script>
```

Do not try dot notation for keys containing `-`.

## Do Not Watch `useAttrs()` Like Normal Reactive State

If an input is important enough to drive reactive component logic, make it a prop instead of relying on an attrs watcher.

```vue
<script setup>
import { watch } from 'vue'

const props = defineProps({
    density: String
})

watch(
    () => props.density,
    (density) => {
        applyDensity(density)
    }
)
</script>
```

For rare side effects that genuinely need the latest fallthrough attrs after an update, read the attrs from an update lifecycle hook rather than pretending the attrs object is a normal reactive store.

## Deliberate Forwarding

If a wrapper needs internal handling for an event **and** must forward the parent's listener, avoid forwarding that same listener twice.

```vue
<script setup>
import { useAttrs } from 'vue'

defineOptions({
    inheritAttrs: false
})

const attrs = useAttrs()

function getForwardedAttrs() {
    const {
        onClick,
        ...forwardedAttrs
    } = attrs

    return forwardedAttrs
}

function handleClick(event) {
    runInternalBehavior(event)
    attrs.onClick?.(event)
}
</script>

<template>
    <button
        v-bind="getForwardedAttrs()"
        @click="handleClick"
    >
        <slot />
    </button>
</template>
```

The important rule is to choose one forwarding path per listener. Do not both include `onClick` in `v-bind` and invoke `attrs.onClick` manually.

For simple transparent wrappers with no internal event handling, `v-bind="attrs"` is sufficient.

## Stability Tier

JavaScript runtime attrs are the normal Tier A/B approach. In Tier C TypeScript foundation components, add types only when they protect a stable contract. Do not enable TypeScript merely to read one fallthrough attribute.
