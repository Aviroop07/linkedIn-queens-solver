import numpy as np
from PIL import Image
import copy
import streamlit as st

def find_no_of_rows(image : Image)->int:
    image_arr = np.array(image)
    height= image_arr.shape[0]
    no_of_rows = -1
    last_black = False
    for i in range(height):
        if image_arr[i][25][0]<=50 and image_arr[i][0][1]<=50 and image_arr[i][0][2]<=50:
            if not last_black:
                no_of_rows+=1
                last_black = True
        else :
            last_black = False
    return no_of_rows


def create_color_array(no_of_rows : int, image_arr : np.array)->list:
    color_arr = []
    height, width = image_arr.shape[:2]
    for row in range(height//(no_of_rows*2), height, height//no_of_rows):
        row_arr = []
        for col in range(width//(no_of_rows*2), width, width//no_of_rows):
            row_arr.append(image_arr[row][col])
        color_arr.append(row_arr)
    return color_arr


def abs_dist(arr1 : list, arr2 : list)->int:
    return np.sum(np.abs(arr1-arr2))


def create_color_board(color_arr : list,no_of_rows : int ,thres : int =0)->list:
    color_board = [[-1 for _ in range(no_of_rows)] for _ in range(no_of_rows)]
    identifier = 1
    color_board[0][0] = identifier
    remaining = no_of_rows**2-1
    queue = []
    queue.append((0,0))
    while remaining>0:
        if len(queue) == 0:
            done = False
            for i in range(no_of_rows):
                if done:
                    break
                for j in range(no_of_rows):
                    if color_board[i][j] == -1:
                        identifier+=1
                        color_board[i][j] = identifier
                        remaining-=1
                        queue.append((i,j))
                        # print(f'New color generated for ({i},{j})')
                        done = True
                        break
            continue
        # print(tabulate(color_board, tablefmt="fancy_grid"))
        i,j = queue.pop(0)
        if i>0 and color_board[i-1][j]==-1 and abs_dist(color_arr[i][j],color_arr[i-1][j])<=thres:
            queue.append((i-1,j))   
            color_board[i-1][j] = color_board[i][j]
            # print(f'({i-1},{j}) = ({i},{j})')
            remaining-=1
            
        if j>0 and color_board[i][j-1]==-1 and abs_dist(color_arr[i][j],color_arr[i][j-1])<=thres:
            queue.append((i,j-1))
            color_board[i][j-1] = color_board[i][j]
            # print(f'({i},{j-1}) = ({i},{j})')
            remaining-=1
            
        if i<no_of_rows-1 and color_board[i+1][j]==-1 and abs_dist(color_arr[i][j],color_arr[i+1][j])<=thres:
            queue.append((i+1,j))
            color_board[i+1][j] = color_board[i][j]
            # print(f'({i+1},{j}) = ({i},{j})')
            remaining-=1
            
        if j<no_of_rows-1 and color_board[i][j+1]==-1 and abs_dist(color_arr[i][j],color_arr[i][j+1])<=thres:
            queue.append((i,j+1))
            color_board[i][j+1] = color_board[i][j]
            # print(f'({i},{j+1}) = ({i},{j})')
            remaining-=1
    return color_board


def create_coordinates(color_board : list)->dict:
    coordinates = {}
    for i in range(len(color_board)):
        for j in range(len(color_board[i])):
            if color_board[i][j] not in coordinates:
                coordinates[color_board[i][j]] = [(i,j)]
            else:
                coordinates[color_board[i][j]].append((i,j))
    return coordinates


def sort_positions(positions : dict)->dict:
    return {i[0]:i[1] for i in sorted(positions.items(),key=lambda x:len(x[1]))}


def modify_pos(positions : dict, x : int, y:int)->dict:
    for i in positions.keys():
        for v in positions[i]:
            positions[i] = [v for v in positions[i] if not (v[0] == x or v[1] == y or (v[0]==x-1 and v[1]==y-1) or (v[0]==x-1 and v[1]==y+1) or (v[0]==x+1 and v[1]==y-1) or (v[0]==x+1 and v[1]==y+1))] 
    return sort_positions(positions)


def show_positions(positions : dict)->None:
    for i in positions.keys():
        print(f'{i}:{len(positions[i])}',end=',')
    print(' ')


def find_queen_pos(solution : list)->list:
    dim = len(solution)
    queen_pos = []
    for row in range(dim):
        for col in range(dim):
            if solution[row][col] == 'Q':
                queen_pos.append((row,col))
    return queen_pos


def create_red_dot(image_arr : np.array, pos : list, n_row : int)->np.array:
    jump = len(image_arr)//n_row
    offset = jump//2
    width = int(jump*0.15)
    for x,y in pos:
        for i in range(offset + jump*x-width,offset + jump*x+width):
            for j in range(offset + jump*y-width,offset + jump*y+width):
                image_arr[i][j] = [255,0,0]
    return image_arr


def check_color_board_validity(color_board : list, pos : dict)->bool:
    for i in range(len(color_board)):
        for j in range(len(color_board[i])):
            if color_board[i][j] == -1 or color_board[i][j]>len(color_board):
                return False
    return np.sum([len(i) for i in pos.values()]) == len(color_board)**2
        

class Node:
    def __init__(self, depth : int, board : list, coordinates: dict)->None:
        self.children = []
        self.depth = depth
        self.board = board
        self.backtrack = None
        # print(tabulate(board, tablefmt="fancy_grid"))
        # show_positions(coordinates)
        if len(coordinates) == 0:
            # print('Success!')
            self.backtrack = self.board
            return
        lowest_val = list(coordinates.keys())[0]
        # print(lowest_val)
        positions = coordinates[lowest_val]
        coordinates.pop(lowest_val)
        # display(coordinates)
        for x,y in positions:
            dup_coor = modify_pos(copy.deepcopy(coordinates),x,y)
            # if not check_pos_validity(dup_coor,x,y):
            #     print('Error!')
            #     return 
            # display(dup_coor)
            dup_board = copy.deepcopy(board)
            dup_board[x][y] = 'Q'
            # print(tabulate(dup_board, tablefmt="fancy_grid"))
            self.children.append(Node(self.depth+1, dup_board, dup_coor))
        
        for c in self.children:
            if c.backtrack is not None:
                self.backtrack = c.backtrack
                break
        
    def solution(self)->list:
        return self.backtrack


def queen_solver(image : Image, no_of_rows : int)->Image:
    try:
        # no_of_rows = find_no_of_rows(image)
        # print(f'no_of_rows = {no_of_rows}')
        if no_of_rows == 0 or no_of_rows==2 or no_of_rows>20:
            raise ValueError('Invalid Image!')
        color_arr = create_color_array(no_of_rows, np.array(image))
        # st.write(tabulate(color_arr, tablefmt="fancy_grid"))
        color_board = create_color_board(color_arr, no_of_rows)
        # print(tabulate(color_board, tablefmt="fancy_grid"))
        coordinates = sort_positions(create_coordinates(color_board))
        if not check_color_board_validity(color_board, coordinates):
            raise ValueError('Invalid Image!')
        # show_positions(coordinates)
        tree = Node(0, color_board, coordinates)
        # print(tabulate(tree.solution(), tablefmt="fancy_grid"))
        final_pos = find_queen_pos(tree.solution())
        # print(final_pos)
        image_arr = np.array(image)[:,:,:3]
        # print(image_arr)
        image_arr = create_red_dot(image_arr, final_pos, no_of_rows)
        return Image.fromarray(image_arr)
    except:
        raise ValueError('Invalid Image!')
    # final_image.show()