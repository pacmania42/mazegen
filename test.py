from src.mazegen import  MazeGenerator as Gen

p = [
 (0, 0),
 (0, 1),
 (0, 2),
 (1, 2),
 (2, 2),
 (2, 3),
 (2, 4),
 (4, 0),
 (5, 0),
 (6, 0),
 (6, 1),
 (6, 2),
 (5, 2),
 (4, 2),
 (4, 3),
 (4, 4),
 (5, 4),
 (6, 4),
]



 
g = Gen(pattern=p, perfect=False)
g.export("maze.txt")

