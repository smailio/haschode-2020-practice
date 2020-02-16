from cachetools import cached
from cachetools.keys import hashkey
import sys

sys.setrecursionlimit(16500)


def parse_input_file(path):
    with open(path, "r") as f:
        lines = f.readlines()
        [max_slice, nb_types] = tuple([int(s) for s in lines[0].split(" ")])
        nb_slices_of_pizza = tuple([int(s) for s in lines[1].split(" ")])
        return {
            "max_slice": max_slice,
            "nb_types": nb_types,
            "nb_slices_of_pizza": nb_slices_of_pizza,
        }


def solve(problem):
    return solve_rec(problem["max_slice"], problem["nb_slices_of_pizza"], tuple([]))


@cached(
    cache={},
    key=lambda max_slice, pizza_list, pizza_selected: hashkey(max_slice, pizza_list),
)
def solve_rec(max_slice, pizza_list, pizza_selected):
    if max_slice == 0:
        return pizza_selected
    without_this_pizza = solve_rec(max_slice, pizza_list[1:], pizza_selected)
    sum_without_this_pizza = sum(without_this_pizza)
    pizza_list = list(
        filter(lambda pizza: (pizza + sum_without_this_pizza) > max_slice, pizza_list)
    )
    if len(pizza_list) == 0:
        return pizza_selected
    nb_slice = pizza_list[0]
    with_this_pizza = solve_rec(
        max_slice - nb_slice, pizza_list[1:], pizza_selected + (nb_slice,)
    )
    if sum(with_this_pizza) > sum_without_this_pizza:
        return with_this_pizza
    else:
        return without_this_pizza


def main():
    path = ""
    problem = parse_input_file(path)
    print(solve(problem))


if __name__ == "__main__":
    main()
