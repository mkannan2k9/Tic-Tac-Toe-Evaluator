import random
import copy

def PLAYER(s):
    x = 0
    y = 0
    for i in range(3):
        for j in range(3):
            if s[i][j] == "X":
                x += 1
            elif s[i][j] == "O":
                y += 1
    if x == y:
        return "X"
    else:
        return "O"

def ACTIONS(s):
    return [(i, j) for i in range(3) for j in range(3) if s[i][j] == "#"]

def RESULT(s, a):
    new_s = [row[:] for row in s]
    new_s[a[0]][a[1]] = PLAYER(s)
    return new_s

def TERMINAL(s):
    for i in range(3):
        if s[i][0] == s[i][1] == s[i][2] and s[i][0] != "#":
            return True
        if s[0][i] == s[1][i] == s[2][i] and s[0][i] != "#":
            return True
    if s[0][0] == s[1][1] == s[2][2] and s[0][0] != "#":
        return True
    if s[0][2] == s[1][1] == s[2][0] and s[0][2] != "#":
        return True
    for i in range(3):
        for j in range(3):
            if s[i][j] == "#":
                return False
    return True

def UTILITY(s):
    for i in range(3):
        if s[i][0] == s[i][1] == s[i][2] and s[i][0] != "#":
            return 1 if s[i][0] == "X" else -1
        if s[0][i] == s[1][i] == s[2][i] and s[0][i] != "#":
            return 1 if s[0][i] == "X" else -1
    if s[0][0] == s[1][1] == s[2][2] and s[0][0] != "#":
        return 1 if s[0][0] == "X" else -1
    if s[0][2] == s[1][1] == s[2][0] and s[0][2] != "#":
        return 1 if s[0][2] == "X" else -1
    return 0

def MAX_VALUE(s):
    if TERMINAL(s):
        return UTILITY(s), None, 0, 0
    v = float('-inf')
    best_action = None
    add = 0
    q = 0
    for action in ACTIONS(s):
        min_val, _, _, _ = MIN_VALUE(RESULT(s, action))
        add += min_val
        q += 1
        if min_val > v:
            v = min_val
            best_action = action
    assert best_action is not None
    return v, best_action, add, q

def MIN_VALUE(s):
    if TERMINAL(s):
        return UTILITY(s), None, 0, 0
    v = float('inf')
    best_action = None
    add = 0
    q = 0
    for action in ACTIONS(s):
        max_val, _, _, _ = MAX_VALUE(RESULT(s, action))
        add += max_val
        q += 1
        if max_val < v:
            v = max_val
            best_action = action
    assert best_action is not None
    return v, best_action, add, q

def PROBABILITY(s, n):
    x_win = 0
    o_win = 0
    draw = 0
    player = PLAYER(s)
    for _ in range(n):
        board = copy.deepcopy(s)
        turn = player
        while not TERMINAL(board):
            moves = ACTIONS(board)
            move = random.choice(moves)
            board = RESULT(board, move)
            turn = "O" if turn == "X" else "X"
        result = UTILITY(board)
        if result == 1:
            x_win += 1
        elif result == -1:
            o_win += 1
        else:
            draw += 1
    total = x_win + o_win + draw
    return x_win / total, o_win / total, draw / total

if __name__ == "__main__":
    s = [["#", "#", "#"], ["#", "#", "#"], ["#", "#", "#"]]
    while not TERMINAL(s):
        print("Current board:")
        for row in s:
            print(row)
        current_player = PLAYER(s)
        x, o, d = PROBABILITY(s, 10000)
        print("Prob of X win:", x)
        print("Prob of O win:", o)
        print("Prob of Draw:", d)
        print(f"Turn for player {current_player}")
        ixi = int(input("Row index: "))
        iyi = int(input("Col index: "))
        s = RESULT(s, (ixi, iyi))