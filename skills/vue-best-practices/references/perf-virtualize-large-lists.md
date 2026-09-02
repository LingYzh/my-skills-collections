---
title: Virtualize Large Lists When Rendering Cost Requires It
impact: HIGH
impactDescription: Large mounted trees can create render and memory pressure, but virtualization should be justified by measured cost and project constraints
type: efficiency
tags: [vue3, performance, virtual-list, large-data, optimization, profiling, dependency-discipline]
---

# Virtualize Large Lists When Rendering Cost Requires It

Virtualization renders only the visible or near-visible portion of a large collection. It can be very effective when the mounted render tree is the actual bottleneck, but it is not a default requirement for every moderately sized list.

## Task List

- Test with realistic data volumes and target devices
- Confirm the mounted list/tree is a meaningful performance bottleneck
- Reuse an existing project virtualization solution when available
- Do not install a virtualization dependency solely because this reference exists
- Account for dynamic item height, keyboard navigation, accessibility, scroll restoration, and testability
- Keep a non-virtualized implementation when it already meets product performance requirements

## Identify the Real Problem First

A long data array does not automatically mean the UI needs virtualization. Measure the rendered result.

Possible bottlenecks include:

- too many mounted DOM/native nodes
- expensive child components
- heavy images/media
- repeated derived-data work
- layout/paint cost
- frequent reactive updates
- network/data transformation

Do not treat item count alone as the decision criterion.

## Conceptual Virtualization Shape

If the project already provides a virtual-list abstraction, the application code should usually consume that established abstraction instead of installing another package.

```vue
<template>
    <ProjectVirtualList
        :items="users"
        item-key="id"
    >
        <template #default="{ item }">
            <UserCard :user="item" />
        </template>
    </ProjectVirtualList>
</template>
```

`ProjectVirtualList` is a placeholder for **whatever virtualization mechanism already belongs to the project**. It is not a library recommendation.

## If No Virtualization Solution Exists

Before adding a dependency, consider whether simpler product/UX changes solve the problem:

- pagination
- incremental loading
- server-side filtering/search
- collapsed sections
- reducing item complexity
- rendering a smaller result window

If those approaches do not satisfy the requirement and measurement shows that virtualization is needed, dependency selection should be an explicit architectural decision outside this generic Skill.

## Dynamic Height and Interaction Concerns

Virtualized lists become more complex when items have unpredictable heights or interactive state. Verify:

- scroll position remains stable
- focus/keyboard navigation remains usable
- recycled rows do not leak stale local state
- dynamic measurement does not cause visible jumping
- automated tests can target rows reliably
- accessibility requirements are still met

Do not trade a small performance gain for fragile interaction behavior.

## Accessibility and Rendering Requirements

Virtualization may be inappropriate when the product requires all items to be mounted simultaneously, for example:

- printing/export capture
- browser find-in-page expectations
- some accessibility flows
- SEO/initial-content requirements in specific web architectures
- scripts that intentionally inspect the full rendered tree

Use the product requirement as the constraint rather than a generic list-size number.

## Performance Rule

There is no universal “virtualize above N items” threshold. Choose virtualization when realistic profiling shows that rendering only the visible window materially improves the required user experience without unacceptable complexity.
