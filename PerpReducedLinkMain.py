# COM-Server
import math
import win32com.client as com


# ----------------------------------------------------------------
# ----------------------------------------------------------------
# ----------------------------------------------------------------
# ------------------------TODO - START----------------------------------------
# ----------------------------------------------------------------
# ----------------------------------------------------------------
# ----------------------------------------------------------------
length = 2
filename = 'flow_29_15.txt'  # NAME OF THE IPUT FILE TO READ
# NO OF ROW AND COL ACCORDING TO INPUT CHANGE ACCORDINGLY
rows, cols = (30+2*length, 30+2*length)
flow = [[[0 for _ in range(2)] for _ in range(cols)] for _ in range(rows)]
flowCopy = [[[0 for _ in range(2)] for _ in range(cols)] for _ in range(rows)]
connected = [[[]
              for _ in range(cols)] for _ in range(rows)]

ct = 1

grid = [[[] for i in range(cols)] for j in range(rows)]
gridReduced = [[[] for i in range(cols)] for j in range(rows)]
gridConnectors = [[[] for i in range(cols)] for j in range(rows)]


# Connecting the COM Server
Vissim = com.dynamic.Dispatch("Vissim.Vissim")
Vissim.New()

# directory of your PTV Vissim installation (where vissim.exe is located)
PTVVissimInstallationPath = Vissim.AttValue("ExeFolder")

# zoom to network
Vissim.Graphics.CurrentNetworkWindow.ZoomTo(0, 0, 700, 150)

# GIVES MAPING FOR ROW,COL -> APPROPRIATE COORINATES X,Y
roadWidth = 3.0
parkingLength = 6


def gridToCoord(row, col):
    row = -row
    multiplier = 3.5
    x0 = col*multiplier
    y0 = row*multiplier - multiplier/2
    s = f"{x0} {y0}"
    return s

# FUNCTION TO GENERATE POINTS FOR SPLINE CREATION


def spLine(x0, y0, x1, y1):
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

# FUNCTION WHICH CONSIDERS INPUT AND GIVES DESIRED OUTPUT FOR FURTHER PROCESS


def genenateDesiredOutput(flow, file):
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

# here the road is assumed to be 2 blocks of length and width of 3.5 m

# A FUNCTION TO ADD BASE LINK - ENTRY LANE


def addBaseLink(row, col, angle, grid, ct, dist):
    rowCopy = row
    row = -row
    multiplier = 3.5
    dist /= 3.5
    s = "D "+f"{ct} "+f"{angle} "
    grid[rowCopy][col].append(s)

    # x1 decreases
    if (angle == 0):
        grid[rowCopy][col+1].append(s)

        x0 = col*multiplier
        y0 = row*multiplier - multiplier/2
        x1 = (col+dist)*multiplier
        y1 = y0
        link = Vissim.Net.Links.AddLink(
            0, f"LINESTRING({x0} {y0}, {x1} {y1})", [roadWidth])

    # y1 increases
    elif (angle == 90):
        grid[rowCopy-1][col].append(s)

        row -= 1
        x0 = col*multiplier + multiplier/2
        y0 = row*multiplier
        x1 = x0
        y1 = (row+dist)*multiplier

        link = Vissim.Net.Links.AddLink(
            0, f"LINESTRING({x0} {y0}, {x1} {y1})", [roadWidth])
    # y1 decreases
    elif (angle == 270):
        grid[rowCopy+1][col].append(s)

        x0 = col*multiplier + multiplier/2
        y0 = row*multiplier
        x1 = x0
        y1 = (row-dist)*multiplier
        link = Vissim.Net.Links.AddLink(
            0, f"LINESTRING({x0} {y0}, {x1} {y1})", [roadWidth])
    # angle 180 - x0 decreases
    else:
        grid[rowCopy][col-1].append(s)
        col += 1
        x0 = col*multiplier
        y0 = row*multiplier - multiplier/2
        x1 = (col-dist)*multiplier
        y1 = y0
        link = Vissim.Net.Links.AddLink(
            0, f"LINESTRING({x0} {y0}, {x1} {y1})", [roadWidth])
    return link
# here the road is assumed to be 2 blocks of length and width of 3.5 m


def addLinkPark(row, col, angle, grid, ct, connected):
    rowCopy = row
    row = -row
    multiplier = roadWidth
    temp = [False, False]
    temp1 = [False, False]
    s = "D "+f"{ct} "+f"{angle} "
    grid[rowCopy][col].append(s)
    connected[rowCopy][col].append(temp)
    # x1 decreases
    if (angle == 0):
        grid[rowCopy][col+1].append(s)
        connected[rowCopy][col+1].append(temp1)

        x0 = col*multiplier
        y0 = row*multiplier - multiplier/2
        x1 = (col+2)*multiplier
        y1 = y0
        link = Vissim.Net.Links.AddLink(
            0, f"LINESTRING({x0} {y0}, {x1} {y1})", [roadWidth])

    # y1 increases
    elif (angle == 90):
        grid[rowCopy-1][col].append(s)
        connected[rowCopy-1][col].append(temp1)

        row -= 1
        x0 = col*multiplier + multiplier/2
        y0 = row*multiplier
        x1 = x0
        y1 = (row+2)*multiplier

        link = Vissim.Net.Links.AddLink(
            0, f"LINESTRING({x0} {y0}, {x1} {y1})", [roadWidth])
    # y1 decreases
    elif (angle == 270):
        grid[rowCopy+1][col].append(s)
        connected[rowCopy+1][col].append(temp1)

        x0 = col*multiplier + multiplier/2
        y0 = row*multiplier
        x1 = x0
        y1 = (row-2)*multiplier
        link = Vissim.Net.Links.AddLink(
            0, f"LINESTRING({x0} {y0}, {x1} {y1})", [roadWidth])
    # angle 180 - x0 decreases
    else:
        grid[rowCopy][col-1].append(s)
        connected[rowCopy][col-1].append(temp1)

        col += 1
        x0 = col*multiplier
        y0 = row*multiplier - multiplier/2
        x1 = (col-2)*multiplier
        y1 = y0
        link = Vissim.Net.Links.AddLink(
            0, f"LINESTRING({x0} {y0}, {x1} {y1})", [roadWidth])
    return link
# function which encodes the postion of drivelane in 3d array for futrther process


def encodeGrid(row, col, angle, grid, ct, connected):
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

# TO PRINT GRID ARRAY


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


# printGrid(grid)
# print3Darray(flow)

start = [0, 0]
end = [0, 0]
width = 1

with open(filename, 'r') as file:
    lines = file.readlines()
    # print(lines)
    for i in range(len(lines)):
        line = lines[i].split('=')
        print(line)
        if (line[0].strip() == "Entry cell"):
            entryCord = line[1].strip()
            print(entryCord)
            entryCord = entryCord.split(',')
            print(entryCord)
            row = int(entryCord[0][1:])
            col = int(entryCord[1][:-1])
            print("row , col : ", row, col)
            start[0] = row
            start[1] = col
            end[0] = row
            end[1] = col+1
            if (row == 0):
                startLink = encodeGrid(
                    row, col+length, 270, grid, ct, connected)
                ct += 1
                endLink = encodeGrid(row+length-1, col+1+length,
                                     90, grid, ct, connected)
                ct += 1
                flow[row+length][col+length][0] = 20
                # exit
                flow[row+length+(length-1)][col+1+length][0] = -20
            elif (col == 0):
                startLink = encodeGrid(
                    row+length, col, 0, grid, ct, connected)
                ct += 1
                endLink = encodeGrid(row+width, col+length-1,
                                     180, grid, ct, connected)
                ct += 1
                flow[row+length][col+2*length][1] = -20
                # exit
                flow[row+width][col+2*length-1][1] = 20

        if (line[0].strip() == "Number of rows"):
            rows = int(line[1].strip())+length
        if (line[0].strip() == "Number of columns"):
            cols = int(line[1].strip())+length

        flowpara = line[0]
        if (line[0][0] == 'f'):
            s = flowpara[2:len(flowpara)-2]
            s = s.split(',')
            x0 = int(s[0])+length
            y0 = int(s[1])+length
            x1 = int(s[2])+length
            y1 = int(s[3])+length
            print(s)
            val = float(line[1][:-3])
            val = int(math.ceil(val))

            if (x1 < x0):  # 270
                flow[x0][y0][0] += val
                if (x0+(length-1) < len(flow)):
                    flow[x0+(length-1)][y0+1][0] -= val
            elif (x1 > x0):  # 90
                flow[x0+length-1][y0+1][0] -= val
                if (x0-(length-1) >= 0):
                    flow[x0][y0][0] += val
            elif (y1 < y0):  # 180
                flow[x0][y0+1][1] += val
                if (y0 - (length-1) >= 0):
                    flow[x0+1][y0][1] -= val
            else:  # 0 -- Note in this we are adding width to flow
                flow[x0+1][y0][1] -= val  # adding width
                if (y0 + (length-1) < len(flow[0])):
                    flow[x0][y0+(length-1)][1] += val

print3Darray(flow)

file = open('desiredOutput.txt', 'w')
genenateDesiredOutput(flow, file)


fileName = 'desiredOutput.txt'

with open(fileName, 'r') as file:
    lines = file.readlines()
    # print(lines)
    for i in range(len(lines)):
        list = lines[i].split()
        row = int(list[0])
        col = int(list[1])
        method = list[2]
        angle = int(list[3])

        if (method == 'Drive'):
            encodeGrid(row, col, angle, grid, ct, connected)
            ct += 1
            # print()
    print("----------------------------")
    printListGrid(grid)
    #
    # copyFlow(flow, flowCopy)

    # entry
    flow[start[0]][start[1]+length][0] = 20
    # exit
    flow[end[0]+(length-1)][end[1]+length][0] = -20
    printListGrid(grid)
    # --------------------TO PRINT CONNECTED GRID------------------

    def printConnected(connected):
        for i in range(0, len(connected)):
            for j in range(0, len(connected[i])):
                if (len(connected[i][j]) == 0):
                    print("          ", end=" ")
                print(connected[i][j], end=" ")
            print()
    printConnected(connected)

# helper function which helps in predicting number of start


def checkForStart(grid, i, j, angle1, row, col):
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


count = 1

# function which identifies the start of the link and mark it with SD encoding


def identifyStartLinks(grid, gridReduced):
    reducedLinkIndex = 1
    global count
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


identifyStartLinks(grid, gridReduced)

#  function which connects vissim and adds the link


def addReducedLinks(row, col, angle, noOfblocks):
    blockLength = 3.5

    row = -row
    multiplier = roadWidth

    # x1 decreases
    if (angle == 0):

        x0 = col*multiplier
        y0 = row*multiplier - multiplier/2
        x1 = (col+noOfblocks)*multiplier
        y1 = y0
        link = Vissim.Net.Links.AddLink(
            0, f"LINESTRING({x0} {y0}, {x1} {y1})", [roadWidth])

    # y1 increases
    elif (angle == 90):

        row -= 1
        x0 = col*multiplier + multiplier/2
        y0 = row*multiplier
        x1 = x0
        y1 = (row+noOfblocks)*multiplier

        link = Vissim.Net.Links.AddLink(
            0, f"LINESTRING({x0} {y0}, {x1} {y1})", [roadWidth])
    # y1 decreases
    elif (angle == 270):

        x0 = col*multiplier + multiplier/2
        y0 = row*multiplier
        x1 = x0
        y1 = (row-noOfblocks)*multiplier
        link = Vissim.Net.Links.AddLink(
            0, f"LINESTRING({x0} {y0}, {x1} {y1})", [roadWidth])
    # angle 180 - x0 decreases
    else:

        col += 1
        x0 = col*multiplier
        y0 = row*multiplier - multiplier/2
        x1 = (col-noOfblocks)*multiplier
        y1 = y0
        link = Vissim.Net.Links.AddLink(
            0, f"LINESTRING({x0} {y0}, {x1} {y1})", [roadWidth])
    return link

# init function which initiates the creating of link


def addReducedLinksinit(grid):
    m = len(grid)
    n = len(grid[0])
    for i in range(0, m):
        for j in range(0, n):
            for k in range(0, len(grid[i][j])):
                item = grid[i][j][k].strip().split()
                if (len(item) == 0):
                    break

                angle1 = int(item[2])
                noOfBlocks = int(item[4])
                addReducedLinks(i, j, angle1, noOfBlocks)


addReducedLinksinit(gridReduced)

# dfs function to fill thegrid to reduce the number of links


def fill(grid, row, col, check, index, pos, blocks, angle):
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
                        fill(gridReduced, i, j, check,
                             index, pos, blocks, angle)
                    elif (angle == 90):
                        check = [-1, 0]
                        fill(gridReduced, i, j, check,
                             index, pos, blocks, angle)
                    elif (angle == 180):
                        check = [0, -1]
                        fill(gridReduced, i, j, check,
                             index, pos, blocks, angle)
                    elif (angle == 0):
                        check = [0, 1]
                        fill(gridReduced, i, j, check,
                             index, pos, blocks, angle)


fillGrid(gridReduced)
printListGridReduced(gridReduced)

# -- Connectors --
'''
solution 2 
so insetad of using connected 2d array we can make use of SD encoding which
gives accurate result, SD will represent start of the link and using that knowledge
we can check the neighbors and if appropriate match then connect both
'''

# function which interacts with vissim and connects link


def connectVissimReduced(grid, x0, y0, z0, x1, y1, z1):
    multiplier = 3.5
    lengthPerBlock = roadWidth
    sx0 = y0*multiplier
    sy0 = x0*multiplier - multiplier/2
    sx1 = y1*multiplier
    sy1 = x1*multiplier
    point1 = grid[x0][y0][z0]
    point2 = grid[x1][y1][z1]
    point1 = point1.strip()
    point1 = point1.split()
    point2 = point2.strip()
    point2 = point2.split()

    if (len(point1) < 3 or len(point2) < 3):
        return 1
    if (int(point1[1]) == int(point2[1])):
        return 1

    # connect
    prevLinkId = int(point1[1])
    linkId = int(point2[1])
    pos1 = int(point1[3])
    pos2 = int(point2[3])

    Vissim.Net.Links.AddConnector(0, Vissim.Net.Links.ItemByKey(prevLinkId).Lanes.ItemByKey(
        1), pos1*lengthPerBlock, Vissim.Net.Links.ItemByKey(linkId).Lanes.ItemByKey(1), (pos2-1)*lengthPerBlock, 1, spLine(sx0, sy0, sx1, sy1)).RecalculateSpline()

# and sub init function for connecting connectors


def connectReduced(grid, x, y, z, check, connectionFlow):
    item1 = grid[x][y][z]
    item1 = item1.strip().split()
    angle1 = int(item1[2])
    if (len(item1) < 3):
        return

    for i in range(0, len(check)):

        temp = check[i]
        x1 = x+temp[0]
        y1 = y+temp[1]
        if (x1 < 0 or y1 < 0 or x1 >= len(flow) or y1 >= len(flow[0])):
            continue
        for j in range(0, len(grid[x1][y1])):
            item2 = grid[x1][y1][j]
            item2 = item2.strip().split()

            angle2 = int(item2[2])
            if (i == 0):
                if (angle2 == connectionFlow[i] or angle2 == angle1):
                    connectVissimReduced(grid, x, y, z, x1, y1, j)

            elif (i == 1):
                if (angle2 == connectionFlow[i] or angle2 == angle1):
                    connectVissimReduced(grid, x, y, z, x1, y1, j)

# an init function which initiates the connection of drivelanes


def addConnectorsInitReduced(grid):
    m = len(grid)
    n = len(grid[0])
    for i in range(0, m):
        for j in range(0, n):
            # -------turn
            # -------staight
            # 2lane gap
            # U - turn
            # angle 270
            if (len(grid[i][j]) == 0):
                continue
            for k in range(0, len(grid[i][j])):
                item1 = grid[i][j][k]

                item1 = item1.strip()
                item1 = item1.split()
                if (len(item1) < 3):
                    continue
                angle1 = int(item1[2])
                # print("angle1 , ",angle1)
                if (angle1 == 270):
                    connectionFlow = [180, 0]
                    # check = [[1, -width], [2*width, 2*width]]
                    check = [[1, -1], [1, 1]]

                    connectReduced(grid, i, j, k, check, connectionFlow)
                    # angle 90
                elif (angle1 == 90):
                    connectionFlow = [0, 180]
                    # check = [[-1, width], [-2*width, -2*width]]
                    check = [[-1, 1], [-1, -1]]
                    connectReduced(grid, i, j, k, check, connectionFlow)
                # angle 180
                elif (angle1 == 180):
                    connectionFlow = [90, 270]
                    # check = [[-width, -1], [2*width, -2*width]]
                    check = [[-1, -1], [1, -1]]
                    connectReduced(grid, i, j, k, check, connectionFlow)
                # angle 0
                elif (angle1 == 0):
                    connectionFlow = [270, 90]
                    # check = [[width, 1], [-2*width, 2*width]]
                    check = [[1, 1], [-1, 1]]
                    connectReduced(grid, i, j, k, check, connectionFlow)

# function which interacts with vissim and connect the U turn areas


def connectUTurn(grid, check, angle1, reqAngle, item1, x, y, z):
    global count
    dict = {270: 180, 90: 0, 180: 90, 0: 270}
    lengthPerBlock = roadWidth
    multiplier = roadWidth
    linkId = int(item1[1])
    x1 = x+check[0]
    y1 = y+check[1]
    sx0 = y*multiplier
    sy0 = x*multiplier - multiplier/2
    sx1 = y1*multiplier
    sy1 = x1*multiplier

    for k in range(len(grid[x1][y1])):
        item2 = grid[x1][y1][k].strip().split()
        prevLinkId = int(item2[1])
        pos1 = int(item2[3])
        if (len(item2) == 0):
            break
        angle2 = int(item2[2])
        if (angle2 == reqAngle):
            s = f"D {count} {reqAngle} {1}"
            grid[x1][y1].append(s)
            s = f"D {count} {reqAngle} {2}"
            grid[x][y].append(s)
            count += 1
            link = addReducedLinks(x1, y1, dict[angle1], 2)
            len1 = link.AttValue('Length2D')
            '''link -> item'''
            Vissim.Net.Links.AddConnector(0, Vissim.Net.Links.ItemByKey(prevLinkId).Lanes.ItemByKey(
                1), (pos1-0.91)*lengthPerBlock, link.Lanes.ItemByKey(1), 0, 1, spLine(sx0, sy0, sx1, sy1)).RecalculateSpline()
            Vissim.Net.Links.AddConnector(0, link.Lanes.ItemByKey(
                1), len1, Vissim.Net.Links.ItemByKey(linkId).Lanes.ItemByKey(1), 0*lengthPerBlock, 1, spLine(sx0, sy0, sx1, sy1)).RecalculateSpline()

# an init function which initiates connetion of U turn areas


def connectUTurnInit(grid):
    m = len(grid)
    n = len(grid[0])
    for i in range(0, m):
        for j in range(0, n):
            for k in range(len(grid[i][j])):
                item = grid[i][j][k].strip().split()
                if (len(item) == 0):
                    break
                m = item[0]
                if (m == 'SD'):
                    angle1 = int(item[2])
                    if (angle1 == 270):
                        reqAngle = 90
                        check = [0, 1]
                        connectUTurn(grid, check, angle1,
                                     reqAngle, item, i, j, k)
                    elif (angle1 == 90):
                        reqAngle = 270
                        check = [0, -1]
                        connectUTurn(grid, check, angle1,
                                     reqAngle, item, i, j, k)
                    elif (angle1 == 180):
                        reqAngle = 0
                        check = [1, 0]
                        connectUTurn(grid, check, angle1,
                                     reqAngle, item, i, j, k)
                    elif (angle1 == 0):
                        reqAngle = 180
                        check = [-1, 0]
                        connectUTurn(grid, check, angle1,
                                     reqAngle, item, i, j, k)


addConnectorsInitReduced(gridReduced)
connectUTurnInit(gridReduced)

# gives first link item


def getStartItem(grid, start):
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
    x = start[0]+blocks-1
    y = start[1]+1
    for k in range(len(grid[x][y])):
        item = grid[x][y][k].strip().split()
        if (len(item) == 0):
            continue
        print(item[0])
        if (item[0] == 'SD'):
            print("found the end")
            return item
    return 'no end'


start[1] += 2  # adding 2 because the grid is padded in all sides by length(2)
print("start block ", start)
startItem = getStartItem(gridReduced, start)
startLinkId = int(startItem[1])
startBlocks = int(startItem[4])
endItem = getEndItem(gridReduced, start, startBlocks)
endLinkId = int(endItem[1])
endLinkLen = Vissim.Net.Links.ItemByKey(endLinkId).AttValue('Length2D')

baseLink = ""
print("Start , end = ", startItem, endItem)
if (start[0] == 0):
    baseindex = [-1, -5]
    baseLink = addBaseLink(baseindex[0], baseindex[1], 0, grid, ct, 100)
    offset = 2
    diff = start[1]-baseindex[1]-2
    # add connectors , col to postion mapping
    Vissim.Net.Links.AddConnector(0, baseLink.Lanes.ItemByKey(
        1), (diff+offset)*roadWidth, Vissim.Net.Links.ItemByKey(startLinkId).Lanes.ItemByKey(1), 0, 1, "LINESTRING EMPTY")
    Vissim.Net.Links.AddConnector(0, Vissim.Net.Links.ItemByKey(endLinkId).Lanes.ItemByKey(1), endLinkLen, baseLink.Lanes.ItemByKey(
        1), (diff+2*offset)*roadWidth, 1, "LINESTRING EMPTY")
# addBaseLinkInit(gridReduced)

# ------------------------------
# Parking Start
# -------------------------------
VehRoutDesPark = Vissim.Net.VehicleRoutingDecisionsParking.AddVehicleRoutingDecisionParking(
    0, baseLink, 1)

VehRoutDesPark.SetAttValue('ParkDur(1)', 20)
VehRoutDesPark.SetAttValue('AllVehTypes', False)
VehRoutDesPark.SetAttValue('VehClasses', 10)


def preProcessParking():
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

                    rowPark = int(coordS[0])+length
                    colPark = int(coordS[1][:-1])+length
                    if (len(grid[rowPark-1][colPark]) != 0):

                        toadd += str(270)
                        toadd += f" {rowPark} , {colPark}\n"
                    else:
                        toadd += str(90)
                        toadd += f" {rowPark+1} , {colPark}\n"
                filePark.writelines(toadd)


def parkingLotinit(grid):
    with open('desiredParking.txt', 'r') as file:
        lines = file.readlines()
        countParkingLots = 1
        # print(lines)
        for i in range(len(lines)):
            # line = lines[i]
            s = lines[i].strip().split()
            print(s)
            if (s[0][0] == 'x'):
                anglePark = int(s[0][1:])

                rowPark = int(s[1])
                colPark = int(s[3])

                # Step 1 - addLink
                linkPark = addLinkPark(
                    rowPark, colPark, anglePark, grid, ct, connected)
                # Step2  - Connector
                #  spLine(sx0, sy0, sx1, sy1)
                '''
                multiplier = 3.5
                sx0 = y0*multiplier
                sy0 = x0*multiplier - multiplier/2
                sx1 = y1*multiplier
                sy1 = x1*multiplier
                '''
                def connectParkingLane(grid):
                    lengthPerBlock = roadWidth
                    if (anglePark == 180):
                        connectRow = rowPark
                        connectCol = colPark+1
                        for i in range(0, len(grid[connectRow][connectCol])):
                            val = grid[connectRow][connectCol][i]
                            val = val.strip().split()
                            multiplier = 3.5
                            sx0 = colPark*multiplier
                            sy0 = rowPark*multiplier - multiplier/2
                            sx1 = connectCol*multiplier
                            sy1 = connectRow*multiplier
                            connectId = int(val[1])
                            connectAngle = int(val[2])
                            pos = int(val[3])

                            if (connectAngle != 0):
                                Vissim.Net.Links.AddConnector(0, Vissim.Net.Links.ItemByKey(connectId).Lanes.ItemByKey(
                                    1), (pos-0.5)*lengthPerBlock, linkPark.Lanes.ItemByKey(1), 0, 1, spLine(sx0, sy0, sx1, sy1)).RecalculateSpline()
                                break
                    elif (anglePark == 0):
                        connectRow = rowPark
                        connectCol = colPark-1
                        for i in range(0, len(grid[connectRow][connectCol])):
                            val = grid[connectRow][connectCol][i]
                            val = val.strip().split()
                            connectId = int(val[1])
                            connectAngle = int(val[2])
                            multiplier = 3.5
                            sx0 = colPark*multiplier
                            sy0 = rowPark*multiplier - multiplier/2
                            sx1 = connectCol*multiplier
                            sy1 = connectRow*multiplier
                            pos = int(val[3])

                            if (connectAngle != 180):
                                Vissim.Net.Links.AddConnector(0, Vissim.Net.Links.ItemByKey(connectId).Lanes.ItemByKey(
                                    1), (pos-0.5)*lengthPerBlock, linkPark.Lanes.ItemByKey(1), 0, 1, spLine(sx0, sy0, sx1, sy1)).RecalculateSpline()
                                break
                    elif (anglePark == 90):
                        connectRow = rowPark+1
                        connectCol = colPark
                        for i in range(0, len(grid[connectRow][connectCol])):
                            val = grid[connectRow][connectCol][i]
                            val = val.strip().split()
                            connectId = int(val[1])
                            connectAngle = int(val[2])
                            multiplier = 3.5
                            sx0 = colPark*multiplier
                            sy0 = rowPark*multiplier - multiplier/2
                            sx1 = connectCol*multiplier
                            sy1 = connectRow*multiplier
                            pos = int(val[3])

                            if (connectAngle != 270):
                                Vissim.Net.Links.AddConnector(0, Vissim.Net.Links.ItemByKey(connectId).Lanes.ItemByKey(
                                    1), (pos-0.5)*lengthPerBlock, linkPark.Lanes.ItemByKey(1), 0, 1, spLine(sx0, sy0, sx1, sy1)).RecalculateSpline()
                                break
                    elif (anglePark == 270):
                        connectRow = rowPark-1
                        connectCol = colPark
                        for i in range(0, len(grid[connectRow][connectCol])):
                            val = grid[connectRow][connectCol][i]
                            val = val.strip().split()
                            connectId = int(val[1])
                            connectAngle = int(val[2])
                            multiplier = 3.5
                            sx0 = colPark*multiplier
                            sy0 = rowPark*multiplier - multiplier/2
                            sx1 = connectCol*multiplier
                            sy1 = connectRow*multiplier
                            pos = int(val[3])

                            if (connectAngle != 90):
                                Vissim.Net.Links.AddConnector(0, Vissim.Net.Links.ItemByKey(connectId).Lanes.ItemByKey(
                                    1), (pos-0.5)*lengthPerBlock, linkPark.Lanes.ItemByKey(1), 0, 1, spLine(sx0, sy0, sx1, sy1)).RecalculateSpline()
                                break
                connectParkingLane(grid)

                # AddParkingLot
                ParkingLot = Vissim.Net.ParkingLots.AddParkingLot(
                    0, linkPark.Lanes.ItemByKey(1), 0.1)

                ParkingLot.SetAttValue("ParkDir", 2)
                Vissim.Net.ParkingLots.ItemByKey(
                    countParkingLots).SetAttValue("Length", parkingLength-0.2)
                # routing decision
                VehRoutDesPark.VehRoutPark.AddVehicleRouteParking(
                    0, ParkingLot)
                countParkingLots += 1


# ----------------
preProcessParking()
print("COMPLETED PREPROCESSING")

# -------------------------
parkingLotinit(gridReduced)
# -------------------------


# AT Last add static routing decision
# unsigned int Key, ILink* Link, double Pos
VehRoutDesSta = Vissim.Net.VehicleRoutingDecisionsStatic.AddVehicleRoutingDecisionStatic(
    0, baseLink, 0.1)  # unsigned int Key, ILink* Link,, double Pos
VehRoutSta1 = VehRoutDesSta.VehRoutSta.AddVehicleRouteStatic(
    0, baseLink, baseLink.AttValue("Length2D"))
# Vehicle Input
Veh1 = Vissim.Net.VehicleInputs.AddVehicleInput(
    0, baseLink)
Veh1.SetAttValue("Volume(1)", 200)


Vissim.Net.Nodes.AddNode(
    0, f'POLYGON(({gridToCoord(0,0)}, {gridToCoord(0,cols)}, {gridToCoord(rows,cols)}, {gridToCoord(rows,0)}, {gridToCoord(0,0)}))')


# unsigned int Key, BSTR WktPolygon
# Vissim.Net.Nodes.AddNode(
#     0, 'POLYGON((-30 -30, 30 -30, 30 30, -30 30, -30 -30))')
# ---------------------------
print("DONE")
# ---------------------------
