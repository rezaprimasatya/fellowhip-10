OBJECT_COLUMNS = ["us_chatgpt", "india_chatgpt"]


@transformer
def convert_object_columns_to_integers(data, *args, **kwargs):
    """Convert all object columns to integers"""
    for column in OBJECT_COLUMNS:
        data[column] = data[column].apply(
            lambda x: 0 if x == "<1" else int(x)
        )
    return data

@test
def test_output(output, *args) -> None:
    for column in OBJECT_COLUMNS:
        assert output[column].dtype == int