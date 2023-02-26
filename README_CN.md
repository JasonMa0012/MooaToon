# MooaToon

- [Features](#features)
- [Works](#works)
- [License](#license)
  * [Commercial Activities](#commercial-activities)
  * [Modify and Republish](#modify-and-republish)
- [Wiki](#wiki)
- [References](#references)

中文 | [English](https://github.com/JasonMa0012/MooaToon)

![Mooa (5)](README_CN.assets/Mooa_gif.gif)

**MooaToon**是一个旨在彻底解决 **UE5 三渲二** 痛点的插件, 结合了UE原生的**光照特性**和强大的**材质系统**, 释放美术师的潜力.



**重要提示**: MooaToon当前禁止获得许可之前的商业行为, 详情请阅读**License**.

**入门**: https://www.yuque.com/jasonma0012/mooa-toon/getting-started

请**Watch**此仓库或加入社交媒体以获得最新消息.


## Features

- **Lumen**
  - 可自由控制**GI强度和混合**
  - 可自由控制**Reflection强度**
- **Shadow**
  - Virtual Shadow Map
  - Ray Tracing Shadow
    - 支持忽略任意部分**自阴影**
    - 支持可控**发影宽度**
- **Translucency**
  - Forward Shading（Lit Transparent）
  - Dithered Opacity
  - Dithered **Translucency Shadow**
- 极佳的灵活性，通过Material Layer你可以自由组合并创建包含以下特性的材质：
  - 日式**赛璐璐**风格，以纯色快为主，明暗分明，常用于还原动画、手绘效果
  - **美式卡通**风格，通常带有GI，相对更加柔和的明暗变化
  - 可自定义的基础色、阴影色、高光色
  - 可自定义的**明暗过渡**，(TODO) 支持**Ramp**
  - 可自定义的**高光过渡**，支持**各向异性高光**
  - 基于Kajiya-Kay的**动态风格化头发高光**
  - **逐光源**的屏幕空间深度检测**边缘光**
  - 基于球面映射顶点法线、法线贴图、或其他方法的**脸影**
  - 通过材质编辑器自由创建、修改你需要的任何特性
- 使用单个Overlay Material的描边
  - 传统**背面描边**
  - 基于屏幕空间深度法线卷积的**正面描边**
  - 输出Velocity以和TSR**抗锯齿**一起使用
  - 一键烘焙平滑法线的工具
  - 处理法线和顶点色的Houdini示例文件
- 影视后期支持
  - 正确的**自动曝光、手动曝光**
  - 可全局控制的曝光补偿
  - 可全局控制的饱和度、对比度等调整
  - **LookDev**工具
- 杂项
  - Morph Targets Normal Intensity


## Works

| Title                                                        | Link                                         | Description                 |
| ------------------------------------------------------------ | -------------------------------------------- | --------------------------- |
| 【MooaToon Devlog】近期成果 UE5 三渲二 Lumen Kajiya-Kay 头发高光 Ramp | https://www.bilibili.com/video/BV13g411t7L8/ | 模型: © UTJ/UCL             |
| ![image-20221229110024330](README_CN.assets/image-20221229110024330.png) |                                              |                             |
| 【Mooa Toon Devlog UE5.1】三渲二？Lumen？我全都要！Time of Day动态演示 | https://www.bilibili.com/video/BV1eG4y1x7Fr/ | 模型: KAGAMI Ⅱ WORKs, VRM4U |
| ![image-20221118014720535](README_CN.assets/image-20221118014720535.png) |                                              |                             |
| 【Mooa Toon Devlog】UE5光线追踪卡通发影 多光源交互           | https://www.bilibili.com/video/BV1xV4y17766/ | 模型：KAGAMI Ⅱ WORKs        |
| ![image-20220723170300020](README_CN.assets/image-20220723170300020.png) |                                              |                             |
| 【MooaToon】开发日志：完整支持UE5光照系统的卡通渲染管线      | https://www.bilibili.com/video/BV1m34y1V7MV  | 模型：KAGAMI Ⅱ WORKs        |
| ![image-20220613220050376](README_CN.assets/image-20220613220050376.png) |                                              |                             |
|                                                              |                                              |                             |
|                                                              |                                              |                             |
|                                                              |                                              |                             |



## License

**简单来说, 你可以将MooaToon用于任何非商业用途. 但在进行商业行为之前, 你必须取得我们的商业授权.**

如果你需要:

- 商业授权
- 为角色设置最佳渲染效果
- 优先技术支持
- 优先Bug修复
- 实现指定的新功能
- ...

请咨询邮箱: jasonma0012@foxmail.com


以下是一份用户许可协议 (以下称为“”协议“”), 协议随时可能更新, 请[Watch](https://github.com/JasonMa0012/MooaToon)此仓库以获取更新通知. 如果不同语言版本的协议出现了冲突, 则以中文版本为准.

如果您继续使用MooaToon则视为已了解且同意该协议, 如果您使用且违反了本协议的条款, 我们保留随时向您追责的权利.

MooaToon的作者是Jason Ma (以下称为"作者"), 并且由以下部分组成:

1. “引擎改动”: 指由Epic Games创建, 由作者进行修改的部分文件, 即通过和[Epic Games仓库](https://github.com/EpicGames/UnrealEngine)进行[分支对比](https://github.com/EpicGames/UnrealEngine/compare/5.1...Jason-Ma-0012:MooaToon-Engine:5.1)得出的有内容修改的文件
2. “插件内容”: 指由作者创建的文件, 包括但不限于:
   1. 引擎分支: [Engine/Plugins/MooaToon](https://github.com/Jason-Ma-0012/MooaToon-Engine/tree/5.1/Engine/Plugins/MooaToon)
   2. 引擎分支其他非第三方新增文件 (如[ToonShadingCommon.ush](https://github.com/Jason-Ma-0012/MooaToon-Engine/blob/5.1/Engine/Shaders/Private/ToonShadingCommon.ush))
   3. [Project分支](https://github.com/Jason-Ma-0012/MooaToon-Engine/tree/5.1_MooaToonProject)内的非第三方内容
3. “渲染技术”: 指由作者设计, 并以此为指导完成“引擎改动”和“插件内容”的技术概念

对于引擎改动, 我们遵循”[Epic协议](https://www.unrealengine.com/en-US/eula/unreal)”, 对于插件内容和渲染技术, 我们在Epic协议的基础上有以下限制:

### Commercial Activities

**在您获得我们的特别许可之前, 禁止您使用MooaToon进行一切商业行为.**

此外, 您可以使用MooaToon进行任何商业目的以外的行为, 但是**您需要自行承担一切行为后果**.

### Modify

**您可以任意修改MooaToon, 但MooaToon的所有权利依旧属于作者**. 

同时也禁止在几乎不改变渲染技术的情况下, 改变引擎改动或插件内容以试图绕过此协议的行为.

## Wiki

https://mooatoon.com/docs/GettingStarted/



## References

| Name          | Author      | Link                                                   |
| ------------- | ----------- | ------------------------------------------------------ |
| VRM4U         | ruyo        | https://github.com/ruyo/VRM4U                          |
| UnityChan     | © UTJ/UCL   | https://unity-chan.com/                                |


