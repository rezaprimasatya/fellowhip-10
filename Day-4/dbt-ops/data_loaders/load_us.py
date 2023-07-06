import pandas as pd


@data_loader
def load_data(*args, **kwargs):
    url = "https://gist.githubusercontent.com/rezaprimasatya/bf84abf34b223cf942589d636b45b9ff/raw/91dcb4d97ee08a999a11347929155b9a636f14e5/us_chatgpt_ai.csv"
    return pd.read_csv(url)


@test
def test_output(output, *args) -> None:
    assert output["chatgpt"].dtype == object
    assert output["ai"].dtype == int
