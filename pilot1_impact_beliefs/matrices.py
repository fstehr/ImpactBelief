import random
from math import ceil
from tabulate import tabulate


# Create the basic list of 100 os
columns = 20
dimension = columns ** 2
print(columns, dimension)
list_of_os = ['o'] * dimension
# print(list_of_os)

# Create lists of Xs (different numbers)
number_Xs_low = [30, 40, 50, 60, 70, 80, 90]
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
    
    print("\\begin{frame}")    
    exec('print("This is Table", index, "with", %s, "Xs")' % i)
    print("\\end{frame}")    
    print()
    print("\\begin{frame}")
    print("\\resizebox{\linewidth}{!}{")
    print("\\texttt{")
    exec("print(tabulate(matrix_%s, tablefmt='latex'))" % i)
    print("}")
    print("}")
    print("\\end{frame}")
    print()
