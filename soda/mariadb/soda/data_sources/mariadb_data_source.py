import logging
from typing import Dict, List, Optional

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import mariadb
from soda.common.exceptions import DataSourceConnectionError
from soda.execution.data_source import DataSource
from soda.execution.data_type import DataType

logger = logging.getLogger(__name__)


class MariadbDataSource(DataSource):
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

        def __init__(self, logs: Logs, data_source_name: str, data_source_properties: dict):
        super().__init__(logs, data_source_name, data_source_properties)
        self.user = data_source_properties.get("username")
        self.password = data_source_properties.get("password")
        self.database = data_source_properties.get("database")
        self.host = data_source_properties.get("host")
        self.port = data_source_properties.get("port")

    def connect(self):
        self.connection = mariadb.connect(
            user=self.user,
            password=self.password,
            database=self.database,
            host=self.host,
            port=self.port,
        )
