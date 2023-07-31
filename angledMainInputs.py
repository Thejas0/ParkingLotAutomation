import win32com.client as com


# this function is used to create the environment , open vissim
def createEnv():
    global Vissim
    print("CREATE ENV")
    # Connecting the COM Server
    Vissim = com.dynamic.Dispatch("Vissim.Vissim")
    Vissim.New()
    print(Vissim)
    # directory of your PTV Vissim installation (where vissim.exe is located)
    PTVVissimInstallationPath = Vissim.AttValue("ExeFolder")

    # zoom to network
    Vissim.Graphics.CurrentNetworkWindow.ZoomTo(0, 0, 700, 150)
    return Vissim


Vissim = createEnv()

LENGTH = 1  # length of the driveway (no of blocks)
WIDTH = 1  # width of the driveway(no of blocks)
FILENAME = 'flow_angled_12_15.txt'  # NAME OF THE INPUT FILE TO READ

rows, cols = (30+2*LENGTH, 30+2*LENGTH)  # noo of rows and cols
BLOCKWIDTH = 3.0  # width of one block
BLOCKLENGTH = 3.0  # LENGTH of one block
PARKINGLENGTH = 5  # parking lot  length
START = [0, 0]  # entry cell
END = [0, 0]  # exit cell
ct = 1  # variable used to keep track of link id
start = [0, 0]  # entry cell
end = [0, 0]  # exit cell

# certain global variables
flow = [[[0 for _ in range(2)] for _ in range(cols)] for _ in range(rows)]
# flowCopy = [[[0 for _ in range(2)] for _ in range(cols)] for _ in range(rows)]
connected = [[[]
              for _ in range(cols)] for _ in range(rows)]
grid = [[[] for i in range(cols)] for j in range(rows)]
gridReduced = [[[] for i in range(cols)] for j in range(rows)]
count = 1
