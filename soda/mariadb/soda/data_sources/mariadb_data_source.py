import logging
from typing import Dict, List, Optional

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import mariadb
from soda.common.exceptions import DataSourceConnectionError
from soda.execution.data_source import DataSource
from soda.execution.data_type import DataType

logger = logging.getLogger(__name__)


class DataSourceImpl(DataSource):
    TYPE = "mariadb"

    SCHEMA_CHECK_TYPES_MAPPING: Dict = {
        "TEXT": ["varchar", "text", "char"],
        "NUMBER": ["integer", "int", "bigint", "mediumint", "smallint", "tinyint"],
    }
    SQL_TYPE_FOR_CREATE_TABLE_MAP: Dict = {
        DataType.TEXT: "TEXT",
        DataType.INTEGER: "INT",
        DataType.DECIMAL: "DECIMAL",
        DataType.DATE: "DATE",
        DataType.TIME: "TIME",
        DataType.TIMESTAMP: "TIMESTAMP_NTZ",
        # DataType.TIMESTAMP_TZ: "TIMESTAMP_TZ",
        DataType.BOOLEAN: "BOOLEAN",
    }

    SQL_TYPE_FOR_SCHEMA_CHECK_MAP = {
        DataType.TEXT: "TEXT",
        DataType.INTEGER: "INTEGER",
        DataType.DECIMAL: "DECIMAL",
        DataType.DATE: "DATE",
        DataType.TIME: "TIME",
        DataType.TIMESTAMP: "TIMESTAMP_NTZ",
        # DataType.TIMESTAMP_TZ: "TIMESTAMP_TZ",
        DataType.BOOLEAN: "BOOLEAN",
    }

    NUMERIC_TYPES_FOR_PROFILING = ["FLOAT", "DECIMAL", "INT"]
    TEXT_TYPES_FOR_PROFILING = ["TEXT", "VARCHAR", "CHAR"]

    def connect(self, connection_properties):
        self.connection_properties = connection_properties
        try:
            self.connection = mariadb.connect(
                host=connection_properties.get("host"),
                user=connection_properties.get("username"),
                password=connection_properties.get("password"),
                database=connection_properties.get("database"),
                port=connection_properties.get("port"),
            )
            return self.connection

        except Exception as e:
            raise DataSourceConnectionError(self.TYPE, e)
