import random

# Global Variables:
# stack_set - the stack to take new cards from
# snake - the current running domino snake

def create_set():
    global stack_set
    global player_set
    global computer_set

    full_stack = [[i, j] for i in range(7) for j in range(i, 7)]
    random.shuffle(full_stack)
    stack_set, computer_set, player_set = split_dominos(full_stack)

def split_dominos(dominos):
    computer_set = [dominos.pop() for i in range(7)]
    player_set = [dominos.pop() for i in range(7)]
    return dominos, computer_set, player_set

def starting_piece():
    global status
    global snake

    computer_double = [x[0] for x in computer_set if x[0] == x[1]]
    computer_double.sort(reverse=True)
    computer_double = computer_double[0] if len(computer_double) > 0 else -1
    player_double = [x[0] for x in player_set if x[0] == x[1]]
    player_double.sort(reverse=True)
    player_double = player_double[0] if len(player_double) > 0 else -1

    if player_double > computer_double:
        snake = [player_set.pop(player_set.index([player_double, player_double]))]
        status = "computer"
    elif player_double < computer_double:
        snake = [computer_set.pop(computer_set.index([computer_double, computer_double]))]
        status = "player"
    else:
        create_set()
        starting_piece()

def print_header():
    print('=' * 70)

def print_stock_sizes():
    print('Stock size:', len(stack_set))
    print('Computer pieces:', len(computer_set))
    print()

def print_snake():
    if len(snake) <= 6:
        for piece in snake:
            print(piece, end='')
    else:
        for piece in snake[:3]:
            print(piece, end='')
        print('...', end='')
        for piece in snake[-3:]:
            print(piece, end='')
    print()

def print_player_stock():
    print('Your pieces:')
    for i, piece in enumerate(player_set):
        print(f'{i + 1}:{piece}')
    print()

def print_status():
    if status == 'player':
        print("Status: It's your turn to make a move. Enter your command.")
    else:
        print("Status: Computer is about to make a move. Press Enter to continue...")

def print_gameplay():
    print_header()
    print_stock_sizes()
    print_snake()
    print()
    print_player_stock()

def computer_move():
    # command = random.randint(-len(computer_set), len(computer_set))
    total_numbers = [x for piece in snake for x in piece]
    computer_numbers = [x for piece in computer_set for x in piece]
    total_numbers.extend(computer_numbers)
    pieces_score = dict()
    numbers_score = {n: total_numbers.count(n) for n in set(computer_numbers)}
    for i, piece in enumerate(computer_set):
        score = numbers_score[piece[0]] + numbers_score[piece[1]]
        pieces_score[i] = score
    pieces_score = sorted(pieces_score.items(), key = lambda x: x[1], reverse=True)
    command_order = [x[0] + 1 for x in pieces_score]
    command_order.append(0)
    for command in command_order:
        if move(command) or move(-command):
            break

def move(command):
    global status

    if command == 0:
        try:
            if status == 'computer':
                computer_set.append(stack_set.pop())
            else:
                player_set.append((stack_set.pop()))
        except IndexError:
            pass
        finally:
            status = 'computer' if status == 'player' else 'player'
            return True

    location = 0 if command < 0 else -1
    if status == 'computer':
        domino = computer_set[abs(command) - 1]
        if not legal_move(domino, location):
            return False
    else:
        domino = player_set[abs(command) - 1]
        if not legal_move(domino, location):
            print("Illegal move. Please try again.")
            return False

    domino = orient_domino(domino, location)
    location = 0 if command < 0 else len(snake)
    snake.insert(location, domino)

    if status == 'computer':
        del computer_set[abs(command) - 1]
    else:
        del player_set[abs(command) - 1]

    status = 'computer' if status == 'player' else 'player'
    return True

def check_game():
    if len(computer_set) == 0:
        print('Status: The game is over. The computer won!')
        exit()
    elif len(player_set) == 0:
        print('Status: The game is over. You won!')
        exit()
    if snake[0][0] == snake[-1][1]:
        x = snake[0][0]
        count = sum([pair.count(x) for pair in snake])
        if count == 8:
            print("Status: The game is over. It's a draw!")
            exit()

def read_command():
    x = input()
    try:
        x = int(x)
        if abs(x) > len(player_set):
            raise ValueError
    except:
        print('Invalid input. Please try again.')
        x = read_command()
    finally:
        return x

def legal_move(domino, snake_location_to_add):
    index = 1 if snake_location_to_add == -1 else 0
    return snake[snake_location_to_add][index] in domino

def orient_domino(domino, location):
    if ((location == 0) and (domino[1] != snake[location][0])) or \
            ((location == - 1) and (domino[0] != snake[location][1])):
        domino = list(reversed(domino))
    return domino

create_set()
starting_piece()

while True:
    print_gameplay()
    check_game()
    print_status()
    if status == 'computer':
        input()
        computer_move()
    else:
        command = read_command()
        while not move(command):
            command = read_command()


