import random


def process_file(filename, names, char_counts, order):
    """Reads a text file containing a list of first names,
    adds each name to a set, and prepares the name for further processing"""
    infile = open(filename, 'r')
    underscores = '_' * order

    for line in infile:

        name = line.lower().strip()
        names.add(name)

        name = underscores + name + underscores

        process_name(name, char_counts, order)

    infile.close()


def process_name(name, char_counts, order):
    """Builds a 2D dictionary with a sequence of one or more characters as the outer key,
    the next character that follows this sequence as the inner key, and
    the number of times this character follows the character sequence as the value"""
    for i in range(0, len(name) - 2*order + 1):
        char_sequence = name[i:i+order]
        next_char = name[i + order]

        if char_sequence not in char_counts:
            char_counts[char_sequence] = dict()

        if next_char not in char_counts[char_sequence]:
            char_counts[char_sequence][next_char] = 1
        else:
            char_counts[char_sequence][next_char] += 1


def convert_count_to_prob(char_counts):
    """Reads a 2D dictionary containing the counts of characters that follow a particular sequence
     and converts counts to percentages"""
    for char_sequence in char_counts:
        total = sum(char_counts[char_sequence].values())
        for next_char in char_counts[char_sequence]:
            char_counts[char_sequence][next_char] /= total


def generate_name(char_probs, order):
    """Generates a single new name given a 2D dictionary of probabilities and Markov order"""
    char_sequence = '_' * order
    name = ''
    done = False

    while not done:
        rand = random.random()
        for next_char in char_probs[char_sequence]:
            if rand < char_probs[char_sequence][next_char]:
                if next_char == '_':
                    done = True
                else:
                    name += next_char
                    char_sequence = char_sequence[1:] + next_char
                break
            else:
                rand -= char_probs[char_sequence][next_char]

    return name


def generate_names(char_probs, names, order, min_length, max_length, quantity):
    """Generates a list of names given a 2D dictionary of probabilities, Markov order, minimum name length,
     maximum name length, and quantity of names to generate"""
    new_names = []
    name = ''

    while len(new_names) < quantity:
        while (len(name) < min_length) or (len(name) > max_length) or (name in names):
            name = generate_name(char_probs, order)
        new_names.append(name.capitalize())
        name = ''
    return new_names


def main():

    done = False

    while not done:

        names = set()
        char_probs = dict()

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

        filename = 'namesBoys.txt'if gender == 'm' else 'namesGirls.txt'

        process_file(filename, names, char_probs, order)

        convert_count_to_prob(char_probs)

        names = generate_names(char_probs, names, order, min_length, max_length, quantity)

        print("\nNEW NAMES:")
        for name in names:
            print(name)

        choice = input("Would you like to generate more names (Y/N)? ").lower()
        done = False if choice == 'y' else True


main()








