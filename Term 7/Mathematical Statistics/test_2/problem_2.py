# Defining the table
table = [
    [86, 574, 57],
    [55, 168, 15],
    [21, 51, 5],
    [12, 16, 2]
]
# Defining the values of number of rows and columns
r = 4
s = 3

# Calculating frequences \nu_{i.} and \nu_{.j}
nu_i = [sum(row) for row in table]
nu_j = [sum([row[i] for row in table]) for i in range(s)]

# Printing the frequences
print(f"nu_i: {nu_i}")
print(f"nu_j: {nu_j}")

# Now, calculating the total number of observations
n = sum(nu_i)
print(f"Total number of observations: {n}")

# Calculating the statistics n(sum_{ij} \nu_{ij}^2/(\nu_{i.}\nu_{.j}) - 1)
chi_square = 0
for i in range(r):
    for j in range(s):
        chi_square += table[i][j]**2 / (nu_i[i] * nu_j[j])

chi_square = n*(chi_square - 1)
print(f"Chi square statistics: {chi_square}")