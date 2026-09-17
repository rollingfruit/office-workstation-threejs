# office-workstation-threejs

根据工位照片设计整理方案，生成可以离线打开、旋转、缩放和导出 PNG 的 Three.js HTML。

## 安装

将本仓库完整复制到 Codex 用户技能目录下的 `office-workstation-threejs` 文件夹：

- macOS / Linux：`~/.codex/skills/office-workstation-threejs`
- Windows：`%USERPROFILE%\.codex\skills\office-workstation-threejs`

设置了 `CODEX_HOME` 时使用该目录下的 `skills`。新建任务并确认技能已被发现。技能的建模流程不依赖特定聊天应用或部署服务；其他支持 SKILL.md 的 Agent 可按其技能加载方式使用，尚未逐一验证兼容性。

## 使用

请自行保存工位照片，并提供 Agent 所在设备可访问的图片路径或图片附件。本仓库不附带原图。

例如：

> 使用 office-workstation-threejs SKILL，读取 `/Users/你的用户名/Pictures/工位.png`，把工位整理得更简洁，保留原有设备，给我可交互 HTML、预览图和布局说明。

也可以追加预算、风格等约束。购买建议须另外调研，示例模板不包含实时商品价格服务。

Agent 先实际查看照片，再修改场景描述、Three.js 几何和页面文案，最后构建并验证。模板中的转角桌与设备组合仅为可编辑示例，需要根据每张新图调整。单张照片生成的是尺寸估算的概念方案，并非精确测量或自动三维重建。

## 手动运行示例

```sh
python scripts/scaffold.py --out ../workstation-demo --reference "/Users/你的用户名/Pictures/工位.png"
cd ../workstation-demo
npm ci
npm run build
```

Windows 的创建命令示例（将用户名和路径替换为实际值）：

```powershell
py -3 scripts/scaffold.py --out ..\workstation-demo --reference "C:\Users\你的用户名\Pictures\工位.png"
```

输入目前要求 PNG，其他格式请先转换。图片会复制到生成工程的 `reference.png`，并在构建时内嵌到 HTML 中。用户图片无需放入技能仓库。

用 Edge 或 Chrome 打开 `dist/workstation.html`。构建需要 Python、Node.js/npm 和依赖下载；最终 HTML 不需要联网。

## 上传失败时

最新版要求：文件已生成但上传失败，摘要应包含核验后的绝对路径、所属设备及打开方式。如果宿主更高优先级指令禁止路径输出，需由宿主解决约束冲突；技能本身不能覆盖它。

## 内容

- `SKILL.md`：工作流、验收和交付约定
- `assets/template/`：Three.js 源码与锁定依赖
- `scripts/scaffold.py`：创建独立工程

Three.js 的许可见 `assets/template/THREE-LICENSE.txt`。仓库为公共仓库，不附带用户工位照片。
