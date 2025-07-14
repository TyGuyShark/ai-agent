from functions.write_file import write_file


if __name__ == "__main__":
    print("Result for  calc loremt.txt test:")
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))

    print("Result for calc / pkg test:")
    print(write_file("calculator", "pkg/moerlorem.txt", "lorem ipsum dolor sit amet"))

    print("Result for /tmp/temp.txt test:")
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

    #print("Result for '../' directory:")
    #print(get_files_info("calculator", "../"))
