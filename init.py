rows = 'ABCDEFGHI'
cols = '123456789'

grid1 = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
grid2 = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
grid3 = '1....................2......3.....4..............5.......6.....7..8.............9'

# helper function:
# given two strings (a and b), func will return the list formed by all the
# possible concatenations of a letter s in string a with a letter t in string b
def cross(a,b):
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)
# returns sudoku board

row_units = [cross(r, cols) for r in rows]
# element example:
# row_units[0] = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']

column_units = [cross(rows, c) for c in cols]
# element example:
# column_units[0] = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']

square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# element example:
# square_units[0] = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']

diagonal_units = [[r+c for r,c in zip(rows,cols)],[r+c for r,c in zip(rows, cols[::-1])]]
# element example:
# diagonal_units[0] = ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']


unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
# set is an unordered collection of items. Every element is unique
# (no duplicates) and must be immutable (which cannot be changed)
# sum adds the items of an iterable and returns the sum
