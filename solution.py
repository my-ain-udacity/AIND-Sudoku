from utils import *

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

diagonal1 = [[rows[x] + cols[x] for x in range(len(cols))]]
diagonal2 = [[rows[x] + cols[(len(cols)-1) - x] for x in range(len(cols))]]

unitlist = row_units + column_units + square_units + diagonal1 + diagonal2

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - {s}) for s in boxes)

diagonal_units = [[r + c for r, c in zip(rows, cols)], [r + c for r, c in zip(rows, cols[::-1])]]
def is_filled_with_one(position):
    return len(position) == 1


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}
    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers
    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)
    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    potential_twins = [box for box in values.keys() if len(values[box]) == 2]
    naked_twins_found = [[box1, box2] for box1 in potential_twins for box2 in peers[box1] if
                         set(values[box1]) == set(values[box2])]

    for i in range(len(naked_twins_found)):
        box1 = naked_twins_found[i][0]
        box2 = naked_twins_found[i][1]
        peers1 = set(peers[box1])
        peers2 = set(peers[box2])
        peers_int = peers1 & peers2

        for peer_val in peers_int:
            if len(values[peer_val]) > 1:
                inner = values[box1]
                for rm_val in inner:
                    values = assign_value(values, peer_val, values[peer_val].replace(rm_val, ''))
    return values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle
    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.
    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}
    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    solved_values = [box for box in values.keys() if is_filled_with_one(values[box])]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(digit, ''))
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle
    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.
    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}
    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned
    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    for unit in unitlist:
        for digit in '123456789':
            places = [box for box in unit if digit in values[box]]
            if is_filled_with_one(places):
                values = assign_value(values, places[0], digit)
    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies
     Parameters
     ----------
     values(dict)
         a dictionary of the form {'box_name': '123456789', ...}
     Returns
     -------
     dict or False
         The values dictionary after continued application of the constraint strategies
         no longer produces any changes, or False if the puzzle is unsolvable
     """
    suspend = False
    while not suspend:
        solved_values = len([box for box in values.keys() if is_filled_with_one(values[box])])
        # rules
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        new_solved_values = len([box for box in values.keys() if is_filled_with_one(values[box])])
        suspend = solved_values == new_solved_values
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.
    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}
    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False
    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(is_filled_with_one(values[s]) for s in boxes):
        return values

    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.

        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    # noinspection PyBroadException
    try:
        import PySudoku

        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')