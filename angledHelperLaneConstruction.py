from angledMainInputs import *


def gridToCoord(row, col, roadWidth):
    '''
    # mapping for row,col to coordinates
    row -  no of rows 
    cols -  no of columns
    '''
    row = -row
    multiplier = (roadWidth)
    x0 = col*multiplier
    y0 = row*multiplier - multiplier/2
    s = f"{x0} {y0}"
    return s

# FUNCTION TO GENERATE POINTS FOR SPLINE CREATION


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
