from init import *
import itertools

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def grid_values(grid):
    """
    Converts grid string into {<box>: <value>} dict with '.' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """
    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
    return dict(zip(boxes, grid))


def grid_values_withhint(grid):
    """
    Converts grid string into {<box>: <value>} dict with '.' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    values = []
    all_digits = '123456789'
    for elem in grid:
        if elem == '.':
            values.append(all_digits)
        else:
            values.append(elem)
    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
    return dict(zip(boxes, values))


def eliminate(values):
    """
    Eliminates values from peers of each box with a single value.
    Goes through all the boxes, and whenever there is a box with a single value,
    eliminates this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values


def only_choice(values):
    """
    Modifies all values that are the only choice for a unit.
    Goes through all the units, and whenever there is a unit with a value
    that only fits in one box, assigns the value to this box.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def naked_twins(values):
    """
    Eliminate values using the naked twins strategy.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # find box in unit of unitlist that has a value length of 2
    for unit in unitlist:
        # add box of len 2 to list for inspection
        twins = [box for box in unit if len(values[box]) == 2]
        # inspect if box of len 2 has a twin within the same unit
        potential_naked_twins = [list(twin) for twin in itertools.combinations(twins, 2)]
        # further inspect formed twins
        for a,b in potential_naked_twins:
            # value to replace peers
            naked_value = values[a]
            # expose naked_twins
            if values[a] == values[b]:
                for box in unit:
                    # exclude naked_twins from value replacement
                    if box != a and box != b:
                        # replace each digit of value
                        for digit in naked_value:
                            values[box] = values[box].replace(digit,'')
    return values


# solving with constraint propagation
def reduce_puzzle(values):
    """
    Iterates eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.

    Args:
        value: A sudoku in dictionary form.
    Returns:
        The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the Naked Twins Strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

# solving with search
def search(values):
    """
    Using depth-first search and propagation
    Try all possible values.
    """
    values = reduce_puzzle(values)
    if values is False:
        return False ##failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ##success
    # choose box with fewest possibilities
    n,s = min((len(values[s]),s) for s in boxes if len(values[s]) > 1)
    # recurrence
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def initiation():
    """
    Game initiation (helper)
    """
    beginnerlevel = 1
    advancedlevel = 2
    expertlevel = 3
    print("Sudoku" "\n" "Code by Philipp Bechhaus" "\n" "\n")
    while True:
        try:
            difficulty = int(input("How hard should we go?: " "\n" "\n" "Select" "\n" "1 for BEGINNER"
                           "\n" "2 for ADVANCED" "\n" "3 for PRO" "\n" "\n"))
        except ValueError:
            print("That's not a number!")
        else:
            if beginnerlevel <= difficulty <= expertlevel:
                break
            else:
                print("We're not there yet..")
    return difficulty

def run():
    """
    Game execution
    """
    difficulty = initiation()
    if difficulty == 1:
        values1 = grid_values(grid1)
        values2 = eliminate(grid_values_withhint(grid1))
        values3 = search(values2)
    if difficulty == 2:
        values1 = grid_values(grid2)
        values2 = eliminate(grid_values_withhint(grid2))
        values3 = search(values2)
    if difficulty == 3:
        values1 = grid_values(grid3)
        values2 = eliminate(grid_values_withhint(grid3))
        values3 = search(values2)
    display(values1)
    print("\n""\n")
    raw_input("Press ENTER to see hints...")
    print("\n""\n")
    display(values2)
    print("\n""\n")
    raw_input("Press ENTER to solve Sudoku...")
    print("\n""\n")
    display(values3)
    print("\n""\n")
    print("Cool!")
    print("\n""\n")

if __name__ == '__main__':
    run()
