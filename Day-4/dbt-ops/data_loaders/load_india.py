import pandas as pd


@data_loader
def load_data_from_api(*args, **kwargs):
    url = "https://gist.githubusercontent.com/rezaprimasatya/605070a0e165f028a2b8fb2f82b7c5ea/raw/0d72155141bd7e718e0a837a635a66792954a850/india_chatgpt_ai.csv"
    data = pd.read_csv(url)
    return data


@test
def test_output(output, *args) -> None:
    assert output["chatgpt"].dtype == object
    assert output["ai"].dtype == int
