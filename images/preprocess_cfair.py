"""
CIFAR gives the dataset in 2D arrays where each row is an image flattened.
This file converts that flattened image to a PNG and saves it to a class
directory. For now, it is only using the test set as we do not need more
than a few images to visualize for this demo.

You can download the CIFAR-10 dataset from the original hosted source
here: https://www.cs.toronto.edu/~kriz/cifar.html
"""
import os
import pickle
import numpy as np
from PIL import Image
from typing import Dict, Any, Tuple
import numpy.typing as npt


def unpickle(file: str) -> Dict[bytes, Any]:
    """Unpickles the file at the specified path and returns a dictionary with the contents.
    Function is from https://www.cs.toronto.edu/~kriz/cifar.html.

    Args:
        file (str): The path to the pickled file.

    Returns:
        dict (Dict[str, Any]): A dictionary containing the unpickled data.
    """
    with open(file, "rb") as fo:
        dict = pickle.load(fo, encoding="bytes")
    return dict


def convert_to_img(
    idx: int, images: npt.NDArray[np.float32], labels: npt.NDArray[np.float32]
) -> Tuple[npt.NDArray[np.float32], int]:
    """Converts the input data to an image and returns it along with its corresponding label.
    The CIFAR-10 dataset is provided in vectors where the first 1024 pixels are the red channel,
    the next 1024 are the green channel, and the last 1024 are the blue channel to compose a
    32 x 32 x 3 pixel image.

    Args:
        idx (int): The index of the input data in the dataset.
        images (np.ndarray): The input data containing the pixel values for each image.
        labels (np.ndarray): The labels associated with the input data.

    Returns:
        Tuple[np.ndarray, int]: A tuple containing the converted image and its corresponding label.
    """
    img = images[idx, :]
    label = labels[idx]
    img_r = np.reshape(img[:1024], (32, 32))
    img_g = np.reshape(img[1024:2048], (32, 32))
    img_b = np.reshape(img[2048:], (32, 32))
    img = np.stack([img_r, img_g, img_b]).transpose((1, 2, 0))
    return img, label


def visualize(
    img: npt.NDArray[np.float32], label: int, classes_key: Dict[int, str]
) -> None:
    """Visualizes the input image and its corresponding label for development
    purposes.

    Args:
        img (np.ndarray): The input image to be visualized.
        label (int): The label associated with the input image.
        classes_key (Dict[int, str]): A dictionary containing the class keys for each label.

    Returns:
        None: This function does not return any value.
    """
    import matplotlib.pyplot as plt

    plt.imshow(img)
    plt.title(f"Label is {classes_key[label]}")
    plt.show()


if __name__ == "__main__":
    CIFAR_BATCHES_DOWNLOAD_UNZIPPED_PATH = "./cifar-10-batches-py"
    OUT_ROOT = "./CIFAR-10"

    CIFAR_LABEL_LIST_PATH = unpickle(
        os.path.join(CIFAR_BATCHES_DOWNLOAD_UNZIPPED_PATH, "batches.meta")
    )[b"label_names"]

    CLASSES_KEY = {
        idx: val.decode("utf-8") for idx, val in enumerate(CIFAR_LABEL_LIST_PATH)
    }
    for val in CLASSES_KEY.values():
        os.makedirs(os.path.join(OUT_ROOT, val), exist_ok=True)
    test_data = unpickle(
        os.path.join(CIFAR_BATCHES_DOWNLOAD_UNZIPPED_PATH, "test_batch")
    )
    images = test_data[b"data"]
    labels = np.array(test_data[b"labels"])

    for idx, row in enumerate(images):
        img, label = convert_to_img(idx=idx, images=images, labels=labels)
        Image.fromarray(img).save(
            os.path.join(OUT_ROOT, CLASSES_KEY[label], f"{idx}.png")
        )
