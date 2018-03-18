def print_color_header(color):
    if color == 0 or color =='black':
        return '\033[0m'
    elif color == 1 or color =='green':  # GREEN
        return '\033[32m'
    elif color == 2 or color =='yellow':  # YELLOW
        return '\033[33m'
    elif color == 3 or color =='red':  # RED
        return '\033[31m'
    elif color == 4 or color =='blue':  # BLUE
        return '\033[36m'
    elif color == 5 or color =='purple':  # Purple
        return '\033[35m'
    elif color == 'ok':
        return '\033[42m[  OK  ]\033[0m     '
    elif color == 'warn':
        return '\033[43m[ WARN ]\033[0m     '
    elif color == 'fail':
        return '\033[41m[ FAIL ]\033[0m     '
    elif color == 'info':
        return '\033[44m[ INFO ]\033[0m     '

def print_message(msg, color=0):
    if color == 'info':
        print print_color_header(color) , print_color_header('blue') , msg , print_color_header(0)
    elif color == 'warn':
        print print_color_header(color) , print_color_header('yellow') , msg , print_color_header(0)
    elif color == 'ok':
        print print_color_header(color) , print_color_header('green') , msg , print_color_header(0)
    elif color == 'fail':
        print print_color_header(color) , print_color_header('red') , msg , print_color_header(0)
    else:
        print_msg = print_color_header(color) , msg , print_color_header(0)
    


def load_page(localpath):
    with open(localpath,'rb') as indexfile:
        data = indexfile.readlines()
    return "".join(data)

def showoff():
    template = "\033[%d%dm@"
    print "  0 1 2 3 4 5 6 7 8 9"
    for i in range (0,9):
        print '%d' %i,
        for j in range(0,9):
            print "\033[%d%dm@"%(i,j),
        print ''