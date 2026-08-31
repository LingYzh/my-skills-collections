---
title: Async API Calls and UI Loading Locks
impact: HIGH
impactDescription: Unguarded async UI actions cause duplicate submissions, conflicting state changes, and race-condition bugs
type: best-practice
tags: [vue3, async, api, promise, loading, disabled, ui-lock, race-condition]
---

# Async API Calls and UI Loading Locks

**Impact: HIGH** - UI-triggered API/interface calls must prevent duplicate or conflicting user actions while the request is pending. Prefer Promise chaining for request flow and always restore the UI lock in `finally()`.

## Task List

- Prefer Promise chaining (`.then().catch().finally()`) for API/interface calls
- Set an operation-specific loading state before the request starts
- Guard the handler against duplicate execution while loading
- Disable or otherwise lock conflicting UI controls during the request
- Show a loading state when the operation is user-visible
- Release the lock in `.finally()` for both success and failure paths
- Keep unrelated actions enabled when they cannot conflict
- Use a request token/counter instead of a single boolean if overlapping requests are intentionally allowed

## Default Pattern

```vue
<script setup>
import { ref } from 'vue'

const isSaving = ref(false)

function saveProfile() {
    if (isSaving.value) return

    isSaving.value = true

    updateProfileApi()
        .then((result) => {
            applySavedProfile(result)
        })
        .catch((error) => {
            showSaveError(error)
        })
        .finally(() => {
            isSaving.value = false
        })
}
</script>

<template>
    <button
        :disabled="isSaving"
        @click="saveProfile"
    >
        {{ isSaving ? 'Saving...' : 'Save' }}
    </button>
</template>
```

This pattern deliberately has two guards:

1. The handler checks `isSaving` so programmatic or unexpected repeated invocation cannot start another request.
2. The UI control is disabled so the user cannot trigger a conflicting action during the request.

## Prefer Promise Chaining for Interface Calls

For ordinary request → success → error → cleanup flows, use chaining by default:

```js
isLoading.value = true

fetchUserApi(userId)
    .then((user) => {
        currentUser.value = user
    })
    .catch((error) => {
        handleLoadError(error)
    })
    .finally(() => {
        isLoading.value = false
    })
```

Use `async` / `await` only when it is materially easier to read, for example when several dependent asynchronous branches would make a Promise chain harder to follow. Do not convert an existing clear Promise chain to `async` / `await` incidentally.

## Scope the Lock to the Operation

Prefer operation-specific state:

```js
const isLoadingUsers = ref(false)
const isSavingProfile = ref(false)
const isDeletingItem = ref(false)
```

Avoid one global `isLoading` flag when independent operations can safely run separately. The purpose is to block **conflicting** user behavior, not freeze unrelated parts of the application.

## Lock Every Conflicting Entry Point

If the same operation can be triggered from several controls, they must share the same lock:

```vue
<template>
    <button :disabled="isSubmitting" @click="submitOrder">
        Submit
    </button>

    <button :disabled="isSubmitting" @click="submitOrder">
        Submit and Close
    </button>
</template>
```

For navigation, destructive actions, form mutation, or other interactions that would invalidate the pending request, disable or guard those actions until the request settles.

## Always Unlock in `finally()`

Do not duplicate unlock logic in both success and error handlers.

**BAD:**

```js
isLoading.value = true

requestApi()
    .then(() => {
        isLoading.value = false
    })
    .catch(() => {
        isLoading.value = false
    })
```

**GOOD:**

```js
isLoading.value = true

requestApi()
    .then(handleSuccess)
    .catch(handleError)
    .finally(() => {
        isLoading.value = false
    })
```

`finally()` is the canonical cleanup point because it runs after either fulfillment or rejection.

## Prevent Earlier Requests from Unlocking a Later Request

If overlapping requests are intentionally allowed, a single boolean can unlock too early. Use a counter or request token instead.

```js
const pendingCount = ref(0)

function runRequest() {
    pendingCount.value += 1

    return requestApi()
        .finally(() => {
            pendingCount.value -= 1
        })
}

const isLoading = computed(() => pendingCount.value > 0)
```

If requests should never overlap, prefer the simpler operation-specific boolean plus duplicate-entry guard.

## Loading UI Requirements

When the operation is visible to the user:

- disable the initiating control or conflicting controls
- show spinner/text/progress feedback where appropriate
- keep the current UI stable until the operation settles
- do not allow repeated submits, destructive actions, or state changes that conflict with the pending request
- restore controls in `finally()` even when the request fails
