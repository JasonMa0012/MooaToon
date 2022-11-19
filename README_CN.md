# MooaToon
中文 | [English](https://github.com/JasonMa0012/MooaToon)

**MooaToon**是一个旨在彻底解决**UE5三渲二**痛点的插件, 结合了UE原生的**光照特性**和强大的**材质系统**, 释放美术的潜力.

正在开发中，请**Watch**此仓库以获得最新消息。

# 特性

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
  - 可自定义的明**暗范围**，(TODO) 支持**Ramp**
  - 可自定义的**高光范围**，支持**各向异性高光**
  - **逐光源**的屏幕空间深度检测**边缘光**
  - (TODO) 基于顶点法线、法线贴图、球面映射或任何其他方法的**脸影**
  - 通过材质编辑器自由创建、修改你需要的任何特性
- 使用单个Overlay Material的**描边**
  - 传统**背面描边**
  - 基于屏幕空间深度法线卷积的**正面描边**
  - 输出Velocity以和TSR**抗锯齿**一起使用

- 影视后期支持

  - 正确的**自动曝光、手动曝光**
  - 可全局控制的曝光补偿
  - 可全局控制的饱和度、对比度等调整
  - **LookDev**工具

视频：

![image-20221118014720535](README_CN.assets/image-20221118014720535.png)

模型: KAGAMI Ⅱ WORKs, VRM4U

https://www.bilibili.com/video/BV1eG4y1x7Fr/

![image-20220723170300020](README_CN.assets/image-20220723170300020.png)

https://www.bilibili.com/video/BV1xV4y17766/



![image-20220613220050376](README_CN.assets/image-20220613220050376.png)

https://www.bilibili.com/video/BV1m34y1V7MV

