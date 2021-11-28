def main():
    date = datetime.date.today()
    width, file_sep = file_sep_width(HEADER, date)

    sep = len(TEXTS[1]) * "-"
    prompt_print(TEXTS, sep)

    if not os.path.isfile(FILE_PATH):
        create_file(HEADER, FILE_PATH, width, file_sep)

    guessed_nums = random_nums()
    guesses = 0
    start_time = time()

    while True:
        guesses += 1
        player = player_choice()
        result = bull_cow_conditions(player, guessed_nums)

        if win_condition(result, guesses):
            result_evaluation(guesses, EVALUATION)
            break
        else:
            print("{} {}/{} {}".format(*result))
            print(sep)
            continue

    end_time = time()
    elapsed_time = time_count(start_time, end_time)
    print_to_file(guesses, elapsed_time, guessed_nums, date, FILE_PATH,
                  width, file_sep)


def file_sep_width(head: tuple, dat) -> list:
    new_list = []
    width = [len(w) + 2 for w in head][:3]
    width.append(len(str(dat)) + 2)
    new_list.append(width)
    new_list.append((sum(width) + 5) * "-")
    return new_list


def prompt_print(text: tuple, sep: str) -> None:
    print(f"{text[0]:^{len(sep)}}\n{sep}\n{text[1]}\n{text[2]}\n{sep}\n"
          f"{text[3]}\n{sep}")


def random_nums() -> dict:
    guessed_dict = {}
    value = 0

    while not len(guessed_dict.keys()) == 4:
        n = choice(range(0, 10))

        if n in guessed_dict.keys():
            continue
        elif n == 0 and value == 0:
            continue
        else:
            guessed_dict.update({n: value})
            value += 1

    return guessed_dict


def player_choice() -> dict:
    while True:
        player_input = input(">>>")

        if input_num_check(player_input):
            continue
        elif input_len_check(player_input):
            continue
        else:
            player_dic = {int(n): i for i, n in enumerate(player_input)}

        if input_duplicate_check(player_dic):
            continue
        else:
            return player_dic


def input_num_check(player_input: str) -> bool:
    for n in player_input:
        if not n.isnumeric():
            print("Enter only numbers! Try it again:")
            return True
    return False


def input_len_check(player_input: str) -> bool:
    if len(player_input) != 4:
        print("Enter exactly 4 numbers! Try it again:")
        return True
    else:
        return False


def input_duplicate_check(nums: dict) -> bool:
    if len(nums) < 4:
        print("Your numbers must be unique! Try it again:")
        return True
    else:
        return False


def bull_cow_conditions(player: dict, guessed_nums: dict) -> list:
    result_list = [0, "bulls", 0, "cows"]

    for n in player.keys():
        if n in guessed_nums.keys():
            if player.get(n) == guessed_nums.get(n):
                result_list[0] += 1
            else:
                result_list[2] += 1

    if result_list[0] == 1:
        result_list.pop(1)
        result_list.insert(1, "bull")

    if result_list[2] == 1:
        result_list.pop(3)
        result_list.insert(3, "cow")

    return result_list


def win_condition(result: list, guesses: int) -> bool:
    if result[0] == 4:
        if guesses == 1:
            print("Congratulation, you've guessed right number\nin 1 guess!")
            return True
        else:
            print("Congratulation, you've guessed right number\nin {} guesses!"
                  .format(guesses))
            return True
    else:
        return False


def result_evaluation(guesses: int, ev: dict) -> None:
    for e in ev:
        if guesses <= e:
            print(f"That's {ev.get(e)}.")
            return None
    print("That's bad.")


def time_count(start, end) -> str:
    seconds = (end - start) % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    game_time = "%d:%02d" % (minutes, seconds)
    return game_time


def create_file(head: tuple, path: str, width: list, sep: str) -> None:
    try:
        with open(path, "w") as file:
            file.write("In this file you can see yours results ;)\n\n")
            file.write(f"{sep}\n")
            for i, n in enumerate(head):
                file.write(f'|{head[i]:^{width[i]}}')
            file.write(f"|\n{sep}")
    except FileNotFoundError:
        print("File not found.")


def print_to_file(
        num: int, g_t: str, g_num: dict, dat,
        path: str, width: list, sep: str) -> None:
    g_list = [str(n) for n in g_num]
    try:
        with open(path, "a") as file:
            file.write(f"\n|{num:<{width[0]}}|{g_t:<{width[1]}}|"
                       f"{''.join(g_list):<{width[2]}}|"
                       f"{str(dat):^{width[3]}}|")
            file.write("\n{}".format(sep))
    except FileNotFoundError:
        print("File not found... Can not write the results.")
    except FileExistsError:
        print("File not exist... Can not write the results.")


if __name__ == "__main__":
    import datetime
    import os
    import sys
    from random import choice
    from time import time

    TEXTS = "WELCOME TO BULLS & COWS.",\
            "I've generated a random 4 digit number for you.",\
            "Let's play a bulls and cows game.",\
            "ENTER NUMBERS:"
    HEADER = "Num of guesses", "Guess time", "Guess numbers", "Date"
    FILE_PATH = os.path.split(sys.argv[0])[0] + "/" + "results.txt"
    EVALUATION = {10: "amazing", 20: "average", 30: "not so good"}

    main()
