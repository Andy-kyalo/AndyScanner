"""
swing_classifier.py

Classifies confirmed swings:

HIGH:
    INITIAL
    HH
    LH

LOW:
    INITIAL
    HL
    LL
"""

from typing import List

from .models import StructurePoint


class SwingClassifier:
    """
    Applies structural labels to confirmed swing points.
    """

    @staticmethod
    def classify_highs(
        points: List[StructurePoint],
    ) -> List[StructurePoint]:

        labelled = []
        previous_price = None

        for point in points:

            if previous_price is None:
                label = "INITIAL"

            elif point.price > previous_price:
                label = "HH"

            else:
                label = "LH"

            labelled.append(
                StructurePoint(
                    index=point.index,
                    time=point.time,
                    price=point.price,
                    kind="HIGH",
                    label=label,
                )
            )

            previous_price = point.price

        return labelled

    @staticmethod
    def classify_lows(
        points: List[StructurePoint],
    ) -> List[StructurePoint]:

        labelled = []
        previous_price = None

        for point in points:

            if previous_price is None:
                label = "INITIAL"

            elif point.price > previous_price:
                label = "HL"

            else:
                label = "LL"

            labelled.append(
                StructurePoint(
                    index=point.index,
                    time=point.time,
                    price=point.price,
                    kind="LOW",
                    label=label,
                )
            )

            previous_price = point.price

        return labelled
