# MooaRel 项目规则

## 项目简介

MooaRel 是 MooaToon 的安装和发布工具项目，主要通过 Windows 批处理脚本和 Python 工具完成安装、更新、构建、打包及 GitHub 发布流程。

## 关联项目与目录

- `E:\MooaRel`：MooaToon 的安装和发布工具。
- `E:\Mooa\MooaToon-Engine`：MooaToon 引擎开发目录，是引擎源码修改的主要位置。
- `E:\Mooa\MooaToon-Engine\Engine\Plugins\MooaToonThirdparty\VRM4U`：VRM4U 插件，作为 Git submodule 管理。
- `E:\WorkSpace\_UE\KawaiiPhysics_MooaToon`：KawaiiPhysics 上游 fork 仓库，用于获取和合并上游更新。
- `E:\WorkSpace\_UE\KawaiiPhysics_MooaToon\Plugins\KawaiiPhysics`：KawaiiPhysics 插件源目录。
- `E:\Mooa\MooaToon-Engine\Engine\Plugins\MooaToonThirdparty\KawaiiPhysics`：KawaiiPhysics 当前开发目录；通过 Junction 连接到上面的插件源目录，日常开发直接使用此路径。

## 本仓库中的发布工作副本

- `E:\MooaRel\MooaToon-Engine`：用于构建和打包的引擎工作副本，不是引擎开发源目录。
- `E:\MooaRel\MooaToon-Project`：用于打包 MooaToon 项目的工作副本。

## 基本规则

- 引擎源码修改优先在 `E:\Mooa\MooaToon-Engine` 进行；发布前再同步到 `E:\MooaRel` 的工作副本。
- 插件都作为MooaToon内置插件与引擎一起发布.
- VRM4U的改动需要先提交到VRM4U仓库, 引擎测提交Submodule的Commit变更即可.
- KawaiiPhysics 的 Junction 是本机开发环境配置, KawaiiPhysics的改动需要同时提交到KawaiiPhysics_MooaToon和引擎仓库.
- 发布凭据只从系统环境变量读取：优先使用 `MOOATOON_ENGINE_TOKEN`，兼容 `GITHUB_TOKEN`；不得把 token 写入仓库文件、脚本或构建产物。
- 清理、构建、压缩和发布操作应优先使用对应目录下已有的 `.bat` 入口，并在操作后检查 Git 状态和生成物。
