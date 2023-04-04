structure1 = [[1, 4], [2, 5], [3, 6],
              [7, 10], [8, 11], [9, 12],
              [13, 16, 17], [14, 18, 19], [15, 20, 21],
              [22, 23, 28], [24, 25, 29], [26, 27, 30]]
structure2 = [[1, 6], [2, 4], [3, 5],
              [7, 12], [8, 10], [9, 11],
              [14, 16, 21], [15, 18, 17], [13, 20, 19],
              [22, 27, 29], [24, 23, 30], [26, 25, 28]]
structure3 = [[1, 5], [2, 6], [3, 4],
              [7, 11], [8, 12], [9, 10],
              [15, 16, 19], [13, 18, 21], [14, 20, 17],
              [22, 25, 30], [24, 27, 28], [26, 23, 29]]

### depending on which treatments are run, the subject number needs to be different and the group matrices are adjusted accordingly

del structure1[3:13]
del structure2[3:13]
del structure3[3:13]

append1 = [[7, 10, 11], [8, 12, 13], [9, 14, 15], [16, 17, 22], [18, 19, 22], [18, 23, 24]]
append2 = [[8, 10, 15], [9, 12, 11], [7, 14, 13], [16, 21, 23], [18, 17, 24], [20, 19, 22]]
append3 = [[9, 10, 13], [7, 12, 15], [8, 14, 11], [16, 19, 24], [18, 21, 22], [20, 17, 23]]

for i in append1:
    structure1.append(i)
for i in append2:
    structure2.append(i)
for i in append3:
    structure3.append(i)


del structure1[9:13]
del structure2[9:13]
del structure3[9:13]


del structure1[0:13]
del structure2[0:13]
del structure3[0:13]

append1 = [[1, 4, 5], [2, 6, 7], [3, 8, 9], [10, 11, 16], [12, 13, 17], [14, 15, 18]]
append2 = [[2, 4, 9], [3, 6, 5], [1, 8, 7], [10, 15, 17], [12, 11, 18], [14, 13, 16]]
append3 = [[3, 4, 7], [1, 6, 9], [2, 8, 5], [10, 13, 18], [12, 15, 16], [14, 11, 17]]

for i in append1:
    structure1.append(i)
for i in append2:
    structure2.append(i)
for i in append3:
    structure3.append(i)


del structure1[3:13]
del structure2[3:13]
del structure3[3:13]

append1 = [[7, 10, 11], [8, 12, 13], [9, 14, 15]]
append2 = [[8, 10, 15], [9, 12, 11], [7, 14, 13]]
append3 = [[9, 10, 13], [7, 12, 15], [8, 14, 11]]

for i in append1:
    structure1.append(i)
for i in append2:
    structure2.append(i)
for i in append3:
    structure3.append(i)


structure1 = [[1, 2, 7], [3, 4, 8], [5, 6, 9],
              [10, 11, 16], [12, 13, 17], [14, 15, 18],
              [19, 20, 25], [21, 22, 26], [23, 24, 27]]
structure2 = [[3, 2, 9], [5, 4, 7], [1, 6, 8],
              [12, 11, 18], [14, 13, 16], [10, 15, 17],
              [21, 20, 27], [23, 22, 25], [19, 24, 26]]
structure3 = [[5, 2, 8], [1, 4, 9], [3, 6, 7],
              [14, 11, 17], [10, 13, 18], [12, 15, 16],
              [23, 20, 26], [19, 22, 27], [21, 24, 25]]

del structure1[3:9]
print(structure1)
