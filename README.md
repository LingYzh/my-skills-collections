# My Skills Collections

个人使用的 AI Agent Skills 收藏、镜像、定制与分发仓库。

根目录 `skills/` 是唯一源码来源。Codex 与 Claude Code marketplace 会把**每个 Skill 单独包装成一个插件**，因此用户可以按需安装单个 Skill；GitHub Release 则只发布与特定 Agent 无关的通用 Skill ZIP。

> 本仓库不是各上游项目的官方镜像。Customized Skill 的行为可能与上游不同。

**Last status check:** 2026-09-02

## Skills

| Skill | 用途 | Local | Upstream | 同步状态 | 本地状态 |
| --- | --- | --- | --- | --- | --- |
| [`vue-best-practices`](./skills/vue-best-practices/) | Vue 3 / Composition API / uni-app Vue 开发实践 | **v18.6.0-personal.6** | **v18.0.0** | 🔵 **Customized** | ✅ **Active** |
| [`grilling`](./skills/grilling/) | 需求/方案压力测试与执行前高返工风险歧义澄清 | **v1.2.0-personal.3** | **unversioned @ 85f83d3** | 🔵 **Customized** | ✅ **Active** |

## Installation

### Codex Plugin Marketplace

添加 marketplace：

```bash
codex plugin marketplace add LingYzh/my-skills-collections --ref master
```

按需安装单个 Skill 插件：

```bash
codex plugin add grilling@lingyzh-skills
codex plugin add vue-best-practices@lingyzh-skills
```

### Claude Code Plugin Marketplace

添加 marketplace：

```bash
claude plugin marketplace add LingYzh/my-skills-collections@master
```

按需安装单个 Skill 插件：

```bash
claude plugin install grilling@lingyzh-skills
claude plugin install vue-best-practices@lingyzh-skills
```

Claude Code 交互界面也可使用：

```text
/plugin marketplace add LingYzh/my-skills-collections
/plugin install grilling@lingyzh-skills
/plugin install vue-best-practices@lingyzh-skills
```

插件内 Skill 会使用宿主的 plugin namespace；启用哪个插件，就只引入对应 Skill。

### Generic Skill ZIP Releases

GitHub tag `v*` 会触发 Release workflow，从根 `skills/<name>/` 分别生成通用 ZIP：

```text
grilling-1.2.0-personal.3.zip
vue-best-practices-18.6.0-personal.6.zip
SHA256SUMS.txt
```

每个 ZIP **不包含 plugin/marketplace 元数据**，并且 ZIP 根目录直接是该 Skill 的内容，例如：

```text
SKILL.md
agents/
references/
...
```

因此可以用于支持普通 Agent Skill ZIP 上传/安装的客户端或 API。OpenAI Skills API 同样接受单个 Skill ZIP 文件作为上传内容。

## Skill Details

### vue-best-practices

- **Local path:** [`skills/vue-best-practices/`](./skills/vue-best-practices/)
- **Upstream:** [`vuejs-ai/skills`](https://github.com/vuejs-ai/skills/tree/main/skills/vue-best-practices)
- **Local version:** `18.6.0-personal.6`
- **Based on upstream:** `18.0.0`
- **Sync state:** Customized
- **License:** MIT
- **Upstream baseline repository HEAD:** `c9d355ff23f654309dd02006be671859df0a134c`
- **Upstream baseline SKILL.md blob:** `feacd704fc48310744f8f8791e318343ea8ab1cb`
- **Upstream baseline references tree:** `d3f4b86fa1ad5a259e3a58dc6ed1fc0958ac7dd0`

主要个人化方向：JS/JSDoc/TS 按稳定度分层、4 格缩进、按任务加载 references、放松过度组件抽象、Axios/Pinia 白名单、request/API/UI 三层调用、异步 UI 锁以及 uni-app 平台兼容规则。

### grilling

- **Local path:** [`skills/grilling/`](./skills/grilling/)
- **Upstream:** [`mattpocock/skills`](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling)
- **Local version:** `1.2.0-personal.3`
- **Upstream version:** unversioned
- **Sync state:** Customized
- **License:** MIT
- **Upstream baseline commit:** `85f83d3fde1d3a90d5c9a657f6998c79a6c37308`
- **Upstream baseline SKILL.md blob:** `8ca78c6d8f901aab0c5a1f896034b70e666ff2a3`
- **Upstream baseline agents/openai.yaml blob:** `ddbdb96139c0c1dfe6bca698f39d0465674b8a39`

主要个人化方向：Ask-tool-first、完整 Grill 与执行前 preflight 双模式、只询问 material ambiguity、每题给推荐、事实自己查、决策 ledger、长会话 checkpoint，以及禁止非必要装饰 emoji。

## Distribution Architecture

```text
skills/                              # source of truth
├── grilling/
└── vue-best-practices/

plugins/                             # generated, one Skill per plugin
├── grilling/
│   ├── .codex-plugin/plugin.json
│   ├── .claude-plugin/plugin.json
│   └── skills/grilling/
└── vue-best-practices/
    ├── .codex-plugin/plugin.json
    ├── .claude-plugin/plugin.json
    └── skills/vue-best-practices/

.agents/plugins/marketplace.json     # Codex marketplace
.claude-plugin/marketplace.json      # Claude Code marketplace
```

插件目录和 marketplace manifest 都是分发产物。**不要直接编辑 `plugins/<name>/skills/`。** 修改根 `skills/<name>/` 后运行：

```bash
python scripts/sync-plugins.py
```

仅检查：

```bash
python scripts/sync-plugins.py --check
```

CI 会在 `master` push / pull request 时检查根 Skill 与所有插件副本、两个 marketplace manifest 是否一致。

## Release

发布新的合集 Release 时创建 `v*` tag 即可；`.github/workflows/release-skills.yml` 会调用：

```bash
python scripts/package-skills.py
```

然后创建/更新对应 GitHub Release 并上传所有独立 Skill ZIP 与 `SHA256SUMS.txt`。

Release tag 是**收藏仓库版本**，Skill 自己继续使用各自 frontmatter 中的本地版本号，两者互不混用。

## Status Legend

| 状态 | 含义 |
| --- | --- |
| 🟢 **Exact snapshot** | 本地 Skill 与记录的上游版本完全一致 |
| 🔵 **Customized** | 基于上游版本进行了有意的本地修改 |
| 🟠 **Upstream updated** | 上游已有新版本或内容，本地尚未选择性吸收 |
| ⚪ **Local only** | 自建 Skill，没有对应上游来源 |
| 🔴 **Needs review** | 来源、版本或兼容性需要重新核对 |

## Sources & Licenses

- `vue-best-practices` — [`vuejs-ai/skills`](https://github.com/vuejs-ai/skills) — MIT
- `grilling` — [`mattpocock/skills`](https://github.com/mattpocock/skills) — MIT

第三方 Skill 的原作者、来源和许可证归各自上游项目所有；本仓库保留来源与上游基线信息，以便后续选择性同步。
