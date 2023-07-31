# COM-Server
import math
import win32com.client as com

from perpMainInputs import *
from perpHelperLaneConstruction import *
from perpHelperPreprocessing import *
from perpHelperVissim import *
from perpHelperPrinting import *

blockWidth = BLOCKWIDTH
blockLength = BLOCKLENGTH
parkWidth = blockWidth
parkLength = 3.0
parkingLength = blockLength


length = LENGTH
width = WIDTH
roadWidth = 1
pLength = 2
pWidth = 1
isDecimal = False
filename = FILENAME  # NAME OF THE IPUT FILE TO READ
# NO OF ROW AND COL ACCORDING TO INPUT CHANGE ACCORDINGLY
# NO OF ROW AND COL ACCORDING TO INPUT CHANGE ACCORDINGLY
rows, cols = (30+2*length, 30+2*length)

# read the input file and get the number of rows and cols
with open(filename, 'r') as file:
    lines = file.readlines()
    a = 0
    b = 0
    # print(lines)
    for i in range(len(lines)):
        line = lines[i].split('=')
        print(line)
        if (line[0].strip() == "Number of rows"):
            rows = int(line[1].strip())+max(2*length, 10)
            a = 1
        if (line[0].strip() == "Number of columns"):
            b = 1
            cols = int(line[1].strip())+max(2*length, 10)
        if (a+b == 2):
            break

# some space variable used overall in the algo (encoded grid)
flow = [[[0 for _ in range(2)] for _ in range(cols)] for _ in range(rows)]
grid = [[[] for i in range(cols)] for j in range(rows)]
gridReduced = [[[] for i in range(cols)] for j in range(rows)]
gridReducedCopy = [[[] for i in range(cols)] for j in range(rows)]

# printGrid(grid)
# print3Darray(flow)

start = [0, 0]
end = [0, 0]
# width = 1

# preprocess the input and fill flow array which will furter contain the direction of driveway
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
                    row, col+length, 270, grid, ct, length)
                ct += 1
                # endLink = encodeGrid(row+length-1, col+1+length,
                #                      90, grid, ct, length)
                endLink = encodeGrid(row+length-1, col+length+width,
                                     90, grid, ct, length)
                ct += 1
                flow[row+length][col+length][0] = 20
                # exit
                flow[row+length+(length-1)][col+width+length][0] = -20
            elif (col == 0):
                startLink = encodeGrid(
                    row+length, col, 0, grid, ct, length)
                ct += 1
                endLink = encodeGrid(row+width, col+length-1,
                                     180, grid, ct, length)
                ct += 1
                flow[row+length][col+2*length][1] = -20
                # exit
                flow[row+width][col+2*length-1][1] = 20

        if (line[0].strip() == "Parking field width"):
            pWidth = int(line[1])
            print("PARKING  ", pWidth, parkWidth)
            parkWidth *= pWidth

        if (line[0].strip() == "Parking field length"):
            pLength = int(line[1])
            parkingLength = blockLength*(pLength-.2)
        if (line[0].strip() == "Driving field width"):
            if (int(line[1]) % 2 == 1):
                isDecimal = True
            width = int(line[1])//2
            roadWidth = (int(line[1])/2) * blockWidth

        if (line[0].strip() == "Driving field length"):
            length = int(line[1])

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
                    flow[x0+(length-1)][y0+width][0] -= val
            elif (x1 > x0):  # 90
                flow[x0+length-1][y0+width][0] -= val
                if (x0-(length-1) >= 0):
                    flow[x0][y0][0] += val
            elif (y1 < y0):  # 180
                flow[x0][y0+length-1][1] += val
                if (y0 - (length-1) >= 0):
                    flow[x0+width][y0][1] -= val
            # here i have changes x0 to x1 and y0 to y1
            else:  # 0 -- Note in this we are adding width to flow
                flow[x0+width][y0][1] -= val  # adding width
                if (y1 + (length-1) < len(flow[0])):
                    flow[x0][y0+(length-1)][1] += val

print3Darray(flow)

file = open('desiredOutput.txt', 'w')
genenateDesiredOutput(flow, file)


fileName = 'desiredOutput.txt'

# read the preprocessed input and process the data
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
            encodeGrid(row, col, angle, grid, ct, length)
            ct += 1
            # print()
print("----------------------------")
printListGrid(grid)
printListGrid(grid)
# --------------------TO PRINT CONNECTED GRID------------------

# print("ROAD WIDTH ", roadWidth)
count = 1
count = identifyStartLinks(grid, gridReduced, count)
addReducedLinksinit(gridReduced, roadWidth, isDecimal)

fillGrid(gridReduced)
printListGridReduced(gridReduced)

start[1] += length

addConnectorsInitReduced(gridReduced)
connectUTurnInit(gridReduced, width, roadWidth, isDecimal, count,start)

print("---------------------------")
printListGridReduced(gridReduced)

# identify the start and end link items
# --------------------------------------
print("start block ", start)
startItem = getStartItem(gridReduced, start)
startLinkId = int(startItem[1])
startBlocks = int(startItem[4])
endItem = getEndItem(gridReduced, start, startBlocks, width)
endLinkId = int(endItem[1])
endLinkLen = Vissim.Net.Links.ItemByKey(endLinkId).AttValue('Length2D')
# --------------------------------------

# Base link creation
# --------------------------------------

baseLink = ""
print("Start , end = ", startItem, endItem)
if (start[0] == 0):
    baseindex = [-1, -5]
    baseLink = addBaseLink(
        baseindex[0], baseindex[1], 0, grid, ct, 100, roadWidth)
    offset = width
    diff = start[1]-baseindex[1]
    # add connectors , col to postion mapping
    # the offset acts as padding and 2* offset cuz width is halfed here
    Vissim.Net.Links.AddConnector(0, baseLink.Lanes.ItemByKey(
        1), (diff+2*offset)*blockLength, Vissim.Net.Links.ItemByKey(startLinkId).Lanes.ItemByKey(1), 0, 1, "LINESTRING EMPTY")
    Vissim.Net.Links.AddConnector(0, Vissim.Net.Links.ItemByKey(endLinkId).Lanes.ItemByKey(1), endLinkLen, baseLink.Lanes.ItemByKey(
        1), (diff+2*(width+offset+1))*blockLength, 1, "LINESTRING EMPTY")
# --------------------------------------


completeGrid(gridReduced, width, isDecimal, gridReducedCopy)
print("grid after filling ")
printListGridReduced(gridReducedCopy)

# ------------------------------
# Parking Start
# -------------------------------
# ----------------
preProcessParking(gridReducedCopy, filename, length)
print("COMPLETED PREPROCESSING")

# -------------------------
parkingLotinit(gridReducedCopy, parkWidth, pWidth,
               pLength, roadWidth, baseLink, parkingLength)
# -------------------------

#           Routing decisions
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
# To change the vehicle input change this paramter
# To change the vehicle input change this paramter
Veh1.SetAttValue("Volume(1)", 200)
# -------------------------

# adding node to network
Vissim.Net.Nodes.AddNode(
    0, f'POLYGON(({gridToCoord(0,0,roadWidth)}, {gridToCoord(0,cols,roadWidth)}, {gridToCoord(rows,cols,roadWidth)}, {gridToCoord(rows,0,roadWidth)}, {gridToCoord(0,0,roadWidth)}))')


# unsigned int Key, BSTR WktPolygon
# Vissim.Net.Nodes.AddNode(
#     0, 'POLYGON((-30 -30, 30 -30, 30 30, -30 30, -30 -30))')
# ---------------------------
print("DONE")
# ---------------------------
