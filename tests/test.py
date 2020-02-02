import glob
import subprocess
import re

# this test is currently not working. will fix later.
files = glob.glob("./*.py")
files.remove("./test.py")
files = [x for x in files if re.search(r".sutd.py$", x) is None]

for file in files:
    newfile = re.sub(r"\.py$", ".sutd.py", file)
    obfs_result = subprocess.run(
        ["python3", "-m", "../sutdobfs", file, newfile], capture_output=True
    )
    file_result = subprocess.run(["python3", file], capture_output=True)
    newfile_result = subprocess.run(["python3", newfile], capture_output=True)
    try:
        assert file_result.stdout == newfile_result.stdout
    except:
        print(file, "failed!")
        raise

print("all tests passed!")
