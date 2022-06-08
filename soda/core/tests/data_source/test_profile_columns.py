from __future__ import annotations

import pytest
from tests.conftest import test_data_source
from tests.helpers.common_test_tables import customers_profiling
from tests.helpers.scanner import Scanner


@pytest.mark.skipif(
    test_data_source == "athena",
    reason="TODO: fix for athena.",
)
@pytest.mark.parametrize(
    "table_name, soda_cl_str, cloud_dict_expectation",
    [
        pytest.param(
            customers_profiling,
            ".%",
            {
                "definitionName": "test_profile_columns.py::test_profile_columns[customer table all numric columns]",
                "dataTimestamp": "2022-04-29T08:41:19.772904",
                "scanStartTimestamp": "2022-04-29T08:41:19.772904",
                "scanEndTimestamp": "2022-04-29T08:41:19.865563",
                "hasErrors": False,
                "hasWarnings": False,
                "hasFailures": False,
                "metrics": [],
                "checks": [],
                "profiling": [
                    {
                        "columnProfiles": [
                            {
                                "columnName": "size",
                                "profile": {
                                    "mins": [0.5, 1.0, 6.0],
                                    "maxs": [6.0, 1.0, 0.5],
                                    "min": 0.5,
                                    "max": 6.0,
                                    "frequent_values": [
                                        {"value": "None", "frequency": 4},
                                        {"value": "0.5", "frequency": 3},
                                        {"value": "6.1", "frequency": 2},
                                    ],
                                    "avg": 2.41666666666667,
                                    "sum": 14.5,
                                    "stddev": 2.7823850680067,
                                    "variance": 7.74166666666667,
                                    "distinct": 3,
                                    "missing_count": 4,
                                    "histogram": {
                                        "boundaries": [
                                            0.5,
                                            0.78,
                                            1.06,
                                            1.34,
                                            1.62,
                                            1.9,
                                            2.18,
                                            2.46,
                                            2.74,
                                            3.02,
                                            3.3,
                                            3.58,
                                            3.86,
                                            4.14,
                                            4.42,
                                            4.7,
                                            4.98,
                                            5.26,
                                            5.54,
                                            5.82,
                                            6.1,
                                        ],
                                        "frequencies": [
                                            3,
                                            1,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            2,
                                        ],
                                    },
                                },
                            },
                            {
                                "columnName": "distance",
                                "profile": {
                                    "mins": [-999, 1, 10, 999],
                                    "maxs": [999, 10, 1, -999],
                                    "min": -999,
                                    "max": 999,
                                    "frequent_values": [
                                        {"value": "10", "frequency": 3},
                                        {"value": "999", "frequency": 3},
                                        {"value": "None", "frequency": 2},
                                        {"value": "-999", "frequency": 1},
                                    ],
                                    "avg": 253.625,
                                    "sum": 2029,
                                    "stddev": 704.850528734386,
                                    "variance": 496814.26785714284,
                                    "distinct": 4,
                                    "missing_count": 2,
                                    "histogram": {
                                        "boundaries": [
                                            -999.0,
                                            -899.1,
                                            -799.2,
                                            -699.3,
                                            -599.4,
                                            -499.5,
                                            -399.6,
                                            -299.7,
                                            -199.8,
                                            -99.9,
                                            -0.0,
                                            99.9,
                                            199.8,
                                            299.7,
                                            399.6,
                                            499.5,
                                            599.4,
                                            699.3,
                                            799.2,
                                            899.1,
                                            999.0,
                                        ],
                                        "frequencies": [
                                            1,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            4,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            3,
                                        ],
                                    },
                                },
                            },
                        ],
                    }
                ],
            },
            id="customer table all numric columns",
        )
    ],
)
def test_profile_columns_numeric(scanner: Scanner, table_name, soda_cl_str, cloud_dict_expectation):
    table_name = scanner.ensure_test_table(table_name)

    scan = scanner.create_test_scan()
    mock_soda_cloud = scan.enable_mock_soda_cloud()
    scan.add_sodacl_yaml_str(
        f"""
          profile columns:
            columns: [{table_name}{soda_cl_str}]
        """
    )
    scan.execute(allow_warnings_only=True)
    # remove the data source name because it's a pain to test
    profiling_result = mock_soda_cloud.pop_scan_result()
    assert profiling_result
    profiling_result = remove_datasource_and_table_name(profiling_result)
    assert len(profiling_result["profiling"]) > 0
    assert len(profiling_result["profiling"][0]["columnProfiles"]) > 0
    assert profiling_result["profiling"][0]["columnProfiles"][0]["columnName"].lower() == "size"
    assert (
        profiling_result["profiling"][0]["columnProfiles"][0]["profile"]["frequent_values"]
        == cloud_dict_expectation["profiling"][0]["columnProfiles"][0]["profile"]["frequent_values"]
    )
    assert (
        profiling_result["profiling"][0]["columnProfiles"][0]["profile"]["histogram"]
        == cloud_dict_expectation["profiling"][0]["columnProfiles"][0]["profile"]["histogram"]
    )


@pytest.mark.skipif(
    test_data_source == "athena",
    reason="TODO: fix for athena.",
)
@pytest.mark.parametrize(
    "table_name, soda_cl_str, cloud_dict_expectation",
    [
        pytest.param(
            customers_profiling,
            ".country",
            {
                "definitionName": "test_profile_columns.py::test_profile_columns_text[table_name0-.country-cloud_dict_expectation0]",
                "dataTimestamp": "2022-04-29T14:32:57.111198",
                "scanStartTimestamp": "2022-04-29T14:32:57.111198",
                "scanEndTimestamp": "2022-04-29T14:32:57.197097",
                "hasErrors": False,
                "hasWarnings": False,
                "hasFailures": False,
                "metrics": [],
                "checks": [],
                "profiling": [
                    {
                        "columnProfiles": [
                            {
                                "columnName": "country",
                                "profile": {
                                    "mins": None,
                                    "maxs": None,
                                    "min": None,
                                    "min_length": 2,
                                    "max": None,
                                    "max_length": 2,
                                    "frequent_values": [
                                        {"value": "BE", "frequency": 6},
                                        {"value": "NL", "frequency": 4},
                                    ],
                                    "avg": None,
                                    "avg_length": 2,
                                    "sum": None,
                                    "stddev": None,
                                    "variance": None,
                                    "distinct": 2,
                                    "missing_count": 0,
                                    "histogram": None,
                                },
                            }
                        ],
                    }
                ],
            },
            id="customer.country (text only)",
        )
    ],
)
def test_profile_columns_text(scanner: Scanner, table_name, soda_cl_str, cloud_dict_expectation):
    table_name = scanner.ensure_test_table(table_name)

    scan = scanner.create_test_scan()
    mock_soda_cloud = scan.enable_mock_soda_cloud()
    scan.add_sodacl_yaml_str(
        f"""
          profile columns:
            columns: [{table_name}{soda_cl_str}]
        """
    )
    scan.execute(allow_warnings_only=True)
    profiling_result = mock_soda_cloud.pop_scan_result()
    # remove the data source name because it's a pain to test
    profiling_result = remove_datasource_and_table_name(profiling_result)

    assert profiling_result["profiling"] == cloud_dict_expectation["profiling"]


@pytest.mark.skipif(
    test_data_source == "athena",
    reason="TODO: fix for athena.",
)
def test_profile_columns_all_tables_all_columns(scanner: Scanner):
    _ = scanner.ensure_test_table(customers_profiling)
    scan = scanner.create_test_scan()
    mock_soda_cloud = scan.enable_mock_soda_cloud()
    scan.add_sodacl_yaml_str(
        """
            profile columns:
                columns: ["%.%"]
        """
    )
    scan.execute(allow_warnings_only=True)
    profiling_result = mock_soda_cloud.pop_scan_result()
    assert len(profiling_result["profiling"]) >= 5


@pytest.mark.parametrize(
    "table_name, soda_cl_str, expectation",
    [
        pytest.param(
            customers_profiling,
            """
                profile columns:
                    columns:
                        - include {table_name}.%
                        - include %.size
                        - exclude %.country
                        - exclude %.id
            """,
            "",
        ),
        pytest.param(
            customers_profiling,
            """
                profile columns:
                    columns:
                        - include %.%
                        - exclude %.id
            """,
            "all but id",
            id="all tables and cols except for id",
        ),
        pytest.param(
            customers_profiling,
            """
                profile columns:
                    columns:
                        - include %.%
                        - exclude %.%
            """,
            "all but id",
            id="all tables and columns included and then all excluded",
        ),
    ],
)
def test_profile_columns_inclusions_exclusions(scanner: Scanner, table_name, soda_cl_str, expectation):
    _table_name = scanner.ensure_test_table(table_name)
    scan = scanner.create_test_scan()
    mock_soda_cloud = scan.enable_mock_soda_cloud()
    scan.add_sodacl_yaml_str(soda_cl_str.format(table_name=_table_name))
    scan.execute(allow_error_warning=True)
    profiling_result = mock_soda_cloud.pop_scan_result()
    for table_result in profiling_result["profiling"]:
        if table_result["table"].lower().startswith("sodatest_customer"):
            column_names = [col_profile["columnName"] for col_profile in table_result["columnProfiles"]]
            if expectation == "all but id":
                assert "id" not in column_names
            elif expectation == "all but nothing":
                assert len(column_names) == 0
            else:
                assert "id" not in column_names
                assert "size" in column_names
                assert "country" not in column_names


def remove_datasource_and_table_name(results_dict: dict) -> dict:
    for i, _ in enumerate(results_dict["profiling"]):
        del results_dict["profiling"][i]["dataSource"]
        del results_dict["profiling"][i]["table"]
    return results_dict
