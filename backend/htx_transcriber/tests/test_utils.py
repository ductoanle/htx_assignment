from htx_transcriber.utils import (
    add_file_version,
    split_file_name
)


def test_split_file_name():
    assert split_file_name("test.mp3") == ("test", ".mp3")
    assert split_file_name("test_ver_1.mp3") == ("test_ver_1", ".mp3")
    assert split_file_name("test.ver_2.mp3") == ("test.ver_2", ".mp3")
    assert split_file_name("test_ver_3.m_3") == ("test_ver_3", ".m_3")


def test_add_file_version():
    assert add_file_version("test.mp3") == "test_ver_1.mp3"
    assert add_file_version("test_ver_1.mp3") == "test_ver_2.mp3"
    assert add_file_version("test_2_ver_2.mp3") == "test_2_ver_3.mp3"
    assert add_file_version("test3.mp3") == "test3_ver_1.mp3"
    assert add_file_version("test_ver_3.mp3") == "test_ver_4.mp3"
