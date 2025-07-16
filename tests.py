from functions.run_python import run_python_file


if __name__ == "__main__":
    print("Result for  calc main.py test:")
    print(run_python_file("calculator", "main.py"))

    print("Result for calc tests.py test:")
    print(run_python_file("calculator", "tests.py"))

    print("Result for calc ../main.py test:")
    print(run_python_file("calculator", "../main.py"))

    print("Result for calc nonexistent.py test:")
    print(run_python_file("calculator", "nonexistent.py"))
