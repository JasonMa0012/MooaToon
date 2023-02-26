# MooaToon

![Mooa (5)](README.assets/Mooa_gif.gif)


**MooaToon** is a plugin that aims to completely solve the shortcomings of **UE5 Toon Rendering**, combining UE5 built-in **Lighting Features** with a **Powerful Material System** to unlock the potential of artists.


**Home Page**: https://mooatoon.com/


## Features

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
  - Kajiya-Kay based **Dynamic Stylized Hair Highlighter**
  - **Per Light** Screen Space Depth Test **Rimlight**
  - **Face Shadow** based on Spherical Mapped Vertex Normal, Normal Map, or other method
  - Free to create and modify any features you need in the material editor
- Outline by single Overlay Material
  - Traditional **Back Face Outline**
  - Screen Space Depth Normal Convolution based **Front Face Outline**
  - Output Velocity to use with TSR **Anti-Aliasing**
  - One-Click baking tool for Smooth Normal
  - Houdini sample file for handling normals and vertex colors
- Cinematic post effect support
  - Correct **automatic exposure and manual exposure**
  - Globally controlled exposure compensation
  - Globally controlled Saturation, Contrast and other adjustments
  - **LookDev** tool
- Misc
  - Morph Targets Normal Intensity


## License

https://mooatoon.com/docs/Licence/


## References

| Name      | Author    | Link                                                  |
| --------- | --------- | ----------------------------------------------------- |
| VRM4U     | ruyo      | https://github.com/ruyo/VRM4U                         |
| UnityChan | © UTJ/UCL | https://unity-chan.com/                               |

