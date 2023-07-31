def print3Darray(flow):

    for i in range(0, len(flow)):
        for j in range(0, len(flow[0])):
            print(f"[{flow[i][j][0]},{flow[i][j][1]}] , ", end="")
        print()


def printGrid(grid):
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if (len(grid[i][j]) < 5):
                print(f"    {grid[i][j]}   ", end="")
            else:
                print(f"{grid[i][j]},", end="")
        print("\n")


def printListGrid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (len(grid[i][j]) == 0):
                print("         []       ,", end="")
            else:
                print(grid[i][j], " , ", end="")
        print()


def printListGridReduced(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (len(grid[i][j]) == 0):
                print("        []        ,", end="")
            else:
                print(grid[i][j], " , ", end="")
        print()


def printConnected(connected):
    for i in range(0, len(connected)):
        for j in range(0, len(connected[i])):
            if (len(connected[i][j]) == 0):
                print("          ", end=" ")
            print(connected[i][j], end=" ")
        print()
