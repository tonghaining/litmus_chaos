import subprocess

import litmus_template
import instruction_template


def save_to_file(file_name, litmus):
    text_file = open(file_name, "w")
    text_file.write(litmus)
    text_file.close()


def check_with_dat3m(litmus_file):
    base_path = "/home/local/haintong/Documents/workspace/Dat3M/"
    command = f"java -jar {base_path}dartagnan/target/dartagnan-3.1.1.jar {base_path}cat/ptx.cat {litmus_file} --printer.afterSimplification=true --method=assume"
    command = command.split(" ")
    result_bytes = subprocess.run(command, stdout=subprocess.PIPE)
    result_string = result_bytes.stdout.decode('utf-8').split("\n")
    return result_string[-3] == "Ok"  # "Ok" or "No"


def check_with_alloy(litmus_file):
    command = f"python3 /home/haintong/Documents/workspace/mixedproxy/src/test_to_alloy.py {litmus_file}"
    command = command.split(" ")
    result_bytes = subprocess.run(command, stdout=subprocess.PIPE)
    result_string = result_bytes.stdout.decode('utf-8').split("\n")
    return result_string[-2] != "// Alloy exited with non-zero return code"  # false output


if __name__ == '__main__':
    template = litmus_template.LitmusTemplates(30)
    threads = [(0, 0), (1, 1)]
    instruction_template = [instruction_template.get_random_store(), instruction_template.get_random_load(),
                            instruction_template.get_random_load()]
    example = template.get_corr(threads, instruction_template)
    file_name = "./example.litmus"
    save_to_file(file_name, example)
    print(check_with_dat3m(file_name) == check_with_alloy(file_name))
