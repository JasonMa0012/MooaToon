# MooaRel 项目规则

## 项目简介

MooaRel 是 MooaToon 的安装和发布工具项目，主要通过 Windows 批处理脚本和 Python 工具完成安装、更新、构建、打包及 GitHub 发布流程。

## 关联项目与目录

- `E:\MooaRel`：MooaToon 的安装和发布工具，及发布用的引擎/项目工作副本。
- `E:\Mooa\`：MooaToon 主开发根目录。
- `E:\Mooa\MooaToon-Engine`：MooaToon 引擎开发目录，是引擎源码修改的主要位置。
- `E:\Mooa\MooaToon-Project`：MooaToon 项目开发目录。
- `E:\Mooa\MooaToon-Engine\Engine\Plugins\MooaToonThirdparty\VRM4U`：VRM4U 插件，作为 Git submodule 管理。
- `E:\Mooa\MooaToon-Engine\Engine\Plugins\MooaToonThirdparty\VibeUE`：VibeUE 插件，作为 Git submodule 管理。
- `E:\Mooa\MooaToon-Engine\Engine\Plugins\MooaToonThirdparty\KawaiiPhysics`：KawaiiPhysics 当前开发目录；通过 Junction 连接到下面的插件源目录，日常开发直接使用此路径。
- `E:\WorkSpace\_UE\KawaiiPhysics_MooaToon`：KawaiiPhysics 上游 fork 仓库，用于获取和合并上游更新。
- `E:\WorkSpace\_UE\KawaiiPhysics_MooaToon\Plugins\KawaiiPhysics`：KawaiiPhysics 插件源目录。
- `E:\WorkSpace\jason-ma-0012.github.io`：MooaToon 官方文档仓库（Docusaurus 站，发布于 https://mooatoon.com/）。`docs/` 存中文文档，`i18n/en/` 存英文翻译。
- `E:\WorkSpace\jasonma0012.github.io`：Hexo 博客仓库（个人博客），**不是** MooaToon 官方文档仓库，注意区分。

## 本仓库中的发布工作副本

- `E:\MooaRel\MooaToon-Engine`：用于构建和打包的引擎工作副本，不是引擎开发源目录。
- `E:\MooaRel\MooaToon-Project`：用于打包 MooaToon 项目的工作副本。

## 文档仓库结构（jason-ma-0012.github.io）

- 根目录为 Docusaurus 站点，`sidebars.js` 从 `docs/` 目录结构自动生成侧边栏。
- `docs/`：中文文档主目录。
  - `docs/GettingStarted/`：开始使用，如 `BuildEnginefromSourceCode.md`、`UseWithOtherPlugins.md`。
  - `docs/MigrateToNewVersion/`：版本迁移文档。
  - `docs/Reference/`：参考文档，`BuiltinPlugins.md` 记录内置插件及内置第三方插件；另有 `ConsoleVariables.md`、`MeshImportSettings.md`、`ProjectAndEditorSettings.md`。
  - `docs/Tutorial/`：教程。
  - `docs/TutorialLegacy/`：旧版（5.0-5.3）教程。
  - `docs/FAQ.md`、`docs/Licence.md`：常见问题与许可协议。
- `i18n/en/docusaurus-plugin-content-docs/current/`：英文翻译，目录结构镜像 `docs/`。
- `blog/`：博客文章。

## 基本规则

- 引擎源码修改优先在 `E:\Mooa\MooaToon-Engine` 进行；发布前再同步到 `E:\MooaRel` 的工作副本。
- 插件都作为MooaToon内置插件与引擎一起发布.
- VRM4U的改动需要先提交到VRM4U仓库, 引擎测提交Submodule的Commit变更即可.
- KawaiiPhysics 的 Junction 是本机开发环境配置, KawaiiPhysics的改动需要同时提交到KawaiiPhysics_MooaToon和引擎仓库.
- 发布凭据只从系统环境变量读取：优先使用 `MOOATOON_ENGINE_TOKEN`，兼容 `GITHUB_TOKEN`；不得把 token 写入仓库文件、脚本或构建产物。
- 清理、构建、压缩和发布操作应优先使用对应目录下已有的 `.bat` 入口，并在操作后检查 Git 状态和生成物。
- 文档同步规则：当 AI 改动了文档中已有的内容，或引擎/插件/项目发生会影响文档的变更（如新增、修改、移除内置插件）时，必须同步更新 MooaToon 官方文档仓库 `E:\WorkSpace\jason-ma-0012.github.io` 中的对应文档；若改动的是中文文档，还需同步更新 `i18n/en` 下的英文翻译，保持中英文内容与结构一致。
