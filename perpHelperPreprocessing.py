from perpMainInputs import *


def genenateDesiredOutput(flow, file):
    """
    # FUNCTION WHICH CONSIDERS INPUT AND GIVES DESIRED OUTPUT FOR FURTHER PROCESS

    flow - 3d grid which helps in representing tthe direction of driveway
    file - filename of input txt file
    """
    for i in range(0, len(flow)):
        for j in range(0, len(flow[0])):
            flag = 0
            s = f"{i} {j} Drive "
            s1 = s
            if (flow[i][j][0] > 0):
                flag = 1
                s += str(270)
                s += "\n"
                file.writelines(s)
            if (flow[i][j][0] < 0):
                if (flag == 1):
                    s = f"{i} {j} Drive "
                flag = 1
                s += str(90)
                s += "\n"
                file.writelines(s)
            if (flow[i][j][1] > 0):
                if (flag == 1):
                    s = f"{i} {j} Drive "
                flag = 1
                s += str(180)
                s += "\n"
                file.writelines(s)
            if (flow[i][j][1] < 0):
                if (flag == 1):
                    s = f"{i} {j} Drive "
                flag = 1
                s += str(0)
                s += "\n"
                file.writelines(s)


def encodeFill(s, grid, x, y, length, temp):
    """
        helper function for encode fill which fills the grid
        s - item to be filled in grid
        x,y - positional parameters
        length - length of link
        temp -  list which determine the direction of flow
    """
    for i in range(1, length):
        x += temp[0]
        y += temp[1]
        grid[x][y].append(s)


def encodeGrid(row, col, angle, grid, ct, length):
    """
        function which consider input and fills the grid
        row ,col- positional paramters
        angle - angle of the object
        gridd - 3d arrau
        ct - to represent unique id of link
        length -length of link  
    """
    rowCopy = row
    link = 0
    row = -row
    temp = [False, False]
    temp1 = [False, False]
    s = "D "+f"{ct} "+f"{angle} "
    grid[rowCopy][col].append(s)
    # x1 decreases
    if (angle == 0):
        encodeFill(s, grid, rowCopy, col, length, [0, 1])
        # grid[rowCopy][col+width].append(s)

    # y1 increases
    elif (angle == 90):
        encodeFill(s, grid, rowCopy, col, length, [-1, 0])
        # grid[rowCopy-width][col].append(s)

    # y1 decreases
    elif (angle == 270):
        encodeFill(s, grid, rowCopy, col, length, [1, 0])
        # grid[rowCopy+width][col].append(s)

    else:
        encodeFill(s, grid, rowCopy, col, length, [0, -1])
        # grid[rowCopy][col-width].append(s)
        col += 1

    return link


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

# a dfs function which gives the extend of no of blocks in a link


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


def identifyStartLinks(grid, gridReduced, count):
    """
     identify the start of the link
     grid - 3d grid
     gridReduced - refined grid (for reducing no of links)
    """
    reducedLinkIndex = 1
    # global count
    row = len(grid)
    col = len(grid[0])
    pos = 1
    for i in range(0, row):
        for j in range(0, col):
            if (len(grid[i][j]) == 0):
                continue
            for k in range(0, len(grid[i][j])):
                item1 = grid[i][j][k]

                item1 = item1.strip()
                item1 = item1.split()
                if (len(item1) < 3):
                    continue

                angle1 = int(item1[2])

                if (angle1 == 270):
                    flag = checkForStart(grid, i-1, j, angle1, row, col)
                    if (flag):
                        s = "SD "+f"{reducedLinkIndex} "+f"{angle1} "
                        check = [1, 0]
                        noOfBlocks = dfs(grid, i, j, angle1, check)
                        s += f"{pos} {noOfBlocks} "
                        gridReduced[i][j].append(s)
                        reducedLinkIndex += 1
                        count += 1
                        continue

                elif (angle1 == 90):
                    flag = checkForStart(grid, i+1, j, angle1, row, col)
                    if (flag):
                        s = "SD "+f"{reducedLinkIndex} "+f"{angle1} "
                        check = [-1, 0]
                        noOfBlocks = dfs(grid, i, j, angle1, check)
                        s += f"{pos} {noOfBlocks} "
                        gridReduced[i][j].append(s)
                        reducedLinkIndex += 1
                        count += 1
                        continue

                elif (angle1 == 180):
                    flag = checkForStart(grid, i, j+1, angle1, row, col)
                    if (flag):
                        s = "SD "+f"{reducedLinkIndex} "+f"{angle1} "
                        check = [0, -1]
                        noOfBlocks = dfs(grid, i, j, angle1, check)
                        s += f"{pos} {noOfBlocks} "
                        gridReduced[i][j].append(s)
                        reducedLinkIndex += 1
                        count += 1
                        continue

                elif (angle1 == 0):
                    flag = checkForStart(grid, i, j-1, angle1, row, col)
                    if (flag):
                        s = "SD "+f"{reducedLinkIndex} "+f"{angle1} "
                        check = [0, 1]
                        noOfBlocks = dfs(grid, i, j, angle1, check)
                        s += f"{pos} {noOfBlocks} "
                        gridReduced[i][j].append(s)
                        reducedLinkIndex += 1
                        count += 1
                        continue
    return count

# dfs function to fill thegrid to reduce the number of links


def fill(grid, row, col, check, index, pos, blocks, angle):
    """
        to fill the empty spaces in the grid in the driveway path
        grid - 3d array
        row,col - position parameters
        check -- list to determine direction
        index -  unique identifier for link
        pos - poa of the link
        blocks - no of block the link will span
        angle - direction of link
    """
    temp = pos
    for _ in range(0, blocks-1):
        s = f"D {index} {angle} {temp+1}"
        row = row+check[0]
        col = col+check[1]
        grid[row][col].append(s)
        temp += 1

# fundamental function which initiates the reduction of link
# how ? in the previous code i made use of grid matrix which has encoding of drivelane
# and using that given an index i run a dfs call for a particular angle


def fillGrid(grid):
    """
        to fill the empty spaces in the grid in the driveway path
        grid - 3d array

    """
    m = len(grid)
    n = len(grid[0])

    for i in range(0, m):
        for j in range(0, n):
            for k in range(0, len(grid[i][j])):
                item = grid[i][j][k].strip().split()
                if (len(item) == 0):
                    break
                if (item[0] != 'SD'):
                    break

                index = int(item[1])
                angle = int(item[2])
                pos = int(item[3])
                blocks = int(item[4])
                print("TESTING ", item[0], item[0] == 'SD')
                if (item[0] == 'SD'):
                    if (angle == 270):
                        check = [1, 0]
                        fill(grid, i, j, check,
                             index, pos, blocks, angle)
                    elif (angle == 90):
                        check = [-1, 0]
                        fill(grid, i, j, check,
                             index, pos, blocks, angle)
                    elif (angle == 180):
                        check = [0, -1]
                        fill(grid, i, j, check,
                             index, pos, blocks, angle)
                    elif (angle == 0):
                        check = [0, 1]
                        fill(grid, i, j, check,
                             index, pos, blocks, angle)


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


def getEndItem(grid, start, blocks, width):
    """
        # get end link item
        grid - 3d array
        start - contains start coordinates
    """
    x = start[0]+blocks-1
    y = start[1]+width
    for k in range(len(grid[x][y])):
        item = grid[x][y][k].strip().split()
        if (len(item) == 0):
            continue
        print(item[0])
        if (item[0] == 'SD'):
            print("found the end")
            return item
    return 'no end'


def completeGrid(grid, width, isDecimal, dummy):
    """
        when the driveway size > 2 then the algo fills the drieway till it spans particular no of blocks
        grid - 3d array 
        width - width of driveway
        isDecimal - wheater the driveway width is odd in no(true is odd)
        dummy - futer contains the completed grid
    """
    tWidth = width
    # print("W idtj   ",width)
    Hfill = [0, 1]
    Vfill = [1, 0]
    if (isDecimal):
        tWidth += 1
    m = len(grid)
    n = len(grid[0])
    for i in range(0, m):
        for j in range(0, n):

            for k in range(0, len(grid[i][j])):
                x = i
                y = j
                s = grid[i][j][k]
                item = s.strip().split()
                angle = int(item[2])
                if (angle == 270 or angle == 90):
                    for l in range(0, tWidth):
                        # print("out of index  ",y,j)
                        if (y >= n):
                            break
                        dummy[x][y].append(s)
                        y += 1
                elif (angle == 180 or angle == 0):
                    for l in range(0, tWidth):
                        if (x >= m):
                            break
                        dummy[x][y].append(s)
                        x += 1


def preProcessParking(grid, filename, length):
    """
        preprocess the given input file , extract the data can create another file for desired inputs
        grid - 3d array
        filename - input filename
        length - length of the block
    """
    print("PREPROCESSING")
    filePark = open('desiredParking.txt', 'w')
    with open(filename, 'r') as file:
        lines = file.readlines()

        for i in range(len(lines)):

            line = lines[i].split('=')
            if (len(line[0]) == 0):
                continue
            s = line[0].strip()

            if (s[0] == 'x'):
                toadd = 'x'
                coordS = ''
                if (s[1] == '0'):
                    anglePark = 0
                    print("Angle park  ", anglePark)
                    coordS = s[3:]
                    print("coordS before split ", coordS)
                    coordS = coordS.split(',')
                    print("coordS after split ", coordS)

                    rowPark = int(coordS[0])+length
                    colPark = int(coordS[1][:-1])+length
                    print("parkoing index", rowPark, colPark)
                    # Case 1 - given intersection point
                    if (len(grid[rowPark][colPark-1]) != 0):
                        print("     0")
                        toadd += str(anglePark)
                        toadd += f" {rowPark} , {colPark}\n"
                    else:
                        print("     180")
                        toadd += str(180)
                        toadd += f" {rowPark} , {colPark+1}\n"

                else:
                    anglePark = int(s[1:3])
                    print("Angle park1,3  ", anglePark)
                    coordS = s[4:]
                    print("coordS before split ", coordS)
                    coordS = coordS.split(',')
                    print("coordS after split ", coordS)

                    rowPark = int(coordS[0])+length
                    colPark = int(coordS[1][:-1])+length
                    print("parkoing index", rowPark, colPark)

                    if (len(grid[rowPark-1][colPark]) != 0):
                        print("     270")
                        toadd += str(270)
                        toadd += f" {rowPark} , {colPark}\n"
                    else:
                        print("      90")
                        toadd += str(90)
                        toadd += f" {rowPark+1} , {colPark}\n"
                filePark.writelines(toadd)
