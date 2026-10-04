import pandas as pd

from src.preprocessing import missing_value_counts


def test_missing_value_counts():
    df = pd.DataFrame(
        {
            "Age": [20, None, 30],
            "Fare": [10, 20, None],
        }
    )

    result = missing_value_counts(df)

    assert result["Age"] == 1
    assert result["Fare"] == 1
