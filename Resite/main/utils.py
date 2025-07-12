from random import shuffle
def generate_templates(count):
    variants = 0
    while True:
        if count % 2 == 0:
            count //= 2
            variants += count
        else:
            break
    return [i for i in range(variants)]


def initialize_list_data(list_item):
    # Standardize line breaks
    normalized = list_item.people.replace("\r\n", "\n").replace("\r", "\n")
    people = normalized.split('\n')
    # Make the number of elements even
    count = len(people)
    if count % 2 == 1:
        people.append('')
        count += 1
    list_item.item_count = count
    # Saving a shuffled version of the list (to make element order irrelevant)
    shuffle(people)
    list_item.people_array = [people]
    # Saving templates
    list_item.templates = generate_templates(count)


def split(parts, part_size):
    new_parts = []
    for part in parts:
        new_parts.append(part[:part_size])
        new_parts.append(part[part_size:])
    return new_parts


def resit_by_template(list_, template):
    part_size = len(list_[0]) // 2
    list_ = split(list_, part_size)
    while True:
        if template >= part_size:
            template -= part_size
            part_size //= 2
            list_ = split(list_, part_size)
        else:
            break
    pairs = []
    for i in range(0, len(list_), 2):
        for o in range(part_size):
            pairs.append([list_[i][o], list_[i + 1][(o + template) % part_size]])
    return pairs