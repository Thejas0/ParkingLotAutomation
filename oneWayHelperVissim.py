import math
import win32com.client as com
# from OneWayMainPerp import *
from oneWayMainPerpInputs import *
from oneWayHelperLaneConstruction import *

roadWidth = ROADWIDTH
parkingLength = PARKINGLENGTH


def addBaseLink(row, col, angle, grid, ct, dist):
    """
        # function to add the entry link - base link (only on upper side plot )
        row,col - positional parameters
        angle - provides the angle of driveway 
        grid - 3 d array
        ct - represent for unique identifier for links
        dist - length of the baselink 
    """
    # print(Vissim)
    # global Vissim
    roadWidth = ROADWIDTH
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

# function to add parking links


def addLinkPark(row, col, angle, grid, ct, connected):
    """
        function to add the parking lot links
        row,col - positional parameter
        angle - angle of driveway
        ct - represent for unique identifier for links

    """
    rowCopy = row
    # row+=1
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

# function to add driveway links


def addReducedLinks(row, col, angle, noOfblocks):
    """
        function to add links in vissim
        row,col - postional parameters
        no of Blocks - the no of blocks the link will psan
        roadWidth - width of road
        isDeciaml - wheter the driveway width is odd or even

    """
    blockLength = 3.5
    row = -row
    multiplier = roadWidth

    # x1 decreases
    if (angle == 0):

        x0 = col*multiplier
        y0 = row*multiplier - multiplier/2
        x1 = (col + noOfblocks)*multiplier
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

# init function for adding driveway links


def addReducedLinksinit(grid):
    """
        an init function which helps in creation of links
        grid - 3d array
        roadWidth - width of the road
        isdecimal - weather the driveway spans off no of blocks
    """
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


# function which interacts with vissim and connects link

# function to connect 2 driveway lanes
def connectVissimReduced(grid, x0, y0, z0, x1, y1, z1):
    """
        to add connector between 2 lanes
        grid - 3d array
        x0,y0,z0 - positional parameters of 1st item
        x1,y1,z1 - positional parameters of 2nd item 
    """
    multiplier = roadWidth
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

# init function which helps inn connection of driveway


def connectReduced(grid, x, y, z, check, connectionFlow):
    """
        2nd init function which helpers in connecting 2 lanes
        grid - 3d array 
        x,y,z - positional paramters
        check - list to check particular directions for connection of links
        connectionFlow - ist which represent the angle of link to connect with  
    """
    item1 = grid[x][y][z]
    item1 = item1.strip().split()
    angle1 = int(item1[2])
    if (len(item1) < 3):
        return

    for i in range(0, len(check)):

        temp = check[i]
        x1 = x+temp[0]
        y1 = y+temp[1]
        if (x1 < 0 or y1 < 0 or x1 >= len(grid) or y1 >= len(grid[0])):
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

# the outer function which wraps all inner functions used for connecting driveways


def addConnectorsInitReduced(grid):
    """
        Init function which start the process of connection of links
        grid - 3d array
    """
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
                    check = [[0, -1], [0, 1]]
                    connectReduced(grid, i, j, k, check, connectionFlow)
                    # angle 90
                elif (angle1 == 90):
                    connectionFlow = [0, 180]
                    # check = [[-1, width], [-2*width, -2*width]]
                    check = [[0, 1], [0, -1]]
                    connectReduced(grid, i, j, k, check, connectionFlow)
                # angle 180
                elif (angle1 == 180):
                    connectionFlow = [90, 270]
                    # check = [[-width, -1], [2*width, -2*width]]
                    check = [[-1, 0], [1, 0]]
                    connectReduced(grid, i, j, k, check, connectionFlow)
                # angle 0
                elif (angle1 == 0):
                    connectionFlow = [270, 90]
                    # check = [[width, 1], [-2*width, 2*width]]
                    check = [[1, 0], [-1, 0]]
                    connectReduced(grid, i, j, k, check, connectionFlow)

# function which interacts with vissim and connect the U turn areas


def connectUTurn(grid, check, angle1, reqAngle, item1, x, y, z, count):
    """
        function which helps in connecting the U -Turn areas
        gridR - 3d array 
        check - list to check for certain position for U - Turn areas
        angle1 -angle of driveway
        reqAngle - angle of Uturn link
        x,y,z - positional paramters

    """
    # global count
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
            return 1
    return 0
# an init function which initiates connetion of U turn areas


def connectUTurnInit(grid, count,start):
    """
        an Init function which coordinates the creation and connection of U-turn areas

        gridR - 3d array
        width - no of block the road spans
        roadWidth -  width of road
        isDecimal - boolean value which states wheter the driveway spans odd or even no of blocks


    """
    m = len(grid)
    n = len(grid[0])
    for i in range(0, m):
        for j in range(0, n):
            for k in range(len(grid[i][j])):
                item = grid[i][j][k].strip().split()
                if (len(item) == 0 or(i==start[0] and j==start[1])):
                    break
                m = item[0]
                if (m == 'SD'):
                    angle1 = int(item[2])
                    if (angle1 == 270):
                        reqAngle = 90
                        check = [0, 1]
                        count += connectUTurn(grid, check, angle1,
                                              reqAngle, item, i, j, k, count)
                    elif (angle1 == 90):
                        reqAngle = 270
                        check = [0, -1]
                        count += connectUTurn(grid, check, angle1,
                                              reqAngle, item, i, j, k, count)
                    elif (angle1 == 180):
                        reqAngle = 0
                        check = [1, 0]
                        count += connectUTurn(grid, check, angle1,
                                              reqAngle, item, i, j, k, count)
                    elif (angle1 == 0):
                        reqAngle = 180
                        check = [-1, 0]
                        count += connectUTurn(grid, check, angle1,
                                              reqAngle, item, i, j, k, count)

# function o create parking lot and its connections


def parkingLotinit(grid, baseLink):
    """
        Function which takes care of creation and connection of parking lot
        grid - 3d array
        baseLink - the baseLink(entry link for the network)
    """
    print(baseLink)
    VehRoutDesPark = Vissim.Net.VehicleRoutingDecisionsParking.AddVehicleRoutingDecisionParking(
        0, baseLink, 1)

    VehRoutDesPark.SetAttValue('ParkDur(1)', 20)
    VehRoutDesPark.SetAttValue('AllVehTypes', False)
    VehRoutDesPark.SetAttValue('VehClasses', 10)

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
                    baseLengthToPark = lengthPerBlock+.2

                    if (anglePark == 180):
                        connectRow = rowPark
                        connectCol = colPark+1
                        val = None
                        baseLengthToPark = 0
                        flag = 1
                        # prioity parking
                        for i in range(0, len(grid[connectRow][connectCol])):
                            val = grid[connectRow][connectCol][i]
                            val = val.strip().split()
                            linkid = int(val[1])
                            l = Vissim.Net.Links.ItemByKey(
                                linkid).AttValue("Length2D")
                            if (int(val[2]) == anglePark and l > 2*roadWidth):
                                flag = 0
                                break
                        for i in range(0, len(grid[connectRow][connectCol])):

                            if (flag != 0):
                                val = grid[connectRow][connectCol][i]
                                val = val.strip().split()

                            multiplier = roadWidth
                            sx0 = colPark*multiplier
                            sy0 = rowPark*multiplier - multiplier/2
                            sx1 = connectCol*multiplier
                            sy1 = connectRow*multiplier
                            connectId = int(val[1])
                            connectAngle = int(val[2])
                            pos = int(val[3])
                            baseLengthToPark = Vissim.Net.Links.ItemByKey(
                                connectId).AttValue("Length2D")-lengthPerBlock-0.1
                            if (flag == 0):
                                Vissim.Net.Links.AddConnector(0, Vissim.Net.Links.ItemByKey(connectId).Lanes.ItemByKey(
                                    1), min((pos-0.5)*lengthPerBlock, baseLengthToPark), linkPark.Lanes.ItemByKey(1), 0.3, 1, spLine(sx0, sy0, sx1, sy1)).RecalculateSpline()
                                break
                            elif (connectAngle != 0):
                                Vissim.Net.Links.AddConnector(0, Vissim.Net.Links.ItemByKey(connectId).Lanes.ItemByKey(
                                    1), (pos-0.5)*lengthPerBlock, linkPark.Lanes.ItemByKey(1), 0.3, 1, spLine(sx0, sy0, sx1, sy1)).RecalculateSpline()
                                break
                    elif (anglePark == 0):
                        connectRow = rowPark
                        connectCol = colPark-1
                        val = None
                        baseLengthToPark = 0
                        flag = 1
                        # prioity parking
                        for i in range(0, len(grid[connectRow][connectCol])):
                            val = grid[connectRow][connectCol][i]
                            val = val.strip().split()
                            linkid = int(val[1])
                            l = Vissim.Net.Links.ItemByKey(
                                linkid).AttValue("Length2D")
                            if (int(val[2]) == anglePark and l > 2*roadWidth):
                                flag = 0
                                break
                        for i in range(0, len(grid[connectRow][connectCol])):
                            if (flag != 0):
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
                            baseLengthToPark = Vissim.Net.Links.ItemByKey(
                                connectId).AttValue("Length2D")-lengthPerBlock-0.1
                            if (flag == 0):
                                Vissim.Net.Links.AddConnector(0, Vissim.Net.Links.ItemByKey(connectId).Lanes.ItemByKey(
                                    1), min((pos-0.5)*lengthPerBlock, baseLengthToPark), linkPark.Lanes.ItemByKey(1), 0.3, 1, spLine(sx0, sy0, sx1, sy1)).RecalculateSpline()
                                break
                            elif (connectAngle != 180):
                                Vissim.Net.Links.AddConnector(0, Vissim.Net.Links.ItemByKey(connectId).Lanes.ItemByKey(
                                    1), (pos-0.5)*lengthPerBlock, linkPark.Lanes.ItemByKey(1), 0.3, 1, spLine(sx0, sy0, sx1, sy1)).RecalculateSpline()
                                break
                    elif (anglePark == 90):
                        connectRow = rowPark+1
                        connectCol = colPark
                        val = None
                        baseLengthToPark = 0
                        flag = 1
                        # prioity parking
                        for i in range(0, len(grid[connectRow][connectCol])):
                            val = grid[connectRow][connectCol][i]
                            val = val.strip().split()
                            linkid = int(val[1])
                            l = Vissim.Net.Links.ItemByKey(
                                linkid).AttValue("Length2D")
                            if (int(val[2]) == anglePark and l > 2*roadWidth):
                                flag = 0
                                break
                        for i in range(0, len(grid[connectRow][connectCol])):
                            if (flag != 0):
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
                            baseLengthToPark = Vissim.Net.Links.ItemByKey(
                                connectId).AttValue("Length2D")-lengthPerBlock-0.1
                            if (flag == 0):
                                Vissim.Net.Links.AddConnector(0, Vissim.Net.Links.ItemByKey(connectId).Lanes.ItemByKey(
                                    1), min((pos-0.5)*lengthPerBlock, baseLengthToPark), linkPark.Lanes.ItemByKey(1), 0.3, 1, spLine(sx0, sy0, sx1, sy1)).RecalculateSpline()
                                break
                            elif (connectAngle != 270):
                                Vissim.Net.Links.AddConnector(0, Vissim.Net.Links.ItemByKey(connectId).Lanes.ItemByKey(
                                    1), (pos-0.5)*lengthPerBlock, linkPark.Lanes.ItemByKey(1), 0.3, 1, spLine(sx0, sy0, sx1, sy1)).RecalculateSpline()
                                break
                    elif (anglePark == 270):
                        connectRow = rowPark-1
                        connectCol = colPark
                        val = None
                        baseLengthToPark = 0
                        flag = 1
                        # prioity parking
                        for i in range(0, len(grid[connectRow][connectCol])):
                            val = grid[connectRow][connectCol][i]
                            val = val.strip().split()
                            linkid = int(val[1])
                            l = Vissim.Net.Links.ItemByKey(
                                linkid).AttValue("Length2D")
                            if (int(val[2]) == anglePark and l > 2*roadWidth):
                                flag = 0
                                break
                        for i in range(0, len(grid[connectRow][connectCol])):
                            if (flag != 0):
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
                            baseLengthToPark = Vissim.Net.Links.ItemByKey(
                                connectId).AttValue("Length2D")-lengthPerBlock-0.1
                            if (flag == 0):
                                Vissim.Net.Links.AddConnector(0, Vissim.Net.Links.ItemByKey(connectId).Lanes.ItemByKey(
                                    1), min((pos-0.5)*lengthPerBlock, baseLengthToPark), linkPark.Lanes.ItemByKey(1), 0.3, 1, spLine(sx0, sy0, sx1, sy1)).RecalculateSpline()
                                break
                            elif (connectAngle != 90):
                                Vissim.Net.Links.AddConnector(0, Vissim.Net.Links.ItemByKey(connectId).Lanes.ItemByKey(
                                    1), (pos-0.5)*lengthPerBlock, linkPark.Lanes.ItemByKey(1), 0.3, 1, spLine(sx0, sy0, sx1, sy1)).RecalculateSpline()
                                break
                connectParkingLane(grid)

                # AddParkingLot
                ParkingLot = Vissim.Net.ParkingLots.AddParkingLot(
                    0, linkPark.Lanes.ItemByKey(1), 0.5)

                ParkingLot.SetAttValue("ParkDir", 2)
                Vissim.Net.ParkingLots.ItemByKey(
                    countParkingLots).SetAttValue("Length", parkingLength)
                # routing decision
                VehRoutDesPark.VehRoutPark.AddVehicleRouteParking(
                    0, ParkingLot)
                countParkingLots += 1
