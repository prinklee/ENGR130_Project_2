import numpy as np 
import sys


#path output should be a list of the coordinates  
class node:
    def __init__(self, x, y, dist=-1, ancestor=None):
        self.x = x
        self.y = y 
        self.dist = dist
        self.anc = ancestor

    def __str__(self):
        return f'The distance from start is {self.dist} and the ancestor is {self.anc}.'

def get_neighbors(n,map,checked_vertices):
    neighbors = [(n.x-1,n.y), (n.x+1,n.y), (n.x,n.y-1), (n.x,n.y+1)]

    if n.x-1==-1 or map[n.x-1][n.y]== '*':
        neighbors.remove((n.x-1,n.y))
    if n.x+1==len(map) or map[n.x+1][n.y] == '*':
        neighbors.remove((n.x+1,n.y))
    if n.y-1==-1 or map[n.x][n.y-1] == '*':
        neighbors.remove((n.x,n.y-1))
    if n.y+1==len(map[0]) or map[n.x][n.y+1] == '*':
        neighbors.remove((n.x,n.y+1))

    for item in neighbors.copy():
        if item in checked_vertices:
            neighbors.remove(item)
    return neighbors

def find_path(map, all_vertices, s,e):
    checked_vertices = set() 
    current_vertices = {s}

    while len(checked_vertices.copy()) != len(all_vertices.keys()):
        for vertex in current_vertices.copy():
            i, j = vertex[0], vertex[1]
            neighbors = get_neighbors(all_vertices[(i,j)],map,checked_vertices)
            current_vertices.update(neighbors)

            for neighbor in neighbors.copy():
                a, b = neighbor[0], neighbor[1]
                if map[a][b] == '-':
                    map[a][b] = int(map[i][j])+1
                    all_vertices.update({(a,b): node(a,b,map[a][b], (i,j))})
                elif int(map[a][b]) > int(map[i][j]) + 1:
                    map[a][b] = int(map[i][j]) + 1
                    all_vertices.update({(a,b): node(a,b,map[a][b], (i,j))})
            current_vertices.remove(vertex)
            checked_vertices.add(vertex)
        

    path = list()

    path.append(e)

    while(all_vertices[path[-1]].anc != None):
        path.append(all_vertices[path[-1]].anc)

    path.reverse()

    return path

def load_map(filename):
    map = np.genfromtxt(filename,delimiter=" ", dtype='str')
    
    all_vertices = dict()

    for x in range(len(map)):
        for i in range(len(map[0])):
            if map[x][i] == '0':
                map[x][i] = '-'
                all_vertices.update({(x,i): node(x,i)})
            if map[x][i] == 'S':
                map[x][i] = '0'
                start = (x,i)
                all_vertices.update({(x,i): node(x,i,0)})
            if map[x][i] == '1':
                map[x][i] = '*'
            if map[x][i] == 'X':
                end = (x,i)
                map[x][i] = '-'
                all_vertices.update({(x,i): node(x,i,-1)})
    return map, all_vertices, start, end


def main():
    map, all_vertices, start, end = load_map(sys.argv[1])
    print(f'The quickest path is {find_path(map,all_vertices, start,end)}.')

if __name__ == '__main__':
    main()