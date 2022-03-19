import src.io_interface as io_interface


def test_io():
    source = io_interface.SourceCode("./examples/bubble_sort.smpl")
    source.read_words()
