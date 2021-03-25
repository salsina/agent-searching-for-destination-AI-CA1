from time import time
distinct_states = 1
found_states = 1
class State:
    def __init__(self, coordinates, remaining_balls_starts, remaining_balls_ends,balls_to_drop,depth,balls_in_backpack):
        self.coordinates = tuple(coordinates)
        self.remaining_balls_starts = tuple(remaining_balls_starts)
        self.remaining_balls_ends = remaining_balls_ends
        self.balls_to_drop = tuple(balls_to_drop)
        self.depth = depth
        self.balls_in_backpack = balls_in_backpack
        
class Node:
    def __init__(self,state,parent,action):
        self.state = state
        self.parent = parent
        self.action = action
        
class Map:
    def __init__(self,rows,cols,map,start_coordinates,end_coordinates,capacity,num_of_balls,balls_coordinates):
        self.rows = int(rows)
        self.cols = int(cols)
        self.map = self.set_map(map)
        self.start_coordinates = start_coordinates
        self.end_coordinates = end_coordinates
        self.capacity = int(capacity)
        self.num_of_balls = int(num_of_balls)
        self.balls_coordinates_start = []
        self.balls_coordinates_end = []
        self.set_ball_coordinates(balls_coordinates)
        self.init_state = State(start_coordinates, self.balls_coordinates_start, self.balls_coordinates_end,[],0,0)
        self.init_node = Node(self.init_state, None,'')
        self.end_state = State(self.end_coordinates, [], [],[],0,0)
        self.ans = []
        
    def set_map(self,map):
        m = []
        for row in map:
            splited = row.split()
            m.append(splited)
        return m
    
    def set_ball_coordinates(self,balls_coordinates):
        for i in range(len(balls_coordinates)):
            splited = [int(x) for x in balls_coordinates[i].split()]
            self.balls_coordinates_start.append( ( splited[0] , splited[1] ) )
            self.balls_coordinates_end.append( ( splited[2] , splited[3] ) )

    def position_is_valid(self,to_add,curr_x,curr_y):
        if to_add == [-1,0]:
            if (curr_x != 0) and (self.map[curr_x - 1][curr_y] != '*') : return True
            else: return False
    
        elif to_add == [1,0]:
            if (curr_x != (self.rows - 1)) and (self.map[curr_x + 1][curr_y] != '*'): return True
            else : return False
        
        elif to_add == [0,-1]:
            if (curr_y != 0) and (self.map[curr_x][curr_y - 1] != '*'): return True
            else : return False
            
        elif to_add == [0,1]:
            if (curr_y != (self.cols-1)) and (self.map[curr_x][curr_y + 1] != '*'): return True
            else: return False  
            
    def is_goal_state(self,state):
        return tuple(self.end_coordinates) == state.coordinates and\
            () == state.balls_to_drop and\
            () == state.remaining_balls_starts 

    def check_children(self,curr_x,curr_y,node,explored,frontier,to_add,action):
        global distinct_states 
        child_coordinates = [curr_x + to_add[0] , curr_y + to_add[1]]            
        child_state = State(child_coordinates,node.state.remaining_balls_starts,node.state.remaining_balls_ends,
                            node.state.balls_to_drop,node.state.depth + 1,node.state.balls_in_backpack)
        
        child_state_tuple = (child_state.coordinates,child_state.remaining_balls_starts,child_state.balls_to_drop)
        if child_state_tuple not in explored :
            distinct_states += 1
            if self.is_goal_state(child_state):
                self.ans.append(action)
                x = node
                while x != None:
                    self.ans.append(x.action)
                    x = x.parent
                return [node.state.depth + 1]
            child_node = Node(child_state,node,action)    
            frontier.append(child_node)
            explored[child_state_tuple] = True
        return [explored, frontier]
           
    def drop_the_ball(self,node,explored,frontier,curr_x,curr_y):
        tmp = list(node.state.balls_to_drop)
        index = tmp.index((curr_x, curr_y))

        tmp2 = list(node.state.balls_to_drop)
        new_drop = tmp2[:index] + tmp2[index+1:]

        child_state = State(node.state.coordinates, node.state.remaining_balls_starts[:] , node.state.remaining_balls_ends[:],
                            new_drop,node.state.depth,node.state.balls_in_backpack - 1)
        
        child_state_tuple = (child_state.coordinates,child_state.remaining_balls_starts,child_state.balls_to_drop)
        if child_state_tuple not in explored :
            if self.is_goal_state(child_state):
                x = node
                while x != None:
                    self.ans.append(x.action)
                    x = x.parent
                return [node.state.depth]
            child_node = Node(child_state,node.parent,node.action + ' & Drop')    
            frontier.append(child_node)
            explored[child_state_tuple] = True
            return [explored, frontier]

    def pick_the_ball(self,node,explored,frontier,curr_x, curr_y):
        global distinct_states
        tmp = list(node.state.remaining_balls_starts)
        index = tmp.index((curr_x, curr_y))

        ball_end = node.state.remaining_balls_ends[index]
        tmp2 = list(node.state.remaining_balls_starts)
        new_remainigs_start = tmp2[:index] + tmp2[index+1:]

        tmp3 = list(node.state.remaining_balls_ends)
        new_remainigs_end = tmp3[:index] + tmp3[index+1:]

        tmp4 = list(node.state.balls_to_drop)
        new_drop = tmp4 + [ball_end]

        child_state = State(node.state.coordinates, new_remainigs_start , new_remainigs_end,
                            new_drop, node.state.depth + 1,node.state.balls_in_backpack + 1)
        
        child_state_tuple = (child_state.coordinates,child_state.remaining_balls_starts,child_state.balls_to_drop)
        if child_state_tuple not in explored :
            distinct_states += 1
            child_node = Node(child_state,node.parent,node.action + ' & Pick')    
            frontier.append(child_node)
            explored[child_state_tuple] = True
            return [explored, frontier]
        return [False]
    
    def BFS(self):
        self.ans = []
        frontier = [self.init_node]
        explored = {(self.init_state.coordinates,self.init_state.remaining_balls_starts,self.init_state.balls_to_drop):True}
        DIRECTIONS = [[0,1,'Right'],[1,0,'Down'],[0,-1,'Left'],[-1,0,'Up'] ]
        global found_states ,distinct_states 
        while len(frontier) > 0:
            node = frontier.pop(0)
            curr_x = node.state.coordinates[0]
            curr_y = node.state.coordinates[1]
            
            if node.state.balls_in_backpack > 0 :
                if node.state.coordinates in node.state.balls_to_drop:
                    ans = self.drop_the_ball(node,explored,frontier,curr_x,curr_y)
                    if len(ans) == 2:
                        explored, frontier = ans[0], ans[1]
                        continue
                    else :
                        return ans[0]

            for to_add in DIRECTIONS:  
                if self.position_is_valid(to_add[:2],curr_x,curr_y):
                    found_states += 1
                    ans = self.check_children(curr_x,curr_y,node,explored,frontier,to_add[:2],to_add[2])
                    if len(ans) == 1:
                        return ans[0]
                    else:
                        explored, frontier = ans[0], ans[1]
                        
            if self.capacity > node.state.balls_in_backpack:            
                if node.state.coordinates in node.state.remaining_balls_starts:
                    found_states += 1
                    ans = self.pick_the_ball(node,explored,frontier,curr_x, curr_y)
                    if len(ans) == 2:
                        explored, frontier = ans[0], ans[1]

        return False
               

f = open("Tests/4.txt") 
file = f.readlines()
row_col= file[0].split()
start_coordinates = [int(x) for x in file[1].split()]
end_coordinates = [int(x) for x in file[2].split()]
num_of_balls = int(file[4])
balls_coordinates = file[5:5+num_of_balls]
map = file[5 + num_of_balls:]
m = Map(row_col[0],row_col[1],map,start_coordinates,end_coordinates,file[3],file[4],balls_coordinates)

t1 = time()
x = m.BFS()
t2 = time()
print('Distance: ',x)
print('All found states: ', found_states )
print('Distict states: ', distinct_states )
print('Time 1: ',t2 - t1)
path = "Init State"
print('Path: ',end = '')
for i in range(len(m.ans) - 1,-1,-1):
    path += m.ans[i] + ' -> '
print(path,end = 'Goal State\n')
t3 = time()
y = m.BFS()
t4 = time()
print('Time 2: ',t4 - t3)
t5 = time()
z = m.BFS()
t6 = time()
print('Time 3: ',t6 - t5)
print('Average time: ',((t2-t1)+(t4-t3)+(t6-t5))/3)