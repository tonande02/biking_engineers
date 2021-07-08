from src.source_to_raw.source_to_raw import read_file

def test_read_file_function():
    # Arrange:
    filepath = "data/testing/source/data.txt"

    # Act:
    data = read_file(filepath)
    print(data)

    # Assert:
    assert isinstance(data, list)
    assert isinstance(data[0], str)
    for item in data:
        assert isinstance(item, str)


    