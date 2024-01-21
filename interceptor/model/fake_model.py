"""
This is 'model' is for development purposes only to unblock work
on of the rest of the system without waiting fof model development.

It returns one of three example softmax outputs for 10 CIFAR-10 classes. 
"""
import numpy as np
import pandas as pd
import torch
import random
from typing import Dict, List, Any


class FakeModel:
    CLASSES_KEY = {
        0: "plane",
        1: "car",
        2: "bird",
        3: "cat",
        4: "deer",
        5: "dog",
        6: "frog",
        7: "horse",
        8: "ship",
        9: "truck",
    }

    FAKE_TENSOR_LS = [
        torch.Tensor([[0.7, 0.2, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]),
        torch.Tensor([[0.3, 0.5, 0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 0.1]]),
        torch.Tensor([[0.0, 0.6, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3]]),
    ]

    def __init__(
        self,
        fake_tensors: List[torch.Tensor] = FAKE_TENSOR_LS,
        classes_key: Dict[int, str] = CLASSES_KEY,
    ) -> None:
        """
        Initializes the fake model with a list of tensors and a dictionary of class labels.

        Parameters:
            fake_tensors (List[torch.Tensor]): A list of fake tensors to be used in the model.
            Defaults to FAKE_TENSOR_LS.
            classes_key (Dict[int, str]): A dictionary of class labels where the keys are the
            class IDs and the values are the corresponding class names. Defaults to CLASSES_KEY.
        """
        self.fake_tensors = fake_tensors
        self.classes_key = classes_key

    def detect(self, *args: Any, **kwargs: Any) -> pd.DataFrame:
        """
        Run an example classification by returning a fake tensor softmax output of a 10 class
        classification problem.

        Parameters:
            args (tuple): A tuple of positional arguments to be passed to the function.
            kwargs (dict): A dictionary of keyword arguments to be passed to the function.
            These are unused other than to prevent input tensors specified in a normal
            inference call making the model fail.

        Returns:
            ret (pd.DataFrame): A pandas dataframe with a fake inference output.
        """
        result = random.choice(self.fake_tensors)

        ret = pd.DataFrame(
            np.column_stack(
                [
                    list(self.classes_key.keys()),
                    list(self.classes_key.values()),
                    result.numpy()[0],
                ]
            ),
            columns=["id", "name", "confidence"],
        )
        ret["id"] = pd.to_numeric(ret["id"])
        ret["confidence"] = pd.to_numeric(ret["confidence"])
        return ret
