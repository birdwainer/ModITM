import os
import pickle
import numpy as np
from PIL import Image


def unpickle(file):
    with open(file, "rb") as fo:
        dict = pickle.load(fo, encoding="bytes")
    return dict


def convert_to_img(idx, images, labels):
    img = images[idx, :]
    label = labels[idx]
    img_r = np.reshape(img[:1024], (32, 32))
    img_g = np.reshape(img[1024:2048], (32, 32))
    img_b = np.reshape(img[2048:], (32, 32))
    img = np.stack([img_r, img_g, img_b]).transpose((1, 2, 0))
    return img, label


def visualize(img, label, classes_key):
    import matplotlib.pyplot as plt

    plt.imshow(img)
    plt.title(f"Label is {classes_key[label]}")
    plt.show()


if __name__ == "__main__":
    """
    CIFAR gives the dataset in 2D arrays where each row is an image flattened.
    This file converts that flattened image to a PNG and saves it to a class
    directory. For now, it is only using the test set as we do not need more
    than a few images to visualize for this demo.

    You can download the CIFAR-10 dataset from the original hosted source
    here: https://www.cs.toronto.edu/~kriz/cifar.html
    """

    CFAIR_BATCHES_DOWNLOAD_UNZIPPED_PATH = (
        "./cifar-10-batches-py"
    )
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

    # img, label = convert_to_img(idx=9991, images=images, labels=labels)
    # visualize(img, label, classes_key=CLASSES_KEY)

    for idx, row in enumerate(images):
        img, label = convert_to_img(idx=idx, images=images, labels=labels)
        Image.fromarray(img).save(
            os.path.join(OUT_ROOT, CLASSES_KEY[label], f"{idx}.png")
        )
