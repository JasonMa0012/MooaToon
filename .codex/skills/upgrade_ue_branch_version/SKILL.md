---
name: upgrade-ue-branch-version
description: Used when users need to upgrade UE branch versions, for example from UE 5.7 to UE 5.8.
---

# UE 分支升级流程

本 Skill 只记录可复用的迁移流程。示例中的路径均为相对路径：

- `<engine-root>`：引擎 Git 仓库根目录，下面的 `Engine/`、`diff.patch` 和 `PatchConflicts.md` 位于此处。
- `<workspace-root>`：包含引擎仓库、项目仓库、`OtherTools/` 和 `UpgradeEvidence/` 的工作区根目录。
- `<kawaii-fork-root>`：本机 KawaiiPhysics fork 的仓库根目录；插件源固定在 `<kawaii-fork-root>/Plugins/KawaiiPhysics`。

默认 Epic 远端名称为 `epic`，用户定制远端名称为 `origin`。除非用户明确要求，不执行 `git commit` 或 `git push`。

## 1. 固定基线和工作区状态

从 `<engine-root>` 开始，记录当前分支、目标 Epic 引用、HEAD 和 merge-base：

```powershell
git status --porcelain --untracked-files=all
git branch --show-current
git rev-parse HEAD
git rev-parse refs/remotes/epic/<version>
git merge-base refs/remotes/epic/<version> HEAD
```

确认官方引用是基线的祖先，区分用户已有修改、待迁移补丁和未跟踪文件。分支存在不等于用户已确认目标版本。

## 2. 生成差异补丁

优先从 `<engine-root>` 调用 `../OtherTools/GenerateDiff.bat`。脚本顶部可以配置：

- `REPOSITORY_PATH`：相对于脚本目录的引擎仓库路径；
- `EPIC_REMOTE`、`BASE_BRANCH`、`TARGET_BRANCH`；`TARGET_BRANCH` 只显示和记录，不参与比较；
- `EXCLUDE_PATHS`：每个排除项单独追加一行，或通过换行/分号传给 PowerShell；
- `OUTPUT_PATH`：相对于引擎仓库根目录的输出文件。

默认排除 `Engine/Plugins/MooaToonThirdparty` 和 `Engine/Build/Commit.gitdeps.xml`。补丁直接覆盖旧文件，不创建备份。脚本必须在导出范围存在未提交或未跟踪文件时停止，不能静默遗漏工作区修改。

通用导出命令：

```powershell
git diff --binary --full-index --no-ext-diff --no-textconv --output=diff.patch epic/<from-version> HEAD -- . ':(exclude)Engine/Plugins/MooaToonThirdparty' ':(exclude)Engine/Build/Commit.gitdeps.xml'
```

生成后执行：

```powershell
git apply --reverse --check --binary diff.patch
git apply --stat diff.patch
Get-FileHash -LiteralPath diff.patch -Algorithm SHA256
```

反向检查只证明补丁对应当前源码，不证明它能无冲突地应用到新版引擎。

## 3. 切换新版 Epic 分支

用户已拉取目标分支时直接使用本地 `refs/remotes/epic/<target-version>`，不重复 fetch。切换前再次检查工作区；仅准备源码迁移时可临时跳过 GitDependencies 钩子：

```powershell
git -c core.hooksPath=NUL switch --detach epic/<target-version>
git status --porcelain --untracked-files=all
```

确认 HEAD 与目标引用一致后再应用补丁。Git 工作区干净不代表外部插件、GitDependencies 或 Junction 已准备好。

## 4. 应用补丁并建立冲突台账

从 `<engine-root>` 调用 `../OtherTools/ApplyPatch.bat`。入口使用同目录的 `ApplyPatch.py`，先确认目标 HEAD 和干净工作区，再运行：

```text
git apply --reject --binary --whitespace=nowarn diff.patch
```

保留以下产物：

- `ApplyPatch.log`：完整 Git 输出；
- `PatchConflicts.md`：每个冲突文件及完成标记；
- `PatchConflicts/NNNN.patch`：没有生成 `.rej` 的整文件冲突。

`git apply` 返回 1 可能只是拒绝了部分 hunk，必须逐项分析。`error: while searching for:` 只是后续失败块的上下文。脚本应拒绝对已有应用产物再次应用；只修复清单时使用 `python ../OtherTools/ApplyPatch.py --inventory-only`。如果升级台账要求保留历史冲突产物，不因 `.rej` 仍存在就把已处理项标为未完成。

## 5. 恢复 MooaToon 第三方插件

在编译、旧材质验证和 Sequence 验证前恢复两个插件。

### VRM4U submodule

路径必须是 `Engine/Plugins/MooaToonThirdparty/VRM4U`，远程必须是：

```text
https://github.com/JasonMa0012/VRM4U_MooaToon.git
```

首次添加：

```powershell
git submodule add https://github.com/JasonMa0012/VRM4U_MooaToon.git Engine/Plugins/MooaToonThirdparty/VRM4U
```

已有 `.gitmodules` 条目或本地模块缓存时：

```powershell
git submodule sync -- Engine/Plugins/MooaToonThirdparty/VRM4U
git submodule update --init --recursive -- Engine/Plugins/MooaToonThirdparty/VRM4U
```

检查 `git submodule status`、子模块远程 URL、插件 `.uplugin` 和子模块工作区状态。VRM4U 源码修改必须先在插件仓库提交，再更新引擎仓库中的 gitlink；本迁移默认不提交。

### KawaiiPhysics Junction

路径 `Engine/Plugins/MooaToonThirdparty/KawaiiPhysics` 必须是 Junction，目标为用户现有 fork 的 `Plugins/KawaiiPhysics`。不要复制源码，也不要把本机绝对路径写进 Skill、项目配置或仓库文件。PowerShell 示例：

```powershell
$engineRoot = (Resolve-Path '.').Path
$kawaiiForkRoot = (Resolve-Path $env:KAWAII_PHYSICS_FORK).Path
$source = Join-Path $kawaiiForkRoot 'Plugins/KawaiiPhysics'
$target = Join-Path $engineRoot 'Engine/Plugins/MooaToonThirdparty/KawaiiPhysics'
if (-not (Test-Path -LiteralPath $source -PathType Container)) { throw "KawaiiPhysics source is missing" }
if (Test-Path -LiteralPath $target) { throw "Junction target already exists" }
New-Item -ItemType Junction -Path $target -Target $source
Get-Item -LiteralPath $target | Format-List FullName,Attributes,LinkType,Target
```

确认目标包含 `KawaiiPhysics.uplugin`，并检查 fork 工作区状态。Junction 是本机开发环境配置；KawaiiPhysics 源码修改需要在 fork 仓库和引擎工作区分别管理。

### 引擎插件开关

如果插件用于内置引擎，在 `Engine/Config/BaseEngine.ini` 的 `[Plugins]` 中保持：

```ini
+EnabledPlugins=(Name="VRM4U",bEnabled=True)
+EnabledPlugins=(Name="KawaiiPhysics",bEnabled=True)
```

Installed Build 的插件编译宏应接收插件名称列表，并从 `Engine/Plugins/MooaToonThirdparty/<Plugin>/<Plugin>.uplugin` 编译和收集二进制。不要把 Junction 路径写入 BuildGraph。

如果插件源码的 `Build.cs` 静态依赖一个标记为可选的官方插件，仍需在项目 `.uproject` 中显式启用该依赖，并重新生成目标收据；插件描述中的 `Optional` 不会替代链接时依赖。

若第三方模块的多个源文件包含相同的匿名命名空间辅助符号，UE 5.8 Unity 合并可能产生重定义。对该模块在 5.8+ 构建中关闭 Unity，并用 `// Mooa ...` / `// Mooa End` 包裹兼容性改动，然后重新验证所有目标。

## 6. 分析并解决冲突

- 搜索全部 `.rej`，按依赖顺序建立 TODO；
- 对每个冲突同时查看 5.7 原始代码、5.8 当前调用方和所有消费者；
- 发现接口重构、序列化字段、缓存键、GPU ID 或材质编译链路变化时，扩大到整个引擎搜索；
- 解决并验证一个冲突文件的全部 hunk 后更新 `PatchConflicts.md`；
- 完成后核对冲突清单、日志和产物数量一致。

## 7. Legacy MooaToon 命名和序列化兼容

当旧分支定义自有 Legacy Toon 材质时，先完成命名兼容，再处理渲染冲突：

- C++ `MSM_Toon` 改为 `MSM_MooaToon`，保留枚举值 13；显示名为 `MooaToon`；
- Shader 使用 `SHADINGMODELID_MOOA_TOON=13`，官方 `SHADINGMODELID_SUBSTRATE_TOON=14`，总数为 15；
- 使用 `MATERIAL_SHADINGMODEL_MOOA_TOON`、`MooaToonBxDF` 和 `PIXEL_INSPECTOR_SHADINGMODELID_MOOA_TOON`；
- Core Redirects 和 `GetMaterialShadingModelFromString()` 同时接受旧短名称与完整枚举名称；正式枚举、输出字符串和生成宏只使用新名称；
- 在同一函数或表中，Mooa 分支放在官方 Toon 前；不跨作用域移动代码强求顺序；
- 保留 `FMaterialShadingModelField` 的位掩码语义和旧枚举数值；
- GPU ID、材质字段或 ShaderMap 布局变化时递增 Shader/DDC 版本；
- 保留五个 Mooa 材质属性的 GUID、名称、Float4 类型、默认值和引脚顺序；旧 MIR 文件已删除时，把赋值迁入当前 MIR 路径，不恢复删除文件。

## 8. 材质、渲染和插件编译验证

从 `<workspace-root>` 执行项目规定的 `./_4_0_Build_And_Run_MooaToon_Debug.bat`；也可从 `<engine-root>` 使用 `../_4_0_Build_And_Run_MooaToon_Debug.bat`。编译等待时间较长时按项目规则定期检查错误、退出和进度。

插件目录恢复后，至少核对：

- UnrealEditor 和 ShaderCompileWorker 的目标配置编译成功；
- VRM4U、KawaiiPhysics 模块和编辑器模块被编译并加载；
- 不再使用 `-DisablePlugins` 作为最终插件验证条件；
- `git diff --check`、UHT、相关模块和 Shader 编译无错误。

## 9. 旧资产验收

只在 Legacy、`r.Substrate=0` 下声明兼容。使用未在新版重存的父材质、材质实例 ShadingModel Override、From Material Expression、材质函数、静态开关、描边和 Sequence 资产：

1. 首次加载后、PostLoad 后和编译后确认 `MSM_MooaToon`、位掩码、生成宏、属性连接和描边引用；
2. 保存测试副本并重开，确认 Shading Model、参数和父子关系保持；
3. Cook 后运行，确认结果不依赖编辑器修复；
4. 固定相机、曝光、灯光和设置，对照旧版本检查 Ramp、Specular、Rim、Tangent、GI、反射、AO、透明/双面、RT 阴影、描边、Cloth、Sequence、导入和水体；
5. 记录证据到 `<workspace-root>/UpgradeEvidence/`，用 `<engine-root>/MigrationTODO.md` 分开标记代码处理和兼容验收。

编译通过、`.rej` 清零或插件可加载都不能替代旧资产保存重开、Cook 和固定场景视觉 A/B。

## 10. 收尾

确认 `PatchConflicts.md`、迁移台账、双语迁移文档、插件状态和工作区状态；保留用户已有修改，不执行 commit/push。若引擎或插件改动影响文档，同步中文文档及对应英文翻译。
