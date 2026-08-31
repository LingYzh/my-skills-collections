---
title: Async API Calls and UI Loading Locks
impact: HIGH
impactDescription: Unguarded async UI actions cause duplicate submissions, conflicting state changes, and race-condition bugs
type: best-practice
tags: [vue3, async, api, promise, loading, disabled, ui-lock, race-condition, uni-app]
---

# Async API Calls and UI Loading Locks

**Impact: HIGH** - UI-triggered API/interface calls must prevent duplicate or conflicting user actions while the request is pending. Prefer Promise chaining for request flow. Restore application-level loading/interaction locks in `finally()`, while respecting platform-specific loading/toast lifecycle rules.

## Task List

- Prefer Promise chaining (`.then().catch().finally()`) for API/interface calls
- Set an operation-specific loading state before the request starts
- Guard the handler against duplicate execution while loading
- Disable or otherwise lock conflicting UI controls during the request
- Show a loading state when the operation is user-visible
- Release application-level state locks in `.finally()` for both success and failure paths
- Keep unrelated actions enabled when they cannot conflict
- Use a request token/counter instead of a single boolean if overlapping requests are intentionally allowed
- In uni-app, hide `uni.showLoading()` before calling `uni.showToast()`; do not rely on a later `uni.hideLoading()` in `.finally()`

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

## Use `finally()` for Application-Level Lock Cleanup

Do not duplicate application-level reactive lock cleanup in both success and error handlers.

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

`finally()` is the normal cleanup point for application-level flags because it runs after either fulfillment or rejection. Platform-native loading/toast APIs can have additional ordering constraints; apply the platform-specific rules below instead of mechanically putting every cleanup call in `finally()`.

## uni-app: Hide Loading Before `showToast`

In uni-app, `uni.showLoading()` and `uni.showToast()` can share the same underlying prompt layer on mini-program-style implementations. DCloud staff has explicitly noted that these two APIs overwrite each other and that `uni.hideLoading()` can also close a toast.

Therefore, when a request uses both `uni.showLoading()` and `uni.showToast()`:

- call `uni.hideLoading()` **before** `uni.showToast()` on both success and failure paths
- do **not** place the only `uni.hideLoading()` after `showToast()` in `.finally()`
- keep the application-level `isLoading` / `isSubmitting` lock cleanup in `.finally()`
- when using `uni.showLoading()` to block interaction, prefer `mask: true` where the target platform supports it
- still keep a handler-level duplicate-entry guard; the visual mask is not a substitute for state-level protection

**BAD:**

```js
uni.showLoading({
    title: '提交中',
    mask: true
})

isSubmitting.value = true

submitApi()
    .then(() => {
        uni.showToast({
            title: '提交成功',
            icon: 'success'
        })
    })
    .catch(() => {
        uni.showToast({
            title: '提交失败',
            icon: 'none'
        })
    })
    .finally(() => {
        uni.hideLoading()
        isSubmitting.value = false
    })
```

The later `uni.hideLoading()` can close or suppress the toast because the loading and toast prompt layers are not independent on affected targets.

**GOOD:**

```js
function submitForm() {
    if (isSubmitting.value) return

    isSubmitting.value = true

    uni.showLoading({
        title: '提交中',
        mask: true
    })

    submitApi()
        .then((result) => {
            applyResult(result)

            uni.hideLoading()
            uni.showToast({
                title: '提交成功',
                icon: 'success'
            })
        })
        .catch((error) => {
            handleSubmitError(error)

            uni.hideLoading()
            uni.showToast({
                title: '提交失败',
                icon: 'none'
            })
        })
        .finally(() => {
            isSubmitting.value = false
        })
}
```

The important order is:

```text
request settles
    → uni.hideLoading()
    → uni.showToast(...)
    → finally: release reactive/business interaction lock
```

If a branch does not show a toast, it must still explicitly close the native loading layer at the appropriate point. Do not leave `uni.showLoading()` open merely because the reactive lock is released in `finally()`.

References:

- uni-app prompt API: https://uniapp.dcloud.net.cn/api/ui/prompt
- DCloud official Q&A explaining the shared underlying prompt layer: https://ask.dcloud.net.cn/question/91875

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
- restore application-level controls in `finally()` even when the request fails
- keep platform-native loading/toast teardown order correct instead of assuming every visual cleanup belongs in `finally()`
