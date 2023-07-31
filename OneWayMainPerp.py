# required imports
import math
import win32com.client as com  # Connecting the COM Server
from oneWayMainPerpInputs import *
from oneWayHelperLaneConstruction import *
from oneWayHelperPreprocessing import *
from oneWayHelperPrinting import *
from oneWayHelperVissim import *

# PARAMETERS
roadWidth = ROADWIDTH
parkingLength = PARKINGLENGTH
length = LENGTH
width = WIDTH
filename = FILENAME  # NAME OF THE IPUT FILE TO READ
rows, cols = (30+2*length, 30+2*length)
ct = 1  # this variable is used to keep track of unique ids

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


start = [0, 0]
end = [0, 0]

# encode the flow grid for further processing
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
                print("Row : ", row)
                startLink = encodeGrid(
                    row, col+length, 270, grid, ct, connected)
                ct += 1
                print("END")
                endLink = encodeGrid(row+length-1, col+1+length,
                                     90, grid, ct, connected)
                ct += 1
                print("Row : ", row)
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
                # if (x0+(length-1) < len(flow)):
                #     flow[x0+(length-1)][y0+1][0] -= val
            elif (x1 > x0):  # 90
                flow[x0+length+1][y0][0] -= val
                # if (x0-(length-1) >= 0):
                #     flow[x0][y0][0] += val
            elif (y1 < y0):  # 180
                flow[x0+1][y0-1][1] -= val
                # if (y0 - (length-1) >= 0):
                #     flow[x0+1][y0][1] -= val
            else:  # 0 -- Note in this we are adding width to flow
                flow[x0+1][y0+1][1] += val  # adding width
                # if (y0 + (length-1) < len(flow[0])):
                #     flow[x0][y0+(length-1)][1] += val


# decoding
print3Darray(flow)
print("-----------before generating desired output-----------------")
printListGrid(grid)
print("-----------------------------")

# to extract desired input from given input
file = open('desiredOutput.txt', 'w')
genenateDesiredOutput(flow, file)

# decoding
print("-----------after desired output-----------------")
printListGrid(grid)
print("-----------------------------")
fileName = 'desiredOutput.txt'


# read the desired input file
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

    # decoding
    print("----------------------------")
    printListGrid(grid)
    print("-------------------")
    printListGrid(grid)
    print("-------------------")

# indetfy the start of the link
count = 1
count = identifyStartLinks(grid, gridReduced, count)

# add the driveway links in com
addReducedLinksinit(gridReduced)

# preprocess th grid(input)
fillGrid(gridReduced)
printListGridReduced(gridReduced)

start[1] += length
# add connectors
addConnectorsInitReduced(gridReduced)
connectUTurnInit(gridReduced, count,start)

# get the start and the end link items
print("start block ", start)
startItem = getStartItem(gridReduced, start)
startLinkId = int(startItem[1])
startBlocks = int(startItem[4])
endItem = getEndItem(gridReduced, start, startBlocks)
endLinkId = int(endItem[1])
endLinkLen = Vissim.Net.Links.ItemByKey(endLinkId).AttValue('Length2D')

baseLink = ""
print("Start , end = ", startItem, endItem)

# add baseLink (EntryLink  to the network)
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

# ----------------
#      PARKING
# ----------------

# preprocess the input to get the desired input  for parking lots
preProcessParking(grid, filename)
print("COMPLETED PREPROCESSING")

# -------------------------
# start creating parking loots
parkingLotinit(gridReduced, baseLink)

# -------------------------


# routing decisions
# --------------------------------------------------
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
# --------------------------------------------------


# adding Node
Vissim.Net.Nodes.AddNode(
    0, f'POLYGON(({gridToCoord(0,0)}, {gridToCoord(0,cols)}, {gridToCoord(rows,cols)}, {gridToCoord(rows,0)}, {gridToCoord(0,0)}))')


# unsigned int Key, BSTR WktPolygon
# Vissim.Net.Nodes.AddNode(
#     0, 'POLYGON((-30 -30, 30 -30, 30 30, -30 30, -30 -30))')
# ---------------------------
print("DONE")
# ---------------------------
