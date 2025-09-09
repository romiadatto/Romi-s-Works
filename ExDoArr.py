import random

EMPTY = "o"
SUBMARINE = "x"


# 1
def print_mat(mat1):
    for i in range(len(mat1)):
        for j in range(len(mat1)):
            print(mat1[i][j],end="  ")
        print()


# 2
def sum_mat(mat1):
    sum = 0
    for row in mat1:
        for coll in row:
            sum += coll
    return sum


# 3
def sum_main_diagonal_mat(mat1):
    len_mat = len(mat1)
    sum = 0
    for i in range(len_mat):
        sum += mat1[i][i]
    return sum


# 4
def correct_kelet(board,row, coll):
    tries = 0
    while row < 0 or row > len(board) or coll < 0 or coll > len(board):  # checking Input integrity
        print("erroneous kelet")
        row = int(input("enter again the row you want-"))
        coll = int(input("enter again the coll you want-"))
        tries += 1
    tries += 1
    list = [tries, row, coll]
    return list


def there_submarine(board,row, coll):
    flag = False
    tries = 0
    while flag == False:
        temp_list = correct_kelet(row, coll)
        tries += temp_list[0]
        row = temp_list[1]
        coll = temp_list[2]
        if board[row - 1][coll - 1] == 'x':
            flag = True
            return tries
        else:
            print("there is no submarine, try again")
            row = int(input("enter the row you want-"))
            coll = int(input("enter the coll you want-"))


def tries_submarine_game(board):
    flag = False
    tries = 0
    print("to blow: ")
    row = int(input("enter the row you want-"))
    coll = int(input("enter the coll you want-"))
    tries = there_submarine(board,row, coll)
    board[row - 1][coll - 1] = "S"
    return tries


def succeed_submarine_game(board):
    in_vain = tries_submarine_game(board)
    print("until now you tried- ", in_vain, " times")
    print("you found the submarine! keep going...")
    num_submarine = 0
    for row in board:
        num_submarine += row.count("x")
    for i in range(num_submarine - 1):
        in_vain += tries_submarine_game(board)
        print("keep going...")
        row = int(input("enter the row you want-"))
        coll = int(input("enter the coll you want-"))
        in_vain += there_submarine(board,row, coll)
        board[row - 1][coll - 1] = "S"
    return board

# 5
def create_mat():
    mat = [[None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           ]
    list= [1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9]
    for i in range(4):
        for j in range(4):
            mat[i][j] = random.choice(list)
            list.remove(mat[i][j])
    return mat


def create_hide_mat():
    mat = [[None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           ]
    for i in range(4):
        for j in range(4):
            mat[i][j] = "⬜"
    return mat


def right_kelet(mat):
    row = int(input("enter the row you want- "))
    coll = int(input("enter the coll you want- "))
    while row < 0 or row > len(mat) or coll < 0 or coll > len(mat):
        print("erroneous kelet")
        row = int(input("enter the row you want- "))
        coll = int(input("enter the coll you want- "))
    list = [row, coll]
    return list


def show_number(mat1,mat2, row1, coll1):
    for i in range(len(mat1)):
        for j in range(len(mat1)):
            if (row1-1 == i and coll1-1 == j):
                mat2[i][j]=mat1[row1-1][coll1-1]
    print_mat(mat2)


def memory_game():
    mat1 = create_mat()
    mat2 = create_hide_mat()
    print_mat(mat2)
    for i in range(2):
        temp_list = right_kelet(mat1)
        row = temp_list[0]
        coll = temp_list[1]
        show_number(mat1,mat2, row, coll)
    mat=create_hide_mat()


def main():
    mat = [[1, 2, 3, 4, 5],
           [6, 7, 8, 9, 10],
           [11, 12, 13, 14, 15],
           [16, 17, 18, 19, 20],
           [21, 22, 23, 24, 25]
           ]
    print_mat(mat)
    print("the sum of the mat is- ", sum_mat(mat))
    print("the sum of the main diagonal is- ", sum_main_diagonal_mat(mat))

    board = [[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
             [SUBMARINE, EMPTY, EMPTY, EMPTY, EMPTY],
             [SUBMARINE, EMPTY, EMPTY, EMPTY, EMPTY],
             [SUBMARINE, EMPTY, EMPTY, EMPTY, EMPTY]
             ]
    board = succeed_submarine_game(board)
    print_mat(board)
    print("you succeeded!, congratulations!!!")
    memory_game()
main()
