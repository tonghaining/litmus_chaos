import time
from os import walk

import subprocess
import test_generator


def check_with_dat3m(litmus_file):
    start_time = time.time()
    repo_base_path = "/home/local/haintong/Documents/workspace/Dat3M/"
    command = f"java -jar {repo_base_path}dartagnan/target/dartagnan-3.1.1.jar {repo_base_path}cat/ptx.cat {litmus_file} --printer.afterSimplification=true --method=assume"
    command = command.split(" ")
    result_bytes = subprocess.run(command, stdout=subprocess.PIPE)
    result_string = result_bytes.stdout.decode('utf-8').split("\n")
    return result_string[-3] == "Ok", time.time() - start_time  # "Ok" or "No"


def check_with_alloy(litmus_file):
    start_time = time.time()
    command = f"python3 /home/haintong/Documents/workspace/mixedproxy/src/test_to_alloy.py {litmus_file}"
    command = command.split(" ")
    result_bytes = subprocess.run(command, stdout=subprocess.PIPE)
    result_string = result_bytes.stdout.decode('utf-8').split("\n")
    return result_string[-2] != "// Alloy exited with non-zero return code", time.time() - start_time  # false output


if __name__ == '__main__':
    base_path = "./litmus_result/"
    file_names = test_generator.generate_all_tests(base_path, 50)
    # file_names = [base_path + file for file in (next(walk(base_path), (None, None, []))[2])]
    dat3m_time = 0
    alloy_time = 0
    for i, file in enumerate(file_names):
        dat3m_result = check_with_dat3m(file)
        alloy_result = check_with_alloy(file)
        dat3m_time += dat3m_result[1]
        alloy_time += alloy_result[1]
        if dat3m_result[0] != alloy_result[0]:
            print(f"The test results are not same for: {file}")
        if i >= 20:
            break
    print(f"runtime of\n dat3m: {dat3m_time} s\n alloy: {alloy_time} s")