import random

FENCE = 'fence'
LD = 'ld'
ST = 'st'

BAR_SYNC = '.bar_sync'
ACQ_REL = '.acq_rel'
ACQUIRE = '.acquire'
RELEASE = '.release'
RELAXED = '.relaxed'
WEAK = '.weak'

CTA = '.cta'
GPU = '.gpu'
SYS = '.sys'

load_instructions = [LD + WEAK]
store_instructions = [ST + WEAK]
fence_instructions = []

for sem in [ACQUIRE, RELAXED]:
    for scope in [CTA, GPU, SYS]:
        load_instructions.append(LD + sem + scope)

for sem in [RELEASE, RELAXED]:
    for scope in [CTA, GPU, SYS]:
        store_instructions.append(ST + sem + scope)

for sem in [BAR_SYNC, ACQ_REL]:
    for scope in [CTA, GPU, SYS]:
        fence_instructions.append(FENCE + sem + scope)


def get_random_load():
    return random.choice(load_instructions)


def get_random_store():
    return random.choice(store_instructions)


def get_random_fence():
    return random.choice(fence_instructions)


def get_all_events(event):
    if event == ST:
        return store_instructions
    elif event == LD:
        return load_instructions
    elif event == FENCE:
        return fence_instructions
    else:
        raise Exception(f"Invalid Event: {event}")


def get_same_cta():
    return [(0, 0), (0, 0)]


def get_diff_cta_same_gpu():
    return [(0, 0), (1, 0)]


def get_diff_gpu():
    return [(0, 0), (0, 1)]
