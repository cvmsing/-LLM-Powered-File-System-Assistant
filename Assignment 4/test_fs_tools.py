from fs_tools import (
    read_file,
    list_files,
    write_file,
    search_in_file
)


print("========== READ FILE ==========")

result = read_file("resumes/resume1.pdf")

print(result)


print("\n========== LIST FILES ==========")

files = list_files("resumes")

for file in files:
    print(file)


print("\n========== LIST PDF FILES ==========")

pdf_files = list_files("resumes", ".pdf")

for file in pdf_files:
    print(file)


print("\n========== WRITE FILE ==========")

result = write_file(
    "output/test.txt",
    "Java Developer\nSpring Boot\nPython"
)

print(result)


print("\n========== SEARCH FILE ==========")

result = search_in_file(
    "output/test.txt",
    "java"
)

print(result)
