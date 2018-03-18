def print_color_header(color):
    if color == 0:
        return '\033[0m'
    elif color == 1:  # GREEN
        return '\033[32m'
    elif color == 2:  # YELLOW
        return '\033[33m'
    elif color == 3:  # RED
        return '\033[31m'
    elif color == 4:  # BLUE
        return '\033[34m'
    elif color == 5:  # Purple
        return '\033[35m'

def print_message(msg, color=0):
    print_msg = print_color_header(color) + msg + print_color_header(0)
    print print_msg
