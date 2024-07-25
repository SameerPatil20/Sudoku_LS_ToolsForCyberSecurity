from pwn import *

def update_board(output):
    values=[output[-13],output[-12],output[-11],output[-9],output[-8],output[-7],output[-5],output[-4],output[-3]]
    cleaned_rows = [row.replace('|', '').strip() for row in values]
    board = []
    for row in cleaned_rows:
        board_row = [int(num) if num != '.' else 0 for num in row.split()]
        board.append(board_row)
    return board

def possible(y,x,n,grid):
    for i in range(0,9):
        if grid[y][i]==n:
            return False
    for i in range(0,9):
        if grid[i][x]==n:
            return False
    x0=(x//3)*3
    y0=(y//3)*3
    for i in range(0,3):
        for j in range(0,3):
            if grid[y0+i][x0+j]==n:
                return False
    return True


def solve(grid):
    for y in range(9):
        for x in range(9):
            if grid[y][x]==0:
                check=0
                for n in range(1,10):
                    if possible(y,x,n,grid):
                        grid[y][x]=n
                        done=solve(grid)
                        if done[0]==True:
                            return done
                        grid[y][x]=0
                if check==0:
                    return [False,grid]
    return [True,grid]
    

io = process(["./sudoku","-q"],stdin=PTY)
game=0
output = io.recvuntil("(space-separated):".encode())
output=output.decode()
output=output.split("\n")
while game<420:
    sudoku_board=update_board(output)
    result=solve(sudoku_board)
    original=update_board(output)
    answer=[]
    for y in range(9):
        for x in range(9):
            if original[y][x]==0:
                out=""
                out+=str(y)
                out+=" "
                out+=str(x)
                out+=" "
                out+=str(result[1][y][x])
                answer.append(out)
    if game!=419:
        for out in answer:
            io.sendline(out.encode())
            output = io.recvuntil("(space-separated):".encode())
            output=output.decode()
            output=output.split("\n")
    else :
        t=len(answer)
        for i in range(t-1):
            io.sendline(answer[i].encode())
            output = io.recvuntil("(space-separated):".encode())
            output=output.decode()
            output=output.split("\n")
        io.sendline(answer[t-1].encode())
        output = io.recvall()
        print(output.decode())
    print("To ezzy game for me",game)
    game+=1