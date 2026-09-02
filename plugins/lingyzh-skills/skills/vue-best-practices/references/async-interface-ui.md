---
title: Async API Calls and UI Loading Locks
impact: HIGH
impactDescription: Clear request layering plus guarded async UI prevents duplicated transport logic, duplicate submissions, conflicting state changes, and race-condition bugs
type: best-practice
tags: [vue3, async, api, promise, axios, request-wrapper, loading, disabled, ui-lock, race-condition, uni-app]
---

# Async API Calls and UI Loading Locks

UI-triggered API/interface calls should use a clear request architecture and prevent duplicate or conflicting user actions while a request is pending.

Prefer this three-layer model when Axios is used:

```text
utils/request.js
    -> configured Axios instance + interceptors
api/<feature>.js
    -> semantic endpoint functions
page/component
    -> business flow + Promise chain + UI loading lock
```

The transport layer owns transport concerns. API definition files own endpoint definitions. Business components own UI state and interaction locks.

## Task List

- Prefer Promise chaining (`.then().catch().finally()`) for ordinary API/interface calls
- Reuse the project's existing request wrapper/client when one exists
- When Axios is used, prefer one project-owned configured `request` instance instead of direct Axios calls scattered through business code
- Define endpoints as named functions in feature/domain API modules
- Call those API functions from business pages/components; avoid embedding endpoint URLs and transport config in the UI layer
- Respect the request wrapper's resolved response contract instead of blindly reading `response.data`
- Keep component/page loading locks out of global request interceptors unless the project explicitly implements a global loading policy
- Set an operation-specific loading state before the request starts
- Guard the handler against duplicate execution while loading
- Disable or otherwise lock conflicting UI controls during the request
- Release application-level state locks in `.finally()` for both success and failure paths
- Keep unrelated actions enabled when they cannot conflict
- In uni-app, do not reject Axios merely because the target is a mini program; choose transport from actual project/target compatibility
- In uni-app, hide `uni.showLoading()` before a following `uni.showToast()`; do not rely on a later `uni.hideLoading()` in `.finally()`

## 1. Preferred Axios Architecture

### Layer 1 — `utils/request.js`: configured transport

Create/configure Axios once and export the configured instance.

Typical responsibilities include:

- `baseURL`
- timeout
- auth/token headers
- request/response interceptors
- request serialization/normalization
- duplicate-request or repeat-submit protection when the project needs it
- common response-code handling
- common transport/network error normalization

```js
// utils/request.js
import axios from 'axios'

const service = axios.create({
    baseURL: import.meta.env.VITE_APP_BASE_API,
    timeout: 10000
})

service.interceptors.request.use((config) => {
    return config
})

service.interceptors.response.use(
    (response) => {
        return response.data
    },
    (error) => {
        return Promise.reject(error)
    }
)

export default service
```

Do not put page/component-specific `isLoading`, button disabling, modal state, or local UI flow inside this global request instance. Those concerns belong to the business layer.

### Layer 2 — `api/<feature>.js`: semantic API definitions

API definition files import the configured `request` instance and expose named business/domain functions.

```js
import request from '@/utils/request'

// 查询活动模板列表
export function listEventFormat(query) {
    return request({
        url: '/business/eventFormat/list',
        method: 'get',
        params: query
    })
}
```

Prefer this over business components doing:

```js
request({
    url: '/business/eventFormat/list',
    method: 'get',
    params: query
})
```

or:

```js
axios.get('/business/eventFormat/list', {
    params: query
})
```

The named API function keeps endpoint paths, HTTP methods, and parameter placement out of volatile UI/business code.

Group endpoint functions by the project's existing domain/feature organization. Do not create a new API-folder taxonomy merely because this reference shows one.

### Layer 3 — page/component: business flow and UI lock

Business code imports semantic API functions and handles local UI state around them.

```vue
<script setup>
import { ref } from 'vue'
import { listEventFormat } from '@/api/business/eventFormat'

const loading = ref(false)
const rows = ref([])
const query = {
    pageNum: 1,
    pageSize: 20
}

function loadList() {
    if (loading.value) return

    loading.value = true

    listEventFormat(query)
        .then((data) => {
            rows.value = data.rows ?? []
        })
        .catch((error) => {
            handleLoadError(error)
        })
        .finally(() => {
            loading.value = false
        })
}
</script>
```

If the response interceptor already resolves `response.data`, `listEventFormat()` resolves that normalized business payload. Do **not** mechanically write `response.data` again in the page layer. Follow the actual contract of the project's request wrapper.

## 2. Promise Chaining Is the Default Business Call Style

For ordinary request -> success -> failure -> cleanup flows, prefer:

```js
listEventFormat(query)
    .then((data) => {
        applyList(data)
    })
    .catch((error) => {
        handleLoadError(error)
    })
    .finally(() => {
        loading.value = false
    })
```

Use `async` / `await` only when it materially improves readability, especially when several dependent asynchronous branches make a Promise chain harder to follow.

Do not convert an existing clear Promise chain to `async` / `await` incidentally.

## 3. UI Loading Locks Belong to the Operation

The transport/request layer may implement network-level duplicate protection, but that does **not** replace business/UI locking.

A UI-triggered operation should normally have both:

1. a handler guard, so programmatic/repeated entry cannot start the same operation again
2. disabled/locked conflicting controls, so the user cannot trigger conflicting state changes while the request is pending

```vue
<script setup>
import { ref } from 'vue'
import { saveProfile } from '@/api/profile'

const isSaving = ref(false)

function submitProfile(payload) {
    if (isSaving.value) return

    isSaving.value = true

    saveProfile(payload)
        .then((data) => {
            applySavedProfile(data)
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
        @click="submitProfile(formData)"
    >
        {{ isSaving ? 'Saving...' : 'Save' }}
    </button>
</template>
```

Scope locks to the operation:

```js
const isLoadingUsers = ref(false)
const isSavingProfile = ref(false)
const isDeletingItem = ref(false)
```

Avoid one global `isLoading` flag when independent operations can safely run separately.

## 4. Axios Is Approved Beyond Web-Only Projects When Compatibility Is Real

Do not use a blanket rule such as "uni-app non-H5 must use `uni.request`".

Axios may remain the preferred request layer in uni-app when:

- the project already uses an Axios-based `request` wrapper successfully on the target
- the project is single-target and that App/mini-program runtime is verified compatible
- the selected Axios version/runtime works directly for the required features
- the project already uses a compatible Axios adapter and the extra adapter behavior is actually needed

A mini-program target by itself is **not** evidence that Axios must be removed.

Use or fall back to `uni.request` / a `uni.request`-based wrapper when there is a concrete reason, such as:

- the target/runtime actually fails with the current Axios setup
- required Axios/browser adapter behavior is unavailable
- the feature needs uni-app/platform-specific request options or request-task APIs that the current Axios layer does not expose correctly
- multi-target compatibility is required and the existing Axios setup is not verified across all targets
- the project already standardizes on a `uni.request` wrapper and replacing it would create unnecessary migration work

Do not install an Axios adapter merely because the project is uni-app. First verify whether the existing Axios setup already works for the actual target and required request features.

## 5. uni-app: Hide Loading Before `showToast`

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

Required order:

```text
request success/failure
    -> uni.hideLoading()
    -> uni.showToast(...)
    -> finally
        -> release reactive/business interaction lock
```

If a branch does not show a toast, it must still explicitly close the native loading layer at the appropriate point.

## 6. Concurrent Requests

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

## Final Checks for Request Code

- transport/config/interceptors stay in the shared request layer
- endpoint URL/method/params stay in named API functions
- volatile page/component code imports semantic API functions instead of raw Axios/request config when practical
- business code respects the wrapper's resolved response shape
- UI loading/disabled locks stay at the operation/business layer
- Promise chaining is used for ordinary request flow
- uni-app transport choice is based on actual compatibility, not on a blanket H5/non-H5 split
- `uni.hideLoading()` precedes a following `uni.showToast()`
