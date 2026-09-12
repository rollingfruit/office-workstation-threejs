# NewLink / Windows daemon 接入

本文件基于 2026-09-11 在 Windows 11 Parallels 环境和本地 `multica-aiwelink` 提交 `05e6ee1` 的穿刺。源码机制与正在运行的二进制可能不一致，使用前检查实际任务环境。

## 输入、技能、结果是三个独立环节

1. 输入：IM 任务中的 Available Files 提供 artifact_id 时，用任务契约中的 `multica artifact download <artifact_id> --name <name>` 下载，再读取真实图片。不要把 artifact_id 当作路径。当前 `pkg/agent/codex.go` 的 turn/start 仅传 text，模型需要主动调用图片工具。Windows CLI `codex exec` 则有 `--image`，不能据此推断 daemon 已接入原生图片参数。
2. 技能：daemon 的 `internal/daemon/local_skills.go` 从 `$CODEX_HOME/skills`（默认用户 `.codex/skills`）发现本地 Codex 技能。任务可能使用独立 CODEX_HOME，由 runtime materialize 选中的技能。源码 `execenv/codex_user_skills.go` 会把用户 SKILL 复制到每个任务的 CODEX_HOME；`execenv.go:hydrateCodexSkills` 中工作区同名技能优先覆盖。本机 Codex app-server 的 skills/list 已验证能发现此技能，但运行中的 daemon 版本和 3D-builder 的新任务是否完成注入仍需 IM 验证。
3. 结果：在已授权交付的 IM 任务中，上传最终 HTML、预览 PNG：`multica artifact upload <path>`，核对成功回执，再报告交付。若上传失败且最终文件已生成，按 SKILL.md 的“上传失败时的本地结果交付”提供经核验的绝对路径和打开方式，并明确未上传成功。不要上传原图、临时文件和中间产物。没有 IM 发送授权的本地研究只生成可下载文件，不自行发消息。

## Parallels 路径与账户

- macOS 的 `/Users/.../Parallels/Windows 11.pvm` 是虚拟机容器，不是直接拼接 Windows 文件路径的挂载盘。
- 本次确认 Windows 可读 `\\Mac\Home\Downloads\工位.png`。共享目录是否开放需要 `Test-Path` 实测，不要假定所有 Mac 目录均共享。
- `prlctl exec "Windows 11"` 默认可能是 SYSTEM；检查 `$env:USERPROFILE`。`--current-user` 可在当前桌面用户下执行，避免把技能或结果写到 systemprofile。
- 本次 NewLink：`C:\Program Files (x86)\NewLink\NewLink.exe`；Codex CLI 为 0.151.0 ARM64，位于用户 `.codex/packages/standalone/releases/.../bin/codex.exe`。不要将此版本路径硬编码为通用依赖，运行时重新发现。
- 单 HTML 内嵌 Three.js 的 IIFE bundle 与原图，避免 file:// 下 ES module、跨文件 fetch 和 CDN 失效。若 WebGL2 不可用，给出明确失败提示并交付已生成 PNG；不要用静态图冒充可交互模型。

生产上架的候选归属是 `plugin-market` 的技能目录；只有附件、技能下发或运行时契约确有缺口时才改 `multica-aiwelink`。研究样例不需要修改 NewLink app.asar 或重启 daemon。


## 上传失败摘要与任务卡片

先完成有限重试；同一错误连续出现时不要无限上传或重新生成已有成果。上传最终失败后，核对文件并准备包含“生成状态、上传错误、完整绝对路径、路径所属设备、打开方式”的摘要。

若当前运行时要求执行 `multica delivery fail --summary <摘要>`，将上述可操作摘要一并传入，最终自然语言答复也保留相同信息。不要先写入只有“临时问题、稍后重试”的失败摘要，因为任务卡片可能只展示该摘要。PowerShell 使用正确引用的字符串变量传给 `--summary`，保留中文、空格和反斜杠；不得把路径当命令执行。

注意：已观察到的 daemon 自动生成 AGENTS.md 曾禁止输出工作区绝对路径，并要求隐藏运行时路径。这是独立于 SKILL 的运行时约束。本技能中的本地交付约定不能覆盖更高优先级指令；如果该限制仍适用，应报告冲突，需由运行时维护方对本技能的本地结果交付场景配置允许规则。不要宣称只安装本技能即可保证 NewLink 卡片显示本地路径。
