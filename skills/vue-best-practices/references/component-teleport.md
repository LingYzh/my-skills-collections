---
title: Teleport Component Guidance
impact: MEDIUM
impactDescription: Teleport changes rendered DOM placement while preserving Vue hierarchy; support and usefulness depend on the target platform
type: best-practice
tags: [vue3, teleport, overlay, positioning, platform]
---

# Teleport Component Guidance

Use `<Teleport>` when browser-rendered UI must escape an ancestor's stacking/overflow/layout context, such as a modal or overlay rendered into an application-owned overlay root.

## Task List

- Confirm the target platform supports Teleport
- Use an existing project overlay target/convention when one exists
- Ensure the target exists before the teleported content renders
- Keep ownership/data flow in the original Vue component hierarchy
- Do not add an overlay/responsive dependency from this reference
- In uni-app, load `uni-app-platform.md` first because Teleport support varies by target

## Basic Overlay

```vue
<template>
    <button @click="isOpen = true">
        Open
    </button>

    <Teleport to="#overlay-root">
        <ModalPanel
            v-if="isOpen"
            @close="isOpen = false"
        />
    </Teleport>
</template>
```

Prefer a target already owned by the application rather than creating new global containers during unrelated work.

## Conditional Teleport

If a layout sometimes renders content inline, drive `:disabled` from existing component/project state.

```vue
<script setup>
const props = defineProps({
    renderInline: Boolean
})
</script>

<template>
    <Teleport
        to="#overlay-root"
        :disabled="props.renderInline"
    >
        <SidePanel />
    </Teleport>
</template>
```

This Skill intentionally does not recommend a media-query package. Reuse the project's existing responsive state when responsive behavior is required.

## Logical Hierarchy Remains Vue-Owned

Teleport changes render placement, not component ownership. Props, events, slots, and provide/inject continue through the Vue hierarchy.

```vue
<template>
    <Teleport to="#overlay-root">
        <ChildPanel
            :message="message"
            @close="isOpen = false"
        />
    </Teleport>
</template>
```

## Platform Gate

In uni-app, Teleport is not universally supported across H5, App, and mini-program targets. Do not use it until `uni-app-platform.md` confirms the current target/runtime is compatible.

If the project already has a platform-native modal/overlay abstraction, prefer that existing abstraction rather than forcing Teleport into cross-platform code.
