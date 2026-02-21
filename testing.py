#####
#
#       Testing Suite for Register Program
# 
#####

import utils.open_file as open_file
import tempfile
import os

##### File Handling

def normal_opening():
    with tempfile.TemporaryDirectory() as temp_directory:
        filepath = os.path.join(temp_directory, "text.txt")

        with open(filepath, "w") as file:
            file.write("hello world")
        result = open_file.openfile(filepath)
        assert result == "hello world", f"expected 'hello world', got {result!r}"

def file_not_found():
    try:
        open_file.openfile("nonexistant.txt")
        assert False, "Expected FileNotFound but nothing was raised"
    except SystemExit as e:
        assert e.code == 404, f"Expected exit code 404, got {e.code}"

def file_is_empty():
    try: 
        with tempfile.TemporaryDirectory() as temp_directory:
            filepath = os.path.join(temp_directory, "empty.txt")

            with open(filepath, "w") as file:
                file.write("")

            open_file.openfile(filepath)
            assert False, "Expected EmptyFile but nothing was Raised"
    except SystemExit as e:
        assert e.code == 204, f"Expected exit code 204, got {e.code}"

def wrong_encoding():
    try: 
        with tempfile.TemporaryDirectory() as temp_directory:
            filepath = os.path.join(temp_directory, "wrong-encoding.txt")

            with open(filepath, "wb") as file: #wb = write binary
                file.write(b"\xe9")

            open_file.openfile(filepath)
            assert False, "Expected UnicodeError but nothing was Raised"
    except SystemExit as e:
        assert e.code == 415, f"Expected exit code 415, got {e.code}"

def wrong_extension():
    try:
        with tempfile.TemporaryDirectory() as temp_directory:
            filepath = os.path.join(temp_directory, "wrong_extension.xls")

            with open (filepath, "w") as file:
                file.write("invalid extension")

            open_file.openfile(filepath)
            assert False, "Expected WrongExtension but nothing was Raised"
    except SystemExit as e:
        assert e.code == 415, f"Expected exit code 415, got {e.code}"

# Can't seem to test permission errors on windows?

def open_directory():
    try:
        with tempfile.TemporaryDirectory() as temp_directory:
            open_file.openfile(temp_directory)
            assert False, "Expected PermissionError but nothing was Raised"
    except SystemExit as e:
        assert e.code == 400, f"Expected exit code 400, got {e.code}"

file_handling_tests = [
    normal_opening,
    file_not_found, 
    file_is_empty, 
    wrong_encoding, 
    wrong_extension, 
    open_directory
]

file_handling_tests_passed = 0
file_handling_tests_number = len(file_handling_tests)








def final_report():
    all_tests_passed = file_handling_tests_passed
    all_tests_total = file_handling_tests_number
    if all_tests_passed == all_tests_total:
        print("\n\nALL TESTS PASSED\n\n\n")
    else:
        print(f"\n File Handling Tests:{file_handling_tests_passed}/{file_handling_tests_number}")

if __name__ == "__main__":

    for test in file_handling_tests:
        try:
            test()
            file_handling_tests_passed += 1
        except AssertionError as e:
            print(f"FAILED: {test.__name__} - {e}")

    final_report()