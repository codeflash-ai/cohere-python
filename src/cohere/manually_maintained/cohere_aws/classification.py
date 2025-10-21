from typing import Any, Dict, Iterator, List, Literal, Union

from .response import CohereObject

Prediction = Union[str, int, List[str], List[int]]
ClassificationDict = Dict[Literal["prediction", "confidence", "text"], Any]


class Classification(CohereObject):
    def __init__(self, classification: Union["Prediction", "ClassificationDict"]) -> None:
        # Prediction is the old format (version 1 of classification-finetuning)
        # ClassificationDict is the new format (version 2 of classification-finetuning).
        # It also contains the original text and the labels' confidence scores of the prediction
        self.classification = classification

    def is_multilabel(self) -> bool:
        cls = self.classification
        # Optimized conditional order to reduce overhead and attribute accesses
        # Most common and fastest evaluated cases come first
        if type(cls) is list:
            return True
        if type(cls) is int or type(cls) is str:
            return False
        # By now, classification must be ClassificationDict, avoid repeated attribute lookups
        # Assumes that 'prediction' key always present if not the old format
        return type(cls["prediction"]) is list

    @property
    def prediction(self) -> Prediction:
        if isinstance(self.classification, (list, int, str)):
            return self.classification
        return self.classification["prediction"]

    @property
    def confidence(self) -> List[float]:
        if isinstance(self.classification, (list, int, str)):
            raise ValueError(
                "Confidence scores are not available for version prior to 2.0 of Cohere Classification Finetuning AWS package"
            )
        return self.classification["confidence"]

    @property
    def text(self) -> str:
        if isinstance(self.classification, (list, int, str)):
            raise ValueError(
                "Original text is not available for version prior to 2.0 of Cohere Classification Finetuning AWS package"
            )
        return self.classification["text"]


class Classifications(CohereObject):
    def __init__(self, classifications: List[Classification]) -> None:
        self.classifications = classifications
        if len(self.classifications) > 0:
            assert all([c.is_multilabel() == self.is_multilabel() for c in self.classifications]), (
                "All classifications must be of the same type (single-label or multi-label)"
            )

    def __iter__(self) -> Iterator:
        return iter(self.classifications)

    def __len__(self) -> int:
        return len(self.classifications)

    def is_multilabel(self) -> bool:
        return len(self.classifications) > 0 and self.classifications[0].is_multilabel()
