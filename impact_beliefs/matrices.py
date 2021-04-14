import random
from math import ceil
from tabulate import tabulate

"""
# Create the basic list of 100 os
columns = 20
dimension = columns ** 2
print(columns, dimension)
list_of_os = ['o'] * dimension
# print(list_of_os)

# Create lists of Xs (different numbers)
number_Xs_low = [int(0.1*dimension), int(0.2*dimension), int(0.3*dimension)]
number_Xs_high = [dimension - i for i in number_Xs_low]
number_Xs = number_Xs_low + number_Xs_high
print('number Xs is', number_Xs)

# Creates n=len(number_Xs) lists called matrix_[number_Xs] with len(matrix_%)=100 and the respective share of xs and os
# and randomly shuffles them.

for i in number_Xs:
    # generates the content for the matrices and shuffles it
    helplist = ['X'] * i + ['o'] * (dimension - i)
    random.shuffle(helplist)

    # splits these lists into a list of lists with length equal to the number of columns
    helpchunks = [
        helplist[j * columns:(j * columns) + columns]
        for j in range(ceil(len(helplist) / columns))
    ]
    # store these matrices in a variable called e.g. matrix_10
    exec("matrix_%s = helpchunks" % i)

    # export these tables as latex tables
    # includes latex formatting s.t. entire output can simply be copy+pasted into tex file
    index = number_Xs.index(i) + 1
    print()
    
    # OBS make this white font so that you can see it in the latex document but not in the screenshots
    
    exec('print("This is Table", index, "with", %s, "Xs")' % i)
    print()
    print("\\texttt{")
    exec("print(tabulate(matrix_%s, tablefmt='latex'))" % i)
    print("}")
    print()
    print("\\pagebreak")
"""

beliefs_neutral = [0]*3   # replace 3 with len(paras)
print(beliefs_neutral)

beliefs_neutral[1] = 3     # replace list lookup with project_id - 1 and 3 with player.num_x_belief
print(beliefs_neutral)



