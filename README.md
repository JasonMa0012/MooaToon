# MooaToon

[中文](https://github.com/JasonMa0012/MooaToon/blob/main/README_CN.md) | English

Mooatoon is a Toon Rendering Pipeline that supports  UE5 lighting system for **Cinematics**.

In development, please **Watch** this repo to get the latest news.

# Features

- Full support for **Lumen**

  - GI

  - Reflection
- Full support for **Shadow**

  - Virtual Shadow Map
  - Ray Tracing Shadow
- **Toon Shadow**
  - Ray Tracing Hair/Face Shadow

  - Support to ignore Ray Tracing Self-Shadow

- Partial support for **Translucency**

  - Forward Shading（Lit Transparent）
  - Dither Opacity
  - (TODO) Translucency Shadow
- Great flexibility, with the Material Layer you can freely combine and create materials that contain the following features

  - **Japanese animation style**, mainly pure color fast, clear light and shadow, often used to restore animation and hand-painted effect
  - **American cartoon style**, usually with GI, with a softer shading
  - Customizable base color, shadow color, highlight color
  - Customizable **light and shadow ranges**, transitions, (TODO) support **Ramp**
  - Customizable **highlight range, transition**, support **anisotropic highlights**
  - (TODO) **Rimlight** based on NoV or Screen Space Depth
  - (TODO) **Face Shadow** based on Vertex Normal, Normal Map, Spherical Mapping, or any other method
  - Free to create and modify any features you need in the material editor
- (TODO) **Back Face Outline**, **Geometry Outline**, and other methods
- (TODO) Cinematic post effect support

  - (TODO) Correct **automatic exposure and manual exposure**
  - Globally controlled exposure compensation
  - Globally controlled Saturation, Contrast and other adjustments
  - **LookDev** support

Videos：

![image-20220723170300020](README.assets/image-20220723170300020.png)

https://www.youtube.com/watch?v=oBibO0WlakE

Model：KAGAMI Ⅱ WORKs

![image-20220613220050376](README.assets/image-20220613220050376.png)

https://www.bilibili.com/video/BV1m34y1V7MV

