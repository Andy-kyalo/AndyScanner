"""
xml_mapper.py

XML market data mapper.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import xml.etree.ElementTree as ET

from backend.mapping.base_mapper import BaseMapper
from backend.models.candle import Candle


class XMLMapper(BaseMapper):
    """
    Converts XML market data into Candle objects.
    """

    def map(self, raw_data):
        """
        Convert XML string into Candle objects.

        Expected XML structure:

        <candles>
            <candle>
                <time>22:00</time>
                <open>45020.5</open>
                <high>45110.75</high>
                <low>44980.25</low>
                <close>45110.75</close>
            </candle>
        </candles>
        """

        self.validate(raw_data)

        root = ET.fromstring(raw_data)

        candles = []

        for node in root.findall("candle"):

            candle = Candle(
                time=node.find("time").text,
                open=float(node.find("open").text),
                high=float(node.find("high").text),
                low=float(node.find("low").text),
                close=float(node.find("close").text),
            )

            candles.append(candle)

        return candles