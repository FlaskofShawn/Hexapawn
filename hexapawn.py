# hexapawn.py
# move generator : line 142 - 278
# board evaluator : line 283 - 348
# minimax search : line 21 -139


def hexapawn(cur_board, board_size, pawn_color, number_moves_ahead):
    """This is the interface function provided by homework prompt.

    Args:
        cur_board: The n-element list.
        board_size: The size of the board.
        pawn_color: The color indicates which turn to move the pawn.
        number_moves_ahead: The number indicates how many moves to look ahead.
    Returns:
        A list of strings represents the next best move. If no legal next move, it returns the first argument itself.
    """
    return minimax_algorithm(cur_board, board_size, pawn_color, number_moves_ahead)


def minimax_algorithm(cur_board, board_size, pawn_color, number_moves_ahead):
    """This function implements the minimax algorithm.

    Args:
        cur_board: The initial node(root).
        board_size: The size of the board.
        pawn_color: The color indicates whose turn to move the pawn.
        number_moves_ahead: The number indicates how many moves to look ahead.

    Returns: A list of string representing the next best move for the current player.

    """
    target_color = pawn_color
    next_turn_color = pawn_color
    best_next_move, best_static_board_val = max_value_propagation(cur_board, board_size, target_color,
                                                                  number_moves_ahead, next_turn_color)
    return best_next_move


def max_value_propagation(cur_board, board_size, target_color, number_moves_ahead, next_turn_color):
    """This function is used for max level player to propagate staci board value.

    Args:
        cur_board:  The current board that a list of strings.
        board_size: The size of the board.
        target_color: A character indicates who is the player given this situation(Max).
        number_moves_ahead: The number indicates how many moves to look ahead.
        next_turn_color: A character indicates which side that needs to generate new nodes and plays the next move.

    Returns:
        The maximum static board value and the best move.
    """

    pawn_codes, number_of_white, number_of_black = locate_pawns(cur_board)

    # compute a temporary static value to check if one side wins or not
    cur_board_static_val = static_board_evaluation(cur_board, pawn_codes, number_of_white, number_of_black,
                                                   target_color, next_turn_color)

    # check if reach the moves limit
    if number_moves_ahead == 0:  # yes then compute and return an empty list and the static board value
        return [], cur_board_static_val

    # check if one side wins
    if cur_board_static_val == 10 or cur_board_static_val == -10:  # return an empty list and the static board value
        # if one side wins
        return cur_board, cur_board_static_val

    # generate new nodes
    new_boards = move_generator(cur_board, board_size, next_turn_color, pawn_codes)
    number_moves_ahead -= 1

    # switch the turn
    if next_turn_color == "w":
        next_turn_color = "b"
    else:
        next_turn_color = "w"

    # compute the maximum static board value and record the corresponding move
    the_best_move_for_return = cur_board
    max_value_for_return = -2100000000  # set the initial value be a impossible small static board value
    for new_board in new_boards:
        cur_optimal_move, cur_static_board_val = min_value_propagation(new_board, board_size, target_color,
                                                                       number_moves_ahead, next_turn_color)
        if cur_static_board_val > max_value_for_return:
            the_best_move_for_return, max_value_for_return = new_board, cur_static_board_val

    return the_best_move_for_return, max_value_for_return


def min_value_propagation(cur_board, board_size, target_color, number_moves_ahead, next_turn_color):
    """This function is used for min level player to propagate staci board value.

    Args:
        cur_board:  The current board that a list of strings.
        board_size: The size of the board.
        target_color: A character indicates who is the player given this situation(Max).
        number_moves_ahead: The number indicates how many moves to look ahead.
        next_turn_color: A character indicates which side that needs to generate new nodes and plays the next move.

    Returns:
        The minimum static board value and the best move.
    """

    pawn_codes, number_of_white, number_of_black = locate_pawns(cur_board)

    # compute a temporary static value to check if one side wins or not
    cur_board_static_val = static_board_evaluation(cur_board, pawn_codes, number_of_white, number_of_black,
                                                   target_color, next_turn_color)

    # check if reach the moves limit
    if number_moves_ahead == 0:  # yes then compute and return an empty list and the static board value
        return [], cur_board_static_val

    # check if one side wins
    if cur_board_static_val == 10 or cur_board_static_val == -10:  # return an empty list and the static board value
        # if one side wins
        return cur_board, cur_board_static_val

    # generate new nodes
    new_boards = move_generator(cur_board, board_size, next_turn_color, pawn_codes)
    number_moves_ahead -= 1

    # switch the turn
    if next_turn_color == "w":
        next_turn_color = "b"
    else:
        next_turn_color = "w"

    # compute the maximum static board value and record the corresponding move
    the_best_move_for_return = cur_board
    min_value_for_return = 2100000000  # set the initial value be a impossible large static board value
    for new_board in new_boards:
        cur_optimal_move, cur_static_board_val = max_value_propagation(new_board, board_size, target_color,
                                                                       number_moves_ahead, next_turn_color)
        if cur_static_board_val < min_value_for_return:
            the_best_move_for_return, min_value_for_return = new_board, cur_static_board_val

    return the_best_move_for_return, min_value_for_return


def move_generator(cur_board, board_size, whose_turn, pawn_codes):
    """This function generates new valid board(nodes) based on current node.

    Args:
        cur_board: The current board that a list of strings.
        board_size: The size of the board.
        whose_turn: A character indicates which side to move this turn.
        pawn_codes: A list contains all pawn codes.

    Returns:
        A 2D list which contains lists of strings.
    """
    new_board_nodes = []
    for i in range(len(pawn_codes)):
        pawn_code = pawn_codes[i]
        if pawn_code[0] != whose_turn:
            continue
        else:  # check if the current pawn can move or not
            cur_row_idx = int(pawn_code[1])
            cur_col_idx = int(pawn_code[2])
            cur_row_string = cur_board[cur_row_idx]
            if whose_turn == "w":  # white pawn moves down
                # check if can move down
                new_row_idx_down = cur_row_idx + 1
                new_col_idx_down = cur_col_idx
                if if_on_the_board(new_row_idx_down, new_col_idx_down, board_size) and cur_board[new_row_idx_down][
                    new_col_idx_down] == "-":
                    cur_row_bottom_string = cur_board[new_row_idx_down]
                    # replace "w" with "-" on the original row
                    new_cur_row_string = cur_row_string[:cur_col_idx] + "-" + cur_row_string[cur_col_idx + 1:]

                    # replace "-" with "w" on the row below the original row
                    new_row_bottom_string = cur_row_bottom_string[:new_col_idx_down] + "w" + cur_row_bottom_string[
                                                                                             new_col_idx_down + 1:]
                    new_node = cur_board.copy()

                    # replace the original strings with the new strings using slicing
                    new_node[cur_row_idx] = new_cur_row_string
                    new_node[new_row_idx_down] = new_row_bottom_string
                    new_board_nodes.append(new_node)

                # check if can move down left and eat the black pawns if exists
                new_row_idx_down_left = cur_row_idx + 1
                new_col_idx_down_left = cur_col_idx - 1
                if if_on_the_board(new_row_idx_down_left, new_col_idx_down_left, board_size) and \
                        cur_board[new_row_idx_down_left][new_col_idx_down_left] == "b":
                    cur_row_bottom_string = cur_board[new_row_idx_down_left]
                    # replace "w" with "-" on the original row
                    new_cur_row_string = cur_row_string[:cur_col_idx] + "-" + cur_row_string[cur_col_idx + 1:]

                    # replace "b" with "w" on the row below the original row
                    new_row_bottom_string = cur_row_bottom_string[:new_col_idx_down_left] + "w" + cur_row_bottom_string[
                                                                                                  new_col_idx_down_left + 1:]
                    new_node = cur_board.copy()

                    # replace the original strings with the new strings using slicing
                    new_node[cur_row_idx] = new_cur_row_string
                    new_node[new_row_idx_down_left] = new_row_bottom_string
                    new_board_nodes.append(new_node)

                # check if can move down right eat the black pawns if exists
                new_row_idx_down_right = cur_row_idx + 1
                new_col_idx_down_right = cur_col_idx + 1
                if if_on_the_board(new_row_idx_down_right, new_col_idx_down_right, board_size) and \
                        cur_board[new_row_idx_down_right][new_col_idx_down_right] == "b":
                    cur_row_bottom_string = cur_board[new_row_idx_down_right]
                    # replace "w" with "-" on the original row
                    new_cur_row_string = cur_row_string[:cur_col_idx] + "-" + cur_row_string[cur_col_idx + 1:]

                    # replace "b" with "w" on the row below the original row
                    new_row_bottom_string = cur_row_bottom_string[
                                            :new_col_idx_down_right] + "w" + cur_row_bottom_string[
                                                                             new_col_idx_down_right + 1:]
                    new_node = cur_board.copy()

                    # replace the original strings with the new strings using slicing
                    new_node[cur_row_idx] = new_cur_row_string
                    new_node[new_row_idx_down_right] = new_row_bottom_string
                    new_board_nodes.append(new_node)

            else:  # black pawn moves up
                # check if can move up
                new_row_idx_up = cur_row_idx - 1
                new_col_idx_up = cur_col_idx
                if if_on_the_board(new_row_idx_up, new_col_idx_up, board_size) and \
                        cur_board[new_row_idx_up][new_col_idx_up] == "-":
                    cur_row_above_string = cur_board[new_row_idx_up]
                    # replace "b" with "-" on the original row
                    new_cur_row_string = cur_row_string[:cur_col_idx] + "-" + cur_row_string[cur_col_idx + 1:]

                    # replace "-" with "b" on the row above the original row
                    new_row_above_string = cur_row_above_string[:new_col_idx_up] + "b" + cur_row_above_string[
                                                                                         new_col_idx_up + 1:]
                    new_node = cur_board.copy()

                    # replace the original strings with the new strings using slicing
                    new_node[cur_row_idx] = new_cur_row_string
                    new_node[new_row_idx_up] = new_row_above_string
                    new_board_nodes.append(new_node)

                # check if can move up left
                new_row_idx_up_left = cur_row_idx - 1
                new_col_idx_up_left = cur_col_idx - 1
                if if_on_the_board(new_row_idx_up_left, new_col_idx_up_left, board_size) and \
                        cur_board[new_row_idx_up_left][new_col_idx_up_left] == "w":
                    cur_row_above_string = cur_board[new_row_idx_up_left]
                    # replace "b" with "-" on the original row
                    new_cur_row_string = cur_row_string[:cur_col_idx] + "-" + cur_row_string[cur_col_idx + 1:]

                    # replace "w" with "b" on the row above the original row
                    new_row_above_string = cur_row_above_string[:new_col_idx_up_left] + "b" + cur_row_above_string[
                                                                                              new_col_idx_up_left + 1:]
                    new_node = cur_board.copy()

                    # replace the original strings with the new strings using slicing
                    new_node[cur_row_idx] = new_cur_row_string
                    new_node[new_row_idx_up_left] = new_row_above_string
                    new_board_nodes.append(new_node)

                # check if can move up right
                new_row_idx_up_right = cur_row_idx - 1
                new_col_idx_up_right = cur_col_idx + 1
                if if_on_the_board(new_row_idx_up_right, new_col_idx_up_right, board_size) and \
                        cur_board[new_row_idx_up_right][new_col_idx_up_right] == "w":
                    cur_row_above_string = cur_board[new_row_idx_up_right]
                    # replace "b" with "-" on the original row
                    new_cur_row_string = cur_row_string[:cur_col_idx] + "-" + cur_row_string[cur_col_idx + 1:]

                    # replace "w" with "b" on the row above the original row
                    new_row_above_string = cur_row_above_string[:new_col_idx_up_right] + "b" + cur_row_above_string[
                                                                                               new_col_idx_up_right + 1:]
                    new_node = cur_board.copy()

                    # replace the original strings with the new strings using slicing
                    new_node[cur_row_idx] = new_cur_row_string
                    new_node[new_row_idx_up_right] = new_row_above_string
                    new_board_nodes.append(new_node)

    return new_board_nodes


def static_board_evaluation(cur_board, pawn_codes, number_of_white, number_of_black, target_color, next_turn_color):
    """This function computes the heuristic value of the current board. The evaluation is based on the logic
    introduced in the lecture. you win = +10, opponent win = -10, otherwise board value = # of your pawns - # of
    opponent's pawns.

    Args:
        cur_board: The n-element list.
        pawn_codes: A list contains all pawn codes.
        number_of_white: The total number of white pawns.
        number_of_black: The total number of black pawns.
        target_color: A character indicates who is the player given this situation(Max).
        next_turn_color: A character indicates which side that needs to generate new nodes and plays the next move.

    Returns: The static board value.

    """
    board_value = 0
    first_row = cur_board[0]
    last_row = cur_board[len(cur_board) - 1]

    # check if one side's pawns has reached the opposite side
    if first_row.find("b") != -1:
        if target_color == "b":  # black turn and black wins
            board_value = 10
        else:  # white turn and black wins
            board_value = -10
        return board_value

    if last_row.find("w") != -1:
        if target_color == "w":  # white turn and white wins
            board_value = 10
        else:  # black turn and white wins
            board_value = -10
        return board_value

    # check if one side's loses all pawns
    if number_of_white == 0:
        if target_color == "w":  # white turn and no white pawns
            board_value = -10
        else:
            board_value = 10  # black turn and no white pawns
        return board_value

    if number_of_black == 0:
        if target_color == "b":  # black turn and no black pawns
            board_value = -10
        else:
            board_value = 10  # white turn and no black pawns
        return board_value

    # check if all pawns cannot move
    pawns_can_move = if_can_move(cur_board, pawn_codes, next_turn_color)
    if not pawns_can_move:  # current side loses the game
        if next_turn_color == target_color:  # if we do the next move but cannot move
            board_value = -10
        else:  # if the opponent do the next move but cannot move
            board_value = 10
        return board_value

    # compute the difference between pawns' count since no one has won
    if target_color == "w":  # white is the max
        board_value = number_of_white - number_of_black
    else:  # black is the max
        board_value = number_of_black - number_of_white

    return board_value


def locate_pawns(cur_board):
    """This function gets the positions of each pawn.

    Args:
        cur_board: The n-element list.

    Returns:
        A list contains the positions of each pawn and the numbers of white pawns and black pawns.
    """

    # define the result list
    pawn_codes = []

    # concatenate the rows to a string
    cur_board_string = "".join(cur_board)

    # compute the numbers of white and black pawns
    number_of_white = cur_board_string.count("w")
    number_of_black = cur_board_string.count("b")

    # find the indices of each pawn
    for i in range(len(cur_board)):
        for j in range(len(cur_board[i])):
            pawn_code = ""
            cur_square = cur_board[i][j]
            if cur_square == "-":  # empty square
                continue
            elif cur_square == "w":  # square has a white pawn
                pawn_code += "w"
                pawn_code += str(i)
                pawn_code += str(j)
            else:  # square has a black pawn
                pawn_code += "b"
                pawn_code += str(i)
                pawn_code += str(j)

            # push the code into returned list
            pawn_codes.append(pawn_code)

    return pawn_codes, number_of_white, number_of_black


def if_can_move(cur_board, pawn_codes, whose_turn):
    """This function checks if the current side player can move without invoking move generator function.

    Args:
        cur_board: The n-element list.
        pawn_codes: pawn_codes: A list contains all pawn codes.
        whose_turn: A character indicates which side to move this turn.

    Returns:
        A boolean value indicates whether the current side can move or not.
    """

    one_pawn_can_move = False
    for i in range(len(pawn_codes)):
        pawn_code = pawn_codes[i]
        if pawn_code[0] != whose_turn:
            continue
        else:  # check if the current pawn can move or not
            cur_row_idx = int(pawn_code[1])
            cur_col_idx = int(pawn_code[2])
            board_size = len(cur_board)
            if whose_turn == "w":  # white pawn moves down
                # check if can move down
                new_row_idx_down = cur_row_idx + 1
                new_col_idx_down = cur_col_idx
                if if_on_the_board(new_row_idx_down, new_col_idx_down, board_size) and cur_board[new_row_idx_down][
                    new_col_idx_down] == "-":
                    one_pawn_can_move = True
                    return one_pawn_can_move

                # check if can move down left and eat the black pawns if exists
                new_row_idx_down_left = cur_row_idx + 1
                new_col_idx_down_left = cur_col_idx - 1
                if if_on_the_board(new_row_idx_down_left, new_col_idx_down_left, board_size) and \
                        cur_board[new_row_idx_down_left][new_col_idx_down_left] == "b":
                    one_pawn_can_move = True
                    return one_pawn_can_move

                # check if can move down right eat the black pawns if exists
                new_row_idx_down_right = cur_row_idx + 1
                new_col_idx_down_right = cur_col_idx + 1
                if if_on_the_board(new_row_idx_down_right, new_col_idx_down_right, board_size) and \
                        cur_board[new_row_idx_down_right][new_col_idx_down_right] == "b":
                    one_pawn_can_move = True
                    return one_pawn_can_move

            else:  # black pawn moves up
                # check if can move up
                new_row_idx_up = cur_row_idx - 1
                new_col_idx_up = cur_col_idx
                if if_on_the_board(new_row_idx_up, new_col_idx_up, board_size) and \
                        cur_board[new_row_idx_up][new_col_idx_up] == "-":
                    one_pawn_can_move = True
                    return one_pawn_can_move

                # check if can move up left
                new_row_idx_up_left = cur_row_idx - 1
                new_col_idx_up_left = cur_col_idx - 1
                if if_on_the_board(new_row_idx_up_left, new_col_idx_up_left, board_size) and \
                        cur_board[new_row_idx_up_left][new_col_idx_up_left] == "w":
                    one_pawn_can_move = True
                    return one_pawn_can_move

                # check if can move up right
                new_row_idx_up_right = cur_row_idx - 1
                new_col_idx_up_right = cur_col_idx + 1
                if if_on_the_board(new_row_idx_up_right, new_col_idx_up_right, board_size) and \
                        cur_board[new_row_idx_up_right][new_col_idx_up_right] == "w":
                    one_pawn_can_move = True
                    return one_pawn_can_move

    return one_pawn_can_move


def if_on_the_board(row_index, col_index, board_size):
    """This function checks if a move out of the boundaries of the board.

    Args:
        row_index: The row index of the move.
        col_index: The column index of the move.
        board_size: The size of the board.

    Returns:
        A boolean value indicates whether the move is on the board or not.
    """
    if board_size > row_index >= 0 and board_size > col_index >= 0:
        return True
    else:
        return False
