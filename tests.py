from functions.get_file_content import get_file_content


if __name__ == "__main__":
    print("Result for  calc / main test:")
    print(get_file_content("calculator", "main.py"))

    print("Result for calc / pkg test:")
    print(get_file_content("calculator", "pkg/calculator.py"))

    print("Result for '/bin/cat' directory:")
    print(get_file_content("calculator", "/bin/cat"))

    #print("Result for '../' directory:")
    #print(get_files_info("calculator", "../"))
