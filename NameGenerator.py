import random


def process_file(filename, names, char_probs, order):
    infile = open(filename, 'r')
    underscores = '_' * order

    for line in infile:

        name = line.lower().strip()
        names.add(name)

        name = underscores + name + underscores

        process_name(name, char_probs, order)

    infile.close()


def process_name(name, char_probs, order):
    for i in range(0, len(name) - 2*order + 1):
        sequence = name[i:i+order]
        next_char = name[i + order]

        if sequence not in char_probs:
            char_probs[sequence] = dict()

        if next_char not in char_probs[sequence]:
            char_probs[sequence][next_char] = 1
        else:
            char_probs[sequence][next_char] += 1


def convert_count_to_prob(char_probs):
    for sequence in char_probs:
        total = sum(char_probs[sequence].values())
        for next_char in char_probs[sequence]:
            char_probs[sequence][next_char] /= total


def generate_name(char_probs, order):
    sequence = '_' * order
    name = ''
    done = False

    while not done:
        rand = random.random()
        for next_char in char_probs[sequence]:
            if rand < char_probs[sequence][next_char]:
                if next_char == '_':
                    done = True
                else:
                    name += next_char
                    sequence = sequence[1:] + next_char
                break
            else:
                rand -= char_probs[sequence][next_char]

    return name


def generate_names(char_probs, name_set, order, min_length, max_length, quantity):
    names = []
    name = ''

    while len(names) < quantity:
        while (len(name) < min_length) or (len(name) > max_length) or (name in name_set):
            name = generate_name(char_probs, order)
        names.append(name.capitalize())
        name = ''
    return names


def main():

    done = False

    while not done:

        male_names = set()
        female_names = set()

        male_char_probs = dict()
        female_char_probs = dict()

        gender = input("Select a gender M or F: ").lower()

        if (gender != 'm') and (gender != 'f'):
            print("Invalid input - please enter M or F for gender\n")
            continue

        try:
            order = int(input("Enter order for Markov model: "))
            min_length = int(input("Enter min name length: "))
            max_length = int(input("Enter max name length: "))
            quantity = int(input("Enter number of names to generate: "))
        except ValueError:
            print("Invalid input - you must enter an integer value\n")
            continue

        char_probs = male_char_probs if gender == 'm' else female_char_probs
        name_set = male_names if gender == 'm' else female_names
        filename = 'namesBoys.txt'if gender == 'm' else 'namesGirls.txt'

        process_file(filename, name_set, char_probs, order)

        convert_count_to_prob(male_char_probs)
        convert_count_to_prob(female_char_probs)

        names = generate_names(char_probs, name_set, order, min_length, max_length, quantity)
        print("\nNEW NAMES:")
        for name in names:
            print(name)

        choice = input("Would you like to generate more names (Y/N)? ").lower()
        done = False if choice == 'y' else True


main()








