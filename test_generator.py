import itertools

import litmus_template
import instruction_template


def save_to_file(file_name, litmus):
    text_file = open(file_name, "w")
    text_file.write(litmus)
    text_file.close()


thread_options = [instruction_template.get_same_cta(),
                  instruction_template.get_diff_cta_same_gpu(),
                  instruction_template.get_diff_gpu()]


def generate_combinations(event_list):
    instructions = []
    for event in event_list:
        instructions.append(instruction_template.get_all_events(event))
    return itertools.product(*instructions)  # return cartesian product of instructions


# test cases
def generate_corr_tests(base_path, template):
    ind = 1
    combinations = generate_combinations(litmus_template.CORR_EVENT)
    file_names = []
    for thread_option in thread_options:
        for combination in combinations:
            litmus = template.get_corr(thread_option, combination)
            file_name = base_path + f"CoRR_{ind}.litmus"
            save_to_file(file_name, litmus)
            file_names.append(file_name)
            ind += 1
    return file_names


def generate_corwr_tests(base_path, template):
    ind = 1
    combinations = generate_combinations(litmus_template.CORWR_EVENT)
    file_names = []
    for thread_option in thread_options:
        for combination in combinations:
            litmus = template.get_corwr(thread_option, combination)
            file_name = base_path + f"CoRWR_{ind}.litmus"
            save_to_file(file_name, litmus)
            file_names.append(file_name)
            ind += 1
    return file_names


def generate_cowrr_tests(base_path, template):
    ind = 1
    combinations = generate_combinations(litmus_template.COWRR_EVENT)
    file_names = []
    for thread_option in thread_options:
        for combination in combinations:
            litmus = template.get_cowrr(thread_option, combination)
            file_name = base_path + f"CoWRR_{ind}.litmus"
            save_to_file(file_name, litmus)
            file_names.append(file_name)
            ind += 1
    return file_names


def generate_cowrwr_tests(base_path, template):
    ind = 1
    combinations = generate_combinations(litmus_template.COWRWR_EVENT)
    thread_option = [(0, 0)]
    file_names = []
    for combination in combinations:
        litmus = template.get_cowrwr(thread_option, combination)
        file_name = base_path + f"CoWRWR_{ind}.litmus"
        save_to_file(file_name, litmus)
        file_names.append(file_name)
        ind += 1
    return file_names


def generate_no_thin_air_tests(base_path, template):
    ind = 1
    combinations = generate_combinations(litmus_template.NO_THIN_AIR_EVENT)
    file_names = []
    for thread_option in thread_options:
        for combination in combinations:
            litmus = template.get_no_thin_air(thread_option, combination)
            file_name = base_path + f"NoThinAir_{ind}.litmus"
            save_to_file(file_name, litmus)
            file_names.append(file_name)
            ind += 1
    return file_names


def generate_sb_tests(base_path, template):
    ind = 1
    combinations = generate_combinations(litmus_template.SB_EVENT)
    file_names = []
    for thread_option in thread_options:
        for combination in combinations:
            litmus = template.get_sb(thread_option, combination)
            file_name = base_path + f"SB_{ind}.litmus"
            save_to_file(file_name, litmus)
            file_names.append(file_name)
            ind += 1
    return file_names


def generate_mp_tests(base_path, template):
    ind = 1
    combinations = generate_combinations(litmus_template.MP_EVENT)
    file_names = []
    for thread_option in thread_options:
        for combination in combinations:
            litmus = template.get_mp(thread_option, combination)
            file_name = base_path + f"MP_{ind}.litmus"
            save_to_file(file_name, litmus)
            file_names.append(file_name)
            ind += 1
    return file_names


def generate_all_tests(base_path, width):
    template = litmus_template.LitmusTemplates(width)
    file_names = []

    # file_names.extend(generate_corr_tests(base_path, template))
    # file_names.extend(generate_corwr_tests(base_path, template))
    # file_names.extend(generate_cowrr_tests(base_path, template))
    # file_names.extend(generate_cowrwr_tests(base_path, template))
    # file_names.extend(generate_no_thin_air_tests(base_path, template))
    # file_names.extend(generate_sb_tests(base_path, template))
    file_names.extend(generate_mp_tests(base_path, template))

    return file_names
