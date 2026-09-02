---
title: Async API Calls and UI Loading Locks
impact: HIGH
impactDescription: Unguarded async UI actions cause duplicate submissions, conflicting state changes, and race-condition bugs
type: best-practice
tags: [vue3, async, api, promise, axios, loading, disabled, ui-lock, race-condition, uni-app]
---

# Async API Calls and UI Loading Locks

UI-triggered API/interface calls must prevent duplicate or conflicting user actions while the request is pending. Prefer Promise chaining for ordinary request flow and restore application-level loading/interaction locks in `finally()`, while respecting platform-specific lifecycle rules.

**Axios is an approved ecosystem dependency for ordinary Web Vue projects in this Skill.** It may be used directly when the project already uses it or when a new Web Vue project needs a reusable HTTP client/request layer. It is not treated as a universal uni-app transport.

## Task List

- Prefer Promise chaining (`.then().catch().finally()`) for ordinary API/interface calls
- Reuse the project's existing request wrapper/client when one exists
- Axios is an approved Web Vue HTTP client; do not replace a working request layer incidentally
- In cross-platform uni-app code, prefer the project's `uni.request`-based abstraction unless Axios compatibility is already established for the actual targets
- Set an operation-specific loading state before the request starts
- Guard the handler against duplicate execution while loading
- Disable or otherwise lock conflicting UI controls during the request
- Show a loading state when the operation is user-visible
- Release application-level state locks in `.finally()` for both success and failure paths
- Keep unrelated actions enabled when they cannot conflict
- Use a request token/counter instead of one boolean if overlapping requests are intentionally allowed
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

This deliberately uses two guards:

1. The handler rejects duplicate/programmatic entry while pending.
2. The UI prevents the user from triggering a conflicting action.

## Prefer Promise Chaining for Interface Calls

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

Use `async` / `await` when it materially improves readability, especially for several dependent asynchronous branches. Do not convert an existing clear Promise chain incidentally.

## Axios in Ordinary Web Vue Projects

When Axios is already the project's HTTP client, use its existing configured instance/interceptors rather than importing the default client everywhere.

A simple project-owned request client can look like:

```js
// api/http.js
import axios from 'axios'

export const http = axios.create({
    baseURL: '/api'
})
```

Then business code remains chain-oriented:

```js
import { http } from '@/api/http'

function loadUser(userId) {
    if (isLoading.value) return

    isLoading.value = true

    return http
        .get(`/users/${userId}`)
        .then((response) => {
            currentUser.value = response.data
        })
        .catch((error) => {
            handleLoadError(error)
        })
        .finally(() => {
            isLoading.value = false
        })
}
```

Prefer a shared Axios instance when the application needs common `baseURL`, headers, interceptors, authentication/error handling, or cancellation behavior.

Do **not**:

- replace an existing working request wrapper/fetch layer merely to standardize on Axios
- create many differently configured Axios instances without a real boundary
- bury UI loading locks exclusively inside a global interceptor when the lock belongs to one specific operation
- assume Axios is portable to every uni-app non-Web target

For a new ordinary Web Vue application with a meaningful reusable HTTP layer and no established request client, Axios is an approved default choice in this Skill.

## Scope the Lock to the Operation

```js
const isLoadingUsers = ref(false)
const isSavingProfile = ref(false)
const isDeletingItem = ref(false)
```

Avoid one global `isLoading` flag when independent operations can safely run separately. The purpose is to block **conflicting** user behavior, not freeze unrelated parts of the application.

## Lock Every Conflicting Entry Point

If the same operation can be triggered from several controls, they must share the same lock.

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

`finally()` is the normal cleanup point for application-level flags because it runs after either fulfillment or rejection. Platform-native loading/toast APIs can have additional ordering constraints.

## uni-app Request Transport

For uni-app code shared across App/mini-program targets, `uni.request` or an existing project wrapper around it is the normal portable transport.

Do not introduce Axios into shared non-H5 uni-app code merely because Axios is approved for ordinary Web Vue. Non-Web uni-app runtimes are not normal browser/XHR environments.

Axios is acceptable in uni-app when:

- the feature is H5/Web-only, or
- the existing project already has a tested Axios adapter/wrapper that supports all required targets

Otherwise preserve the cross-platform request layer already used by the project.

Vue 3 uni-app APIs support Promise-style calls, so the preferred chain style can still be used with `uni.request`/project wrappers without requiring Axios.

## uni-app: Hide Loading Before `showToast`

When a request uses both `uni.showLoading()` and `uni.showToast()`:

- call `uni.hideLoading()` **before** `uni.showToast()` on both success and failure paths
- do **not** place the only `uni.hideLoading()` after `showToast()` in `.finally()`
- keep the application-level `isLoading` / `isSubmitting` lock cleanup in `.finally()`
- when using `uni.showLoading()` to block interaction, prefer `mask: true` where the target platform supports it
- keep a handler-level duplicate-entry guard; the visual mask is not a substitute for state-level protection

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
    .finally(() => {
        uni.hideLoading()
        isSubmitting.value = false
    })
```

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
    -> uni.hideLoading()
    -> uni.showToast(...)
    -> finally: release reactive/business interaction lock
```

If a branch does not show a toast, it must still explicitly close the native loading layer at the appropriate point.

## Prevent Earlier Requests from Unlocking a Later Request

If overlapping requests are intentionally allowed, use a counter or request token instead of one boolean.

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
