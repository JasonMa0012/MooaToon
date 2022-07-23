# MooaToon
中文 | [English](https://github.com/JasonMa0012/MooaToon)

MooaToon是一个用于**影视**的完整支持UE5光照系统的卡通渲染管线。

正在开发中，请**Watch**此仓库以获得最新消息。

# 特性

- 对于**Lumen**的完整支持
  - GI
  - Reflection
- 对于**Shadow**的完整支持

  - Virtual Shadow Map
  - Ray Tracing Shadow
- **卡通阴影**
- 光线追踪发/脸影
  
  - 支持忽略光线追踪自阴影

- **Translucency**部分支持
  - Forward Shading（Lit Transparent）
  - Dither Opacity
  - (TODO) Translucency Shadow
- 极佳的灵活性，通过Material Layer你可以自由组合并创建包含以下特性的材质：

  - 日式**赛璐璐**风格，以纯色快为主，明暗分明，常用于还原动画、手绘效果
  - **美式卡通**风格，通常带有GI，相对更加柔和的明暗变化
  - 可自定义的基础色、阴影色、高光色
  - 可自定义的明**暗范围、过渡**，(TODO) 支持**Ramp**
  - 可自定义的**高光范围、过渡**，支持**各向异性高光**
  - (TODO) 基于视角或屏幕空间深度的**边缘光**
  - (TODO) 基于顶点法线、法线贴图、球面映射或任何其他方法的**脸影**
  - 通过材质编辑器自由创建、修改你需要的任何特性
- (TODO) **背面法描边**、**几何描边**以及其他方法 
- (TODO) 影视后期支持

  - 正确的**自动曝光、手动曝光**
  - 可全局控制的曝光补偿
  - 可全局控制的饱和度、对比度等调整
  - **LookDev**支持

视频：

![image-20220723170300020](README_CN.assets/image-20220723170300020.png)

https://www.bilibili.com/video/BV1xV4y17766/

模型：KAGAMI Ⅱ WORKs

![image-20220613220050376](README_CN.assets/image-20220613220050376.png)

https://www.bilibili.com/video/BV1m34y1V7MV

