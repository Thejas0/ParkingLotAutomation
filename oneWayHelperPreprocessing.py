
# FUNCTION WHICH CONSIDERS INPUT AND GIVES DESIRED OUTPUT FOR FURTHER PROCESS
import math
from oneWayMainPerpInputs import *
from oneWayHelperLaneConstruction import *

# funtion to generate desired input from given input


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
            # s += "\n"
            # if (flag == 1):
            #     file.writelines(s)

# encoding the grid


def encodeGrid(row, col, angle, grid, ct, connected):
    """
        function which consider input and fills the grid
        row ,col- positional paramters
        angle - angle of the object
        gridd - 3d arrau
        ct - to represent unique id of link

    """
    rowCopy = row
    link = 0
    row = -row
    temp = [False, False]
    temp1 = [False, False]
    s = "D "+f"{ct} "+f"{angle} "
    grid[rowCopy][col].append(s)
    connected[rowCopy][col].append(temp)
    # x1 decreases
    if (angle == 0):
        grid[rowCopy][col+1].append(s)
        connected[rowCopy][col+1].append(temp1)

    # y1 increases
    elif (angle == 90):
        # print("ROW Copy : ",row,rowCopy-1)
        if (rowCopy != 0):

            grid[rowCopy-1][col].append(s)
            connected[rowCopy-1][col].append(temp1)

    # y1 decreases
    elif (angle == 270):
        grid[rowCopy+1][col].append(s)
        connected[rowCopy+1][col].append(temp1)

    else:
        grid[rowCopy][col-1].append(s)
        connected[rowCopy][col-1].append(temp1)

        col += 1

    return link


filename = FILENAME
length = LENGTH
width = WIDTH


# to identy the start of the link
def identifyStartLinks(grid, gridReduced, count):
    """
     identify the start of the link
     grid - 3d grid
     gridReduced - refined grid (for reducing no of links)
    """
    # global count
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

# helper2 function for encoding the grid


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

# helper function for encoding the grid ,


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

# preprocessing the input for parking lots creation


def preProcessParking(grid, filename):
    """
        preprocess the given input file , extract the data can create another file for desired inputs
        grid - 3d array
        filename - input filename
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

                    rowPark = int(coordS[0])+length+1
                    colPark = int(coordS[1][:-1])+length

                    # Case 1 - given intersection point
                    if (len(grid[rowPark][colPark-1]) != 0):

                        toadd += str(anglePark)
                        toadd += f" {rowPark} , {colPark}\n"
                    else:
                        toadd += str(180)
                        toadd += f" {rowPark} , {colPark+1}\n"

                else:
                    anglePark = int(s[1:3])
                    print("Angle park1,3  ", anglePark)
                    coordS = s[4:]
                    print("coordS before split ", coordS)
                    coordS = coordS.split(',')
                    print("coordS after split ", coordS)

                    rowPark = int(coordS[0])+length+1
                    colPark = int(coordS[1][:-1])+length
                    if (len(grid[rowPark-1][colPark]) != 0):

                        toadd += str(270)
                        toadd += f" {rowPark} , {colPark}\n"
                    else:
                        toadd += str(90)
                        toadd += f" {rowPark+1} , {colPark}\n"
                filePark.writelines(toadd)


# def addBaseLink(row, col, angle, grid, ct, dist):
#     global Vissim
#     roadWidth = ROADWIDTH
#     rowCopy = row
#     row = -row
#     multiplier = 3.5
#     dist /= 3.5
#     s = "D "+f"{ct} "+f"{angle} "
#     grid[rowCopy][col].append(s)

#     # x1 decreases
#     if (angle == 0):
#         grid[rowCopy][col+1].append(s)

#         x0 = col*multiplier
#         y0 = row*multiplier - multiplier/2
#         x1 = (col+dist)*multiplier
#         y1 = y0
#         link = Vissim.Net.Links.AddLink(
#             0, f"LINESTRING({x0} {y0}, {x1} {y1})", [roadWidth])

#     # y1 increases
#     elif (angle == 90):
#         grid[rowCopy-1][col].append(s)

#         row -= 1
#         x0 = col*multiplier + multiplier/2
#         y0 = row*multiplier
#         x1 = x0
#         y1 = (row+dist)*multiplier

#         link = Vissim.Net.Links.AddLink(
#             0, f"LINESTRING({x0} {y0}, {x1} {y1})", [roadWidth])
#     # y1 decreases
#     elif (angle == 270):
#         grid[rowCopy+1][col].append(s)

#         x0 = col*multiplier + multiplier/2
#         y0 = row*multiplier
#         x1 = x0
#         y1 = (row-dist)*multiplier
#         link = Vissim.Net.Links.AddLink(
#             0, f"LINESTRING({x0} {y0}, {x1} {y1})", [roadWidth])
#     # angle 180 - x0 decreases
#     else:
#         grid[rowCopy][col-1].append(s)
#         col += 1
#         x0 = col*multiplier
#         y0 = row*multiplier - multiplier/2
#         x1 = (col-dist)*multiplier
#         y1 = y0
#         link = Vissim.Net.Links.AddLink(
#             0, f"LINESTRING({x0} {y0}, {x1} {y1})", [roadWidth])
#     return link
