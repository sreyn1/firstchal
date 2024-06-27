import matplotlib.pyplot as plt

file_path = '/Users/sebastie.reynaud1/Documents/ALGO Assistant/challenge/pipeline/data/ehyd_messstellen_all_gw/messstellen_alle.csv'


def getxy(id):
    xlist = []
    ylist=[]
    with open(file_path, 'r', encoding='latin-1') as file:
        next(file)
        found=False
        for line in file:
            # Split the line into columns based on semicolons
            columns = line.strip().split(';')

            # Check if there are at least four columns and the fourth column matches x
            xlist.append(float(columns[0].replace(',','.')))
            ylist.append(float(columns[1].replace(',', '.')))
            if  int(columns[3]) == id:
                found_line = line.strip()
                found = True
                break
        if found:
            print(f"Found '{id}' in the line: {found_line}")
        else:
            print(f"'{id}' not found in any line.")
        return xlist, ylist


getxy(358051)
getxy(358051)
x,y=getxy(300012)

li=list(zip(x,y))
plt.scatter(*zip(*li))
plt.gca().set_aspect('equal')
plt.show()