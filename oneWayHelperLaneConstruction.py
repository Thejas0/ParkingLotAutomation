
def gridToCoord(row, col):
    '''
    # mapping for row,col to coordinates
    row -  no of rows 
    cols -  no of columns
    '''
    row = -row
    multiplier = 3.5
    x0 = col*multiplier
    y0 = row*multiplier - multiplier/2
    s = f"{x0} {y0}"
    return s


def spLine(x0, y0, x1, y1):
    """
    # FUNCTION TO GENERATE POINTS FOR SPLINE CREATION
    x0 - row1
    y0 - col1
    x1 - row2
    y1 - col2 
    """
    n = 50
    xDif = x1-x0
    yDif = y1-y0
    XGap = xDif/n
    YGap = yDif/n
    listX = [x0]
    listY = [y0]
    for i in range(0, n):
        listX.append(x0+XGap)
        listY.append(y0+YGap)
        x0 += XGap
        y0 += YGap

    ans = "LINESTRING"
    ans += "("
    for i in range(0, len(listX)-1):
        ans += f"{listX[i]} "
        ans += f"{listY[i]}"
        if i != len(listX)-2:
            ans += ' , '
    ans += ")"
    # print(ans)
    return ans


def checkForStart(grid, i, j, angle1, row, col):
    """
        # this function helps to identify the start of the link
        grid - 3D grid 
        i,j - positionl corrdinates of grid
        angle1 - angle of driveway
        row - no o rows
        col - no of cols 
    """
    if (i < 0 or j < 0 or i >= row or j >= col):
        return True
    for k in range(0, len(grid[i][j])):
        item1 = grid[i][j][k]
        item1 = item1.strip()
        item1 = item1.split()
        if (len(item1) < 3):
            return True

        angle2 = int(item1[2])
        if (angle1 == angle2):
            return False
    return True


def dfs(grid, i, j, angle1, check):
    """
        # for getting the length of the link in terms of no of blocks
        grid - 3D grid 
        i,j - positionl corrdinates of grid
        angle1 - angle of driveway
        check - list 

    """
    m = len(grid)
    n = len(grid[0])
    print(angle1, i, j)
    if (i < 0 or j < 0 or i >= m or j >= n):
        print("exit overbound")
        return 0
    for k in range(0, len(grid[i][j])):
        item1 = grid[i][j][k]

        item1 = item1.strip()
        item1 = item1.split()
        # print(item1)
        if (len(item1) < 3):
            return 0
        angle2 = int(item1[2])
        print("       ",  angle2, i, j)
        if (angle2 == angle1):
            return 1+dfs(grid, i+check[0], j+check[1], angle1, check)
    return 0


def getItem2(gridReduced, i, j, angle1):
    for k in range(0, len(gridReduced[i][j])):
        item = gridReduced[i][j][k].strip().split()
        angle2 = int(item[2])
        if (angle1 == angle2):
            return item
    return -1


def getStartItem(grid, start):
    """
        # gives first link item 
        grid - 3d array
        start - contains start coordinates
    """
    x = start[0]
    y = start[1]
    for k in range(len(grid[x][y])):
        item = grid[x][y][k].strip().split()
        print(item)
        if (len(item) == 0):
            continue
        print(item[0])
        if (item[0] == 'SD'):
            print("found start")
            return item
    return 'no start'

# gives end link item


def getEndItem(grid, start, blocks):
    """
        # get end link item
        grid - 3d array
        start - contains start coordinates
    """
    x = start[0]
    y = start[1]+1
    for k in range(len(grid[x][y])):
        item = grid[x][y][k].strip().split()
        if (len(item) == 0):
            continue
        print(item[0])
        if (item[0] == 'D' and int(item[2]) == 90):
            print("found the end")
            return item
    return 'no end'
