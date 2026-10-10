
import numpy as np
import pandas as pd
import pytest

from src.data import (
    COLUMN_NAMES,
    validate_schema,
    rename_columns,
    load_data,
)


# Du lieu mau hop le
SAMPLE = {
    "cement": 300.0,
    "slag": 60.0,
    "fly_ash": 80.0,
    "water": 180.0,
    "superplasticizer": 7.0,
    "coarse_aggregate": 1000.0,
    "fine_aggregate": 800.0,
    "age": 28,
    "strength": 38.0,
}


# TEST 1: Du lieu hop le
def test_valid_schema():
    df = pd.DataFrame([SAMPLE])
    result = validate_schema(df)

    assert len(result) == 1
    assert list(result.columns) == COLUMN_NAMES


# TEST 2: Gia tri khong hop le
@pytest.mark.parametrize(
    "field,value",
    [
        ("cement", -10),
        ("water", -1),
        ("age", 0),
        ("age", 28.5),
        ("strength", 0),
        ("cement", np.nan),
        ("cement", np.inf),
        ("cement", "abc"),
    ],
)
def test_invalid_schema_values(field, value):
    data = SAMPLE.copy()
    data[field] = value

    df = pd.DataFrame([data])

    with pytest.raises(ValueError):
        validate_schema(df)


# TEST 3: Thieu cot
def test_missing_column():
    data = SAMPLE.copy()
    data.pop("water")

    df = pd.DataFrame([data])

    with pytest.raises(ValueError):
        validate_schema(df)


# TEST 4: Sai thu tu cot
def test_wrong_column_order():
    df = pd.DataFrame([SAMPLE])

    df = df[COLUMN_NAMES[::-1]]

    with pytest.raises(ValueError):
        validate_schema(df)


# TEST 5: Dataset rong
def test_empty_dataset():
    df = pd.DataFrame(columns=COLUMN_NAMES)

    with pytest.raises(ValueError):
        validate_schema(df)

# ==========================================
# TEST 6: DOI TEN COT DU LIEU GOC UCI
# ==========================================

def test_rename_original_uci_columns():

    raw_df = load_data()

    result = rename_columns(raw_df)

    assert list(result.columns) == COLUMN_NAMES
    assert len(result) == 1030


# ==========================================
# TEST 7: PHAT HIEN COT BI DAO THU TU
# ==========================================

def test_rename_rejects_swapped_columns():

    raw_df = load_data().copy()

    columns = list(raw_df.columns)

    columns[0], columns[1] = (
        columns[1], columns[0]
    )

    raw_df.columns = columns

    with pytest.raises(ValueError):
        rename_columns(raw_df)


# ==========================================
# TEST 8: CHAP NHAN TEN COT CHUAN
# ==========================================

def test_rename_standard_columns():

    df = pd.DataFrame([SAMPLE])

    result = rename_columns(df)

    assert list(result.columns) == COLUMN_NAMES
    assert result.shape == (1, 9)
