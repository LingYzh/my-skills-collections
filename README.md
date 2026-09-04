# My Skills Collections

个人使用的 AI Agent Skills 收藏、镜像、定制与分发仓库。

根目录 `skills/` 既是 Skill 源码，也是 Codex / Claude Code 单 Skill 插件本体。每个 Skill 都可以从 marketplace 独立安装；GitHub Release 则只发布与特定 Agent 无关的通用 Skill ZIP。

> 本仓库不是各上游项目的官方镜像。Customized Skill 的行为可能与上游不同。

**Last status check:** 2026-09-04

## Skills

| Skill | 用途 | Local | Upstream | 同步状态 | 本地状态 |
| --- | --- | --- | --- | --- | --- |
| [`vue-best-practices`](./skills/vue-best-practices/) | Vue 3 / Composition API / uni-app Vue 开发实践 | **v18.6.0-personal.6** | **v18.0.0** | 🔵 **Customized** | ✅ **Active** |
| [`grilling`](./skills/grilling/) | 需求/方案压力测试与执行前高返工风险歧义澄清 | **v1.2.0-personal.3** | **unversioned @ 85f83d3** | 🔵 **Customized** | ✅ **Active** |
| [`powershell-windows-cli`](./skills/powershell-windows-cli/) | PowerShell 7 / Windows PowerShell 5.1 / CMD Agent 使用规范 | **v1.0.0-snapshot.1** | **snapshot @ 90a5953** | 🟢 **Snapshot** | ✅ **Active** |

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
codex plugin add powershell-windows-cli@lingyzh-skills
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
claude plugin install powershell-windows-cli@lingyzh-skills
```

Claude Code 交互界面也可使用：

```text
/plugin marketplace add LingYzh/my-skills-collections
/plugin install grilling@lingyzh-skills
/plugin install vue-best-practices@lingyzh-skills
/plugin install powershell-windows-cli@lingyzh-skills
```

插件内 Skill 会使用宿主的 plugin namespace；启用哪个插件，就只引入对应 Skill。

### Generic Skill ZIP Releases

GitHub tag `v*` 会触发 Release workflow，从根 `skills/<name>/` 分别生成通用 ZIP：

```text
grilling-1.2.0-personal.3.zip
vue-best-practices-18.6.0-personal.6.zip
powershell-windows-cli-1.0.0-snapshot.1.zip
SHA256SUMS.txt
```

每个 ZIP 会排除 `.codex-plugin/` 和 `.claude-plugin/`，ZIP 根目录直接是通用 Skill 内容：

```text
SKILL.md
agents/
references/
...
```

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

### powershell-windows-cli

- **Local path:** [`skills/powershell-windows-cli/`](./skills/powershell-windows-cli/)
- **Upstream:** [`UncertaintyDeterminesYou4ndMe/powershell-windows-cli-agent-skill`](https://github.com/UncertaintyDeterminesYou4ndMe/powershell-windows-cli-agent-skill)
- **Local version:** `1.0.0-snapshot.1`
- **Upstream version:** unversioned
- **Sync state:** Snapshot
- **License:** MIT
- **Upstream baseline commit:** `90a59539db1d7b4406a32cd7b337e76bbe7d6a3c`
- **Upstream baseline SKILL.md blob:** `7c9d88617131f09b83502533b7a839dc0083650e`
- **Upstream baseline references tree:** `1437dca59e89040a467a3247f2b9956cc02cb240`

当前仅做分发适配：保留上游 Skill 正文、references、helper scripts 与 evals，补充本仓库版本 metadata 和 Codex / Claude plugin manifest；尚未开始个人化审计。

## Distribution Architecture

```text
skills/
├── grilling/
│   ├── SKILL.md
│   ├── agents/
│   ├── .codex-plugin/plugin.json
│   └── .claude-plugin/plugin.json
├── powershell-windows-cli/
│   ├── SKILL.md
│   ├── references/
│   ├── scripts/
│   ├── evals/
│   ├── .codex-plugin/plugin.json
│   └── .claude-plugin/plugin.json
└── vue-best-practices/
    ├── SKILL.md
    ├── references/
    ├── .codex-plugin/plugin.json
    └── .claude-plugin/plugin.json

.agents/plugins/marketplace.json     # Codex marketplace -> ./skills/<name>
.claude-plugin/marketplace.json      # Claude Code marketplace -> ./skills/<name>
```

这里没有生成的 Skill mirror。`skills/<name>/` 同时承担三种角色：

1. 通用 Agent Skill 源码；
2. Codex 单 Skill plugin root；
3. Claude Code 单 Skill plugin root。

因此日常修改 Skill 时**不需要运行同步脚本**。修改 `skills/<name>/` 后可以直接提交；只有在 Skill 版本号变化时，需要同步修改该目录下两个 plugin manifest 的版本字段以及 marketplace 中 Claude 条目的版本字段。

CI 只验证 marketplace / plugin manifest 结构和通用 ZIP 内容，不生成或要求提交任何 Skill 副本。

## Release

发布新的合集 Release 时创建 `v*` tag 即可；`.github/workflows/release-skills.yml` 会调用：

```bash
python scripts/package-skills.py
```

然后创建/更新对应 GitHub Release，并上传所有独立 Skill ZIP 与 `SHA256SUMS.txt`。

Release tag 是**收藏仓库版本**，Skill 自己继续使用各自 frontmatter 中的本地版本号，两者互不混用。

## Status Legend

| 状态 | 含义 |
| --- | --- |
| 🟢 **Exact snapshot** | 本地 Skill 与记录的上游版本完全一致 |
| 🟢 **Snapshot** | 上游 Skill 内容保持不变，仅增加本仓库分发 metadata / host manifest |
| 🔵 **Customized** | 基于上游版本进行了有意的本地修改 |
| 🟠 **Upstream updated** | 上游已有新版本或内容，本地尚未选择性吸收 |
| ⚪ **Local only** | 自建 Skill，没有对应上游来源 |
| 🔴 **Needs review** | 来源、版本或兼容性需要重新核对 |

## Sources & Licenses

- `vue-best-practices` — [`vuejs-ai/skills`](https://github.com/vuejs-ai/skills) — MIT
- `grilling` — [`mattpocock/skills`](https://github.com/mattpocock/skills) — MIT
- `powershell-windows-cli` — [`UncertaintyDeterminesYou4ndMe/powershell-windows-cli-agent-skill`](https://github.com/UncertaintyDeterminesYou4ndMe/powershell-windows-cli-agent-skill) — MIT

第三方 Skill 的原作者、来源和许可证归各自上游项目所有；本仓库保留来源与上游基线信息，以便后续选择性同步。
