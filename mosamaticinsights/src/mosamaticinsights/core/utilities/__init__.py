import sys
import pathlib
import numpy as np


def home():
    return pathlib.Path.home()


def is_macos():
    return sys.platform.lower() == 'darwin'


def get_rescale_params(p):
    rescale_slope = getattr(p, 'RescaleSlope', None)
    rescale_intercept = getattr(p, 'RescaleIntercept', None)
    if rescale_slope is not None and rescale_intercept is not None:
        return rescale_slope, rescale_intercept
    # Try Enhanced DICOM structure
    if 'SharedFunctionalGroupsSequence' in p:
        fg = p.SharedFunctionalGroupsSequence[0]
        if 'PixelValueTransformationSequence' in fg:
            pvt = fg.PixelValueTransformationSequence[0]
            rescale_slope = pvt.get('RescaleSlope', 1)
            rescale_intercept = pvt.get('RescaleIntercept', 0)
            return rescale_slope, rescale_intercept
    return 1, 0


def get_pixels_from_dicom_object(p, normalize=True):
    pixels = p.pixel_array
    if not normalize:
        return pixels
    if normalize is True: # Map pixel values back to original HU values
        rescale_slope, rescale_intercept = get_rescale_params(p)
        return rescale_slope * pixels + rescale_intercept
    if isinstance(normalize, int):
        return (pixels + np.min(pixels)) / (np.max(pixels) - np.min(pixels)) * normalize
    if isinstance(normalize, list):
        return (pixels + np.min(pixels)) / (np.max(pixels) - np.min(pixels)) * normalize[1] + normalize[0]
    return pixels


def convert_labels_to_157(label_image: np.array) -> np.array:
    label_image157 = np.copy(label_image)
    label_image157[label_image157 == 1] = 1
    label_image157[label_image157 == 2] = 5
    label_image157[label_image157 == 3] = 7
    return label_image157


def normalize_between(img: np.array, min_bound: int, max_bound: int) -> np.array:
    img = (img - min_bound) / (max_bound - min_bound)
    img[img < 0] = 0
    img[img > 1] = 0
    c = (img - np.min(img))
    d = (np.max(img) - np.min(img))
    img = np.divide(c, d, np.zeros_like(c), where=d != 0)
    return img


def apply_window_center_and_width(image: np.array, center: int, width: int) -> np.array:
    image_min = center - width // 2
    image_max = center + width // 2
    windowed_image = np.clip(image, image_min, image_max)
    windowed_image = ((windowed_image - image_min) / (image_max - image_min)) * 255.0
    return windowed_image.astype(np.uint8)


def calculate_area(labels: np.array, label, pixel_spacing) -> float:
    mask = np.copy(labels)
    mask[mask != label] = 0
    mask[mask == label] = 1
    area = np.sum(mask) * (pixel_spacing[0] * pixel_spacing[1]) / 100.0
    return area


def calculate_index(area: float, height: float) -> float:
    return area / (height * height)


def calculate_bmi(weight: float, height: float) -> float:
    return weight / (height * height)
