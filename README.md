# My Skills Collections

个人使用的 AI Agent Skills 收藏、镜像与定制仓库。

这个仓库用于集中保存我实际会使用或准备改造的 Skills。部分 Skill 会保持与上游一致，部分则会在保留来源与版本信息的前提下，根据个人工作流进行修改。

> 本仓库不是各上游项目的官方镜像。若本地 Skill 已进行定制，其行为可能与上游版本不同。

**Last status check:** 2026-09-02

## Skills

| Skill | 用途 | Local | Upstream | 同步状态 | 本地状态 |
| --- | --- | --- | --- | --- | --- |
| [`vue-best-practices`](./skills/vue-best-practices/) | Vue 3 / Composition API / uni-app Vue 开发实践 | **v18.6.0-personal.6** | **v18.0.0** | 🔵 **Customized** | ✅ **Active** |
| [`grilling`](./skills/grilling/) | 对计划、需求、架构和决策进行追问、压力测试及执行前歧义澄清 | **v1.2.0-personal.3** | **unversioned @ 85f83d3** | 🔵 **Customized** | ✅ **Active** |

## Skill Details

### vue-best-practices

Vue 3 开发工作流与最佳实践 Skill。当前个人版本重点关注业务代码可维护性、按任务加载规则、跨平台兼容、异步 UI 行为和依赖纪律。

- **Local path:** [`skills/vue-best-practices/`](./skills/vue-best-practices/)
- **Upstream:** [`vuejs-ai/skills`](https://github.com/vuejs-ai/skills/tree/main/skills/vue-best-practices)
- **Upstream branch:** `main`
- **Local version:** `18.6.0-personal.6`
- **Based on upstream version:** `18.0.0`
- **Sync state:** Customized
- **License:** MIT
- **Upstream repository HEAD when baseline was checked:** `c9d355ff23f654309dd02006be671859df0a134c`
- **Upstream baseline SKILL.md blob:** `feacd704fc48310744f8f8791e318343ea8ab1cb`
- **Upstream baseline references/ tree:** `d3f4b86fa1ad5a259e3a58dc6ed1fc0958ac7dd0`
- **Imported into this repository:** 2026-08-31
- **Customization started:** 2026-08-31
- **Last local review:** 2026-09-02

#### Current customizations

1. **Stability-driven JS / JSDoc / TS tiers**
    - volatile business code defaults to JavaScript
    - moderately stable shared code defaults to JavaScript with optional JSDoc
    - stable contract-heavy foundation code may prefer TypeScript
    - language/architecture migration is never an incidental refactor

2. **Mandatory four-space formatting**
    - all edited hand-maintained source/config files use four ASCII spaces
    - legacy 2-space/mixed files are normalized when edited
    - existing project formatting tools are aligned when necessary so they do not revert edited source

3. **Async request/UI policy**
    - Promise chaining is preferred for ordinary API/interface request flow
    - Axios projects prefer `utils/request.js -> api/<feature>.js -> page/component` layering
    - request wrappers own transport/interceptor concerns; API modules own endpoint definitions; pages/components own UI loading locks
    - conflicting UI actions are locked while requests are pending
    - uni-app native loading is hidden before a following toast; application-level locks remain a `finally()` cleanup concern

4. **Task-scoped reference loading and relaxed abstraction**
    - references are loaded only when relevant instead of preloading four large core files for every task
    - component/composable extraction requires a real responsibility, reuse, lifecycle, or maintenance boundary
    - no fixed CRUD component recipe, UI-section count, component-depth threshold, or list-size threshold

5. **uni-app platform gate**
    - H5/Web, App, and mini-program targets are treated as different runtimes
    - DOM, routing, refs, networking, Teleport, Transition, KeepAlive, Suspense, and other platform-sensitive guidance must pass compatibility checks first
    - Axios is allowed on App/mini-program targets when the actual project/runtime is compatible; non-H5 is not an automatic reason to switch transport
    - `uni.request` is used when there is a concrete compatibility/platform-network reason or when it is already the project standard

6. **Dependency-conservative policy with approved ecosystem exceptions**
    - Pinia is an approved/default Vue app-level state solution when a genuine global store boundary exists
    - Axios is an approved request-layer dependency for Vue and compatible uni-app targets
    - existing request/store architecture is not replaced incidentally
    - other third-party libraries still require an explicit technical reason or an existing project dependency

7. **Upstream rule cleanup**
    - primitive state defaults to normal `ref()`; `shallowRef()` is reserved for intentionally shallow/opaque/large root-replacement state
    - Suspense is treated as experimental
    - performance advice is profiling/evidence-driven instead of based on fake-precise thresholds
    - all references have been reviewed and examples normalized to the personal conventions

This Skill is intentionally different from upstream. Upstream version/commit/tree information above is retained as the baseline for future comparison and selective rebasing.

### grilling

对计划、需求、架构、工作流和产品决策进行追问与压力测试，并在执行类任务中对高返工风险歧义进行开工前澄清的 Skill。保留上游 `design tree + frontier + round` 核心机制，同时针对 Agent Ask 工具、执行前澄清、长会话和中文沟通进行了个人化。

- **Local path:** [`skills/grilling/`](./skills/grilling/)
- **Upstream:** [`mattpocock/skills`](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling)
- **Upstream branch:** `main`
- **Local version:** `1.2.0-personal.3`
- **Upstream version:** unversioned
- **Sync state:** Customized
- **License:** MIT
- **Upstream baseline commit:** `85f83d3fde1d3a90d5c9a657f6998c79a6c37308`
- **Upstream baseline SKILL.md blob:** `8ca78c6d8f901aab0c5a1f896034b70e666ff2a3`
- **Upstream baseline agents/openai.yaml blob:** `ddbdb96139c0c1dfe6bca698f39d0465674b8a39`
- **Imported and customized:** 2026-09-02
- **Last local review:** 2026-09-02

#### Current customizations

1. **Two activation modes**
    - explicit Grill / stress-test / requirement-clarification requests run the full material design tree
    - normal planning/execution tasks run only a short preflight when unresolved ambiguity could materially change scope, behavior, architecture, irreversible actions, or acceptance criteria
    - merely mentioning a plan/design/requirement is not enough to trigger the Skill
    - execution preflight resumes the original task automatically once the blocking material ambiguity is resolved

2. **Materiality-based questioning**
    - ask when different reasonable answers would meaningfully change the result or create significant rework
    - facts, cheap reversible details, naming, formatting, and choices already covered by project/user conventions are not separate user questions
    - uncertainty by itself is not a reason to ask

3. **Plain-language, recommendation-led decisions**
    - use the user's language and keep every question easy to scan
    - one underlying decision per question; avoid unnecessary jargon
    - every material question gets one concrete recommended answer with a short reason
    - settled user policies, existing project behavior, and user-designated reference implementations are strong recommendation defaults

4. **Facts are researched, not delegated back to the user**
    - inspect code, files, docs, connected tools, and current external facts before asking
    - only ask the user for real decisions/preferences or facts that only the user can know
    - unresolved research blocks only dependent branches, not unrelated work

5. **Ask-tool-first interaction**
    - when the host Agent exposes an Ask/AskUserQuestion-style tool, use it instead of rendering chat questionnaires
    - use single-select by default; use multi-select only for genuinely additive choices
    - rely on the host UI's custom/free-text answer path instead of inventing a fake `Other` option when the UI already provides one
    - fill each Ask invocation with as many independent frontier questions as the host schema comfortably supports
    - plain-text A/B/C questions and compact batch replies are fallback behavior only when no usable Ask tool exists

6. **No decorative emoji**
    - question titles, options, recommendations, checkpoints, summaries, and text fallbacks do not add decorative emoji/pictograms
    - emoji is used only when the content itself requires it or literal user content must be preserved

7. **Decision ledger and conflict handling**
    - preserve settled answers and do not repeatedly ask the same decision in narrower forms
    - if a later answer conflicts with a settled policy, point out the conflict and reopen only the affected branch
    - long explicit Grill sessions use compact decision checkpoints to reduce decision loss from context compression

8. **Material completeness without over-grilling**
    - explicit Grill mode leaves no material branch silently assumed
    - execution preflight asks only questions that block or substantially change the current task
    - low-impact hypothetical edges and decisions implied by prior policies do not deserve separate questions

## Status Legend

| 状态 | 含义 |
| --- | --- |
| 🟢 **Exact snapshot** | 本地 Skill 与记录的上游版本完全一致 |
| 🔵 **Customized** | 基于上游版本进行了有意的本地修改 |
| 🟠 **Upstream updated** | 上游已有新版本或新内容，本地尚未同步/重基 |
| ⚪ **Local only** | 自建 Skill，没有对应上游来源 |
| 🔴 **Needs review** | 来源、版本或兼容性需要重新核对 |

## Tracking Policy

为了避免“版本号相同但内容已经不同”的情况，本仓库尽量同时记录：

1. Skill 自身的本地版本号；
2. 它所基于的上游版本、revision 或 commit；
3. 上游仓库与分支；
4. 上游基线的 commit / tree / blob 信息；
5. 当前本地定制内容；
6. 最近一次状态检查日期。

对已经进入 **Customized** 状态的 Skill，不会直接用新的 upstream 内容覆盖本地修改。更新上游时应先比较差异，再选择性吸收适合当前个人工作流的变化。

## Repository Layout

```text
my-skills-collections/
├── README.md
└── skills/
    ├── grilling/
    │   ├── SKILL.md
    │   └── agents/
    │       └── openai.yaml
    └── vue-best-practices/
        ├── SKILL.md
        └── references/
            └── ...
```

后续新增 Skill 时统一放入 `skills/<skill-name>/`，并在本 README 的 Skills 表格中登记来源、版本和同步状态。

## Sources & Licenses

第三方 Skill 的原作者、来源和许可证归各自上游项目所有。本仓库在保留和修改第三方 Skill 时，会尽量保留其原始 license metadata 与来源信息。

当前收录的第三方 Skill：

- `vue-best-practices` — [`vuejs-ai/skills`](https://github.com/vuejs-ai/skills) — MIT
- `grilling` — [`mattpocock/skills`](https://github.com/mattpocock/skills) — MIT
