# MooaToon 项目规则

## 项目简介

`C:\MooaToon` 是 MooaToon 的安装、更新、构建、打包及 GitHub 发布工具仓库，主要通过 Windows 批处理脚本和 Python 工具完成相关流程。

## 关联项目与目录

- `C:\MooaToon`：当前电脑上的项目根目录，包含安装工具、发布工具以及引擎/项目工作副本。
- `C:\MooaToon\MooaToon-Engine`：MooaToon 引擎开发目录，是引擎源码修改和本地构建的主要位置。
- `C:\MooaToon\MooaToon-Project`：MooaToon 项目开发目录，也是本地运行和打包项目的工作副本。
- `C:\MooaToon\MooaToon-Engine\Engine\Plugins\MooaToonThirdparty\VRM4U`：VRM4U 插件，作为 Git submodule 管理，当前位于引擎仓库内。
- `C:\MooaToon\MooaToon-Engine\Engine\Plugins\MooaToonThirdparty\VibeUE`：VibeUE 插件，作为 Git submodule 管理，当前位于引擎仓库内。
- `C:\MooaToon\MooaToon-Engine\Engine\Plugins\MooaToonThirdparty\KawaiiPhysics`：KawaiiPhysics 在引擎中的使用路径；这是一个 Junction，指向下面的外部插件源目录。
- `C:\Users\jason\Workspace\KawaiiPhysics_MooaToon`：KawaiiPhysics 上游 fork 仓库，用于获取和合并上游更新；插件源目录为 `Plugins\KawaiiPhysics`。
- `C:\Users\jason\Workspace\KawaiiPhysics_MooaToon\Plugins\KawaiiPhysics`：KawaiiPhysics 插件源目录，当前由引擎目录中的 Junction 使用。
- `C:\Users\jason\Workspace\jason-ma-0012.github.io`：MooaToon 官方文档仓库（Docusaurus 站，发布于 https://mooatoon.com/）。`docs\` 存中文文档，`i18n\en\` 存英文翻译。

## 本仓库中的发布工作副本

发布工具位于 `C:\MooaToon\ReleaseTools`，并使用 `C:\MooaToon\MooaToon-Engine` 和 `C:\MooaToon\MooaToon-Project` 完成构建、压缩和发布。

## 文档仓库结构（`C:\Users\jason\Workspace\jason-ma-0012.github.io`）

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

- 引擎源码修改优先在 `C:\MooaToon\MooaToon-Engine` 进行；项目修改在 `C:\MooaToon\MooaToon-Project` 进行。
- 插件都作为MooaToon内置插件与引擎一起发布.
- VRM4U的改动需要先提交到VRM4U仓库, 引擎测提交Submodule的Commit变更即可.
- KawaiiPhysics 的 Junction 是本机开发环境配置，实际源码在 `C:\Users\jason\Workspace\KawaiiPhysics_MooaToon\Plugins\KawaiiPhysics`；KawaiiPhysics 的改动需要同时提交到 `KawaiiPhysics_MooaToon` 和引擎仓库。
- 发布凭据只从系统环境变量读取：优先使用 `MOOATOON_ENGINE_TOKEN`，兼容 `GITHUB_TOKEN`；不得把 token 写入仓库文件、脚本或构建产物。
- 清理、构建、压缩和发布操作应优先使用对应目录下已有的 `.bat` 入口，并在操作后检查 Git 状态和生成物。
- 引擎编译并打开项目统一使用 `C:\MooaToon\_4_0_Build_And_Run_MooaToon_Debug.bat`（从 `C:\MooaToon` 目录执行），构建 `UnrealEditor Win64 Debug` 与 `ShaderCompileWorker Win64 Debug`，并保持硬件 Ray Tracing 启用。编译期间每 15 分钟检查一次编译进度，并确认编译输出中没有报错。
- 文档同步规则：当 AI 改动了文档中已有的内容，或引擎/插件/项目发生会影响文档的变更（如新增、修改、移除内置插件）时，必须同步更新 MooaToon 官方文档仓库 `C:\Users\jason\Workspace\jason-ma-0012.github.io` 中的对应文档；若改动的是中文文档，还需同步更新 `i18n/en` 下的英文翻译，保持中英文内容与结构一致。
- 所有对于官方引擎代码的修改统一用 "// Mooa <描述>" 开始、"// Mooa End" 结束包裹, 便于之后升级.
- 所有对于第三方插件源码的修改也统一用 "// Mooa <描述>" 开始、"// Mooa End" 结束包裹；插件仓库或 submodule 应先提交插件改动，再更新引擎中的 submodule 指针.
- 由于UE项目巨大, 所有大范围修改都应该尽可能广泛搜索收集上下文, 然后生成TODO List并逐个执行, 最后逐个验证以确保无遗漏.
- 实际工作中若发现本文档有误或缺失, 或有新的通用经验, 需及时更新本文.
