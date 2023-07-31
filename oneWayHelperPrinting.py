
# o print flow variable
def print3Darray(flow):

    for i in range(0, len(flow)):
        for j in range(0, len(flow[0])):
            print(f"[{flow[i][j][0]},{flow[i][j][1]}] , ", end="")
        print()

# TO PRINT GRID ARRAY


def printGrid(grid):
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if (len(grid[i][j]) < 5):
                print(f"    {grid[i][j]}   ", end="")
            else:
                print(f"{grid[i][j]},", end="")
        print("\n")


# TO PRINT GRID ARRAY
def printListGrid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (len(grid[i][j]) == 0):
                print("         []       ,", end="")
            else:
                print(grid[i][j], " , ", end="")
        print()

# TO PRINT GRID ARRAY


def printListGridReduced(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (len(grid[i][j]) == 0):
                print("        []        ,", end="")
            else:
                print(grid[i][j], " , ", end="")
        print()
