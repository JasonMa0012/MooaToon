# MooaToon

[中文](https://github.com/JasonMa0012/MooaToon/blob/main/README_CN.md) | English

**MooaToon** is a plugin that aims to completely solve the shortcomings of UE5 **Toon Rendering**, combining UE5 built-in **Lighting Features** with a **Powerful Material System** to unlock the potential of artists.

In development, please **Watch** this repo to get the latest news.

# Features

- **Lumen**
- Free to control **GI Intensity and Blending**
  
- Free to control **Reflection Intensity**
- **Shadow**
  - Virtual Shadow Map
  - Ray Tracing Shadow
    - Support for ignoring arbitrary partial **Self-Shadow**
    - Support for controllable **Hair Shadow Width**
- **Translucency**
  - Forward Shading (Lit Transparent)
  - Dithered Opacity
  - Dithered **Translucency Shadow**
- Great flexibility, with the Material Layer you can freely combine and create materials that contain the following features

  - **Japanese Animation style**, mainly pure color fast, clear light and shadow, often used to restore animation and hand-painted effect
  - **American Cartoon style**, usually with GI, with a softer shading
  - Customizable Base Color, Shadow Color, Specular Color
  - Customizable **Light and Shadow Range**, (TODO) support **Ramp Map**
  - Customizable **Highlight Range**, support **Anisotropic Highlight**
  - **Per Light** Screen Space Depth Test **Rimlight**
  - (TODO) **Face Shadow** based on Vertex Normal, Normal Map, Spherical Mapping, or any other method
  - Free to create and modify any features you need in the material editor
- **Outline** by single Overlay Material
  - Traditional **Back Face Outline**
  - Screen Space Depth Normal Convolution based **Front Face Outline**
  - Output Velocity to use with TSR **Anti-Aliasing**

- Cinematic post effect support

  - Correct **automatic exposure and manual exposure**
  - Globally controlled exposure compensation
  - Globally controlled Saturation, Contrast and other adjustments
  - **LookDev** tool

Videos：

![image-20221118014720535](README.assets/image-20221118014720535.png)

Models: KAGAMI Ⅱ WORKs, VRM4U

https://www.bilibili.com/video/BV1eG4y1x7Fr/

![image-20220723170300020](README.assets/image-20220723170300020.png)

https://www.youtube.com/watch?v=oBibO0WlakE



![image-20220613220050376](README.assets/image-20220613220050376.png)

https://www.bilibili.com/video/BV1m34y1V7MV

