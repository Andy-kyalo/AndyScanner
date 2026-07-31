"""
mapper_factory.py

Mapper Factory.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.mapping.csv_mapper import CSVMapper
from backend.mapping.json_mapper import JSONMapper
from backend.mapping.xml_mapper import XMLMapper
from backend.mapping.mt5_mapper import MT5Mapper


class MapperFactory:
    """
    Factory responsible for creating
    the correct mapper.
    """

    _mappers = {
        "csv": CSVMapper,
        "json": JSONMapper,
        "xml": XMLMapper,
        "mt5": MT5Mapper,
    }

    @classmethod
    def create(cls, mapper_type):
        """
        Create mapper instance.

        Parameters
        ----------
        mapper_type : str

        Returns
        -------
        BaseMapper
        """

        if mapper_type is None:
            raise ValueError("Mapper type cannot be None.")

        mapper = cls._mappers.get(
            mapper_type.lower()
        )

        if mapper is None:
            supported = ", ".join(
                cls._mappers.keys()
            )

            raise ValueError(
                f"Unsupported mapper '{mapper_type}'. "
                f"Supported: {supported}"
            )

        return mapper()

    @classmethod
    def register(
        cls,
        name,
        mapper_class,
    ):
        """
        Register a new mapper.
        """

        cls._mappers[name.lower()] = mapper_class

    @classmethod
    def available_mappers(cls):
        """
        Returns all registered mappers.
        """

        return sorted(cls._mappers.keys())