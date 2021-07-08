# ImagingS

![CI](https://github.com/StardustDL/ImagingS/workflows/CI/badge.svg) ![](https://img.shields.io/github/license/StardustDL/ImagingS.svg) [![](https://img.shields.io/pypi/dm/imagings)](https://pypi.org/project/imagings/)

![](https://repository-images.githubusercontent.com/226446069/77831900-b856-11ea-95ef-6fd6c38a9edc)

A toolset for computer graphics and imaging processing.

- [Demo Video](https://www.bilibili.com/video/BV1Q54y1i7Lg/)
- [Usage 中文](https://github.com/StardustDL/own-staticfile-hosting/tree/0eb7357813c8f043e5bc6c488e4fe2c971a87424/StardustDL/ImagingS/Helping)

## Features

- Geometry
  - Line ( DDA & Bresenham )
  - Curve ( Bezier & B-spline )
  - Ellipse
  - Polygon
    - Polyline
    - Rectangle
- Transform
  - Translate
  - Rotate
  - Scale
  - Skew
  - Matrix
- Clip
- Interactivity
  - WYSIWYG
  - Shortcuts
- Document
  - Json
  - Code editor
- Export
  - PNG, JPEG, BMP

## Usage

```sh
# Install
pip install imagings
# Launch GUI
imagings
# or use
python -m ImagingS.Gui
```

## Development

1. Clone this repository.
2. Install dependencies.

```sh
pip install requirements.txt
```

3. Generate UI codes

```sh
python -m ImagingS.Gui.uic
```

4. Run GUI

```sh
python -m ImagingS.Gui
```

5. Run CLI

```sh
python -m ImagingS.Cli input.txt output_dir
```
