# My Skills Collections

个人使用的 AI Agent Skills 收藏、镜像与定制仓库。

这个仓库用于集中保存我实际会使用或准备改造的 Skills。部分 Skill 会保持与上游一致，部分则会在保留来源与版本信息的前提下，根据个人工作流进行修改。

> 本仓库不是各上游项目的官方镜像。若本地 Skill 已进行定制，其行为可能与上游版本不同。

**Last status check:** 2026-08-31

## Skills

| Skill | 用途 | Local | Upstream | 同步状态 | 本地状态 |
| --- | --- | --- | --- | --- | --- |
| [`vue-best-practices`](./skills/vue-best-practices/) | Vue 3 / Composition API 开发最佳实践 | **v18.2.0-personal.2** | **v18.0.0** | 🔵 **Customized** | ✅ **Active** |

## Skill Details

### vue-best-practices

Vue 3 开发工作流与最佳实践 Skill，覆盖响应式、SFC、组件数据流、Composables、状态管理、异步接口交互、异步组件、动画及性能优化等主题。

- **Local path:** [`skills/vue-best-practices/`](./skills/vue-best-practices/)
- **Upstream:** [`vuejs-ai/skills`](https://github.com/vuejs-ai/skills/tree/main/skills/vue-best-practices)
- **Upstream branch:** `main`
- **Local version:** `18.2.0-personal.2`
- **Based on upstream version:** `18.0.0`
- **Sync state:** Customized
- **License:** MIT
- **Upstream repository HEAD when baseline was checked:** `c9d355ff23f654309dd02006be671859df0a134c`
- **Upstream baseline SKILL.md blob:** `feacd704fc48310744f8f8791e318343ea8ab1cb`
- **Upstream baseline references/ tree:** `d3f4b86fa1ad5a259e3a58dc6ed1fc0958ac7dd0`
- **Imported into this repository:** 2026-08-31
- **Customization started:** 2026-08-31

#### Current customizations

1. **Stability-driven JavaScript / TypeScript policy**
    - **Business / volatile:** default to JavaScript for pages, route views, CRUD/forms/dashboards, feature-specific components and feature-specific composables.
    - **Shared / moderately stable:** default to JavaScript with optional JSDoc at meaningful public boundaries.
    - **Foundation / stable contract:** prefer TypeScript for low-change, broadly reused, contract-heavy components/composables/infrastructure.
    - Never migrate JavaScript ↔ TypeScript as an incidental refactor; migration must be explicit or technically justified.
    - Existing local project conventions take priority when modifying existing files.

2. **Four-space indentation**
    - All authored or edited hand-maintained code uses four ASCII spaces per indentation level.
    - Editing a legacy 2-space or mixed-indentation file also normalizes the entire edited file to four spaces.

3. **Async API/interface interaction policy**
    - Prefer Promise chaining (`then/catch/finally`) for API/interface calls.
    - UI-triggered requests use loading/disabled interaction locks and release them in `finally()`.

This Skill is now intentionally different from upstream. Upstream version/commit/tree information above is retained as the baseline for future comparison and selective rebasing.

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
2. 它所基于的上游版本；
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
    └── vue-best-practices/
        ├── SKILL.md
        └── references/
            └── async-interface-ui.md
```

后续新增 Skill 时统一放入 `skills/<skill-name>/`，并在本 README 的 Skills 表格中登记来源、版本和同步状态。

## Sources & Licenses

第三方 Skill 的原作者、来源和许可证归各自上游项目所有。本仓库在保留和修改第三方 Skill 时，会尽量保留其原始 license metadata 与来源信息。

当前收录的第三方 Skill：

- `vue-best-practices` — [`vuejs-ai/skills`](https://github.com/vuejs-ai/skills) — MIT
