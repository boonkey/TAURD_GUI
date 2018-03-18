import threading

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

printing_lock = threading.Lock()

def print_message(msg, color=0):
    printing_lock.acquire()
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
    printing_lock.release()


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

def find_ticks(min, max):
    n = max - min
    factorization = set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(pow(n, 0.5) + 1)) if n % i == 0)))
    
    for j in range(-11, -5):
        m = n / -j
        small_fact = set(reduce(list.__add__, 
                ([i, m//i] for i in range(1, int(pow(m, 0.5) + 1)) if m % i == 0)))
        if 4 in small_fact:
            print '%d big ticks, 4 small ticks' %-j
    for j in range(-11, -5):
        m = n / -j
        small_fact = set(reduce(list.__add__, 
                ([i, m//i] for i in range(1, int(pow(m, 0.5) + 1)) if m % i == 0)))
        if 5 in small_fact:
            print '%d big ticks, 5 small ticks' %-j
    
    for j in range(-11, -5):
        m = n / -j
        small_fact = set(reduce(list.__add__, 
                ([i, m//i] for i in range(1, int(pow(m, 0.5) + 1)) if m % i == 0)))
        if 3 in small_fact:
            print '%d big ticks, 3 small ticks' %-j

    for j in range(-11, -5):
        m = n / -j
        small_fact = set(reduce(list.__add__, 
                ([i, m//i] for i in range(1, int(pow(m, 0.5) + 1)) if m % i == 0)))
        if 2 in small_fact:
            print '%d big ticks, 2 small ticks' %-j

find_ticks(0,255)
