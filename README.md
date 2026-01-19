# Mosamatic Insights
Mosamatic Insights is a tool for in-depth body composition analysis of image data.

## Usage

## Todo
- [x] Get PyInstaler running as PySide6 app (--noconsole)
- [x] Get PyInstaller running


Load DICOM series recursively

Run segmentation on selected series (TotalSegmentator) > cache to file (choose TS task eg liver segments)

View summary stats organ volumes (including liver segments)

Select series and view image slice viewer with TS segmentations as overlay

Hide/view all or selected segmentations

Run slice selection on selected series (take cached TS segmentations)

Run muscle fat segmentation on selected or all slices (both argmax and softmax)

View with single slice viewer (vtkImageStack for overlays)

HOW TO INCLUDE DIXON?

HOW TO TALK TO EXTERNAL PYTHON ENV (Conda based). INCLUDE THIS IN INSTALLER PACKAGE


  1.  Create installers for Mac and Windows that setup Python (through mamba) and run empty PySide6 GUI with a test button for PyTorch and OpenCV