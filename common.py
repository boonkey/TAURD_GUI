import threading
import sys

def print_color_header(color):
    if color == 0 or color == 'black':
        return '\033[0m'
    elif color == 1 or color == 'green':  # GREEN
        return '\033[32m'
    elif color == 2 or color == 'yellow':  # YELLOW
        return '\033[33m'
    elif color == 3 or color == 'red':  # RED
        return '\033[31m'
    elif color == 4 or color == 'blue':  # BLUE
        if 'linux' in sys.platform:
            return '\033[36m'
        return '\033[34m'
    elif color == 5 or color == 'purple':  # Purple
        return '\033[35m'
    elif color == 'ok':
        return '\r\033[32m[  OK  ]\033[0m     '
    elif color == 'warn':
        return '\r\033[33m[ WARN ]\033[0m     '
    elif color == 'fail':
        return '\r\033[31m[ FAIL ]\033[0m     '
    elif color == 'info':
        if 'linux' in sys.platform:
            return '\r\033[36m[ INFO ]\033[0m     '
        return '\r\033[34m[ INFO ]\033[0m     '
    elif color == 'verb':
        return '\r\033[35m[ VERB ]\033[0m     '


printing_lock = threading.Lock()


def print_message(msg, color=0):
    printing_lock.acquire()
    if color == 'info':
        print print_color_header(color), print_color_header('blue'), msg, print_color_header(0)
    elif color == 'warn':
        print print_color_header(color), print_color_header('yellow'), msg, print_color_header(0)
    elif color == 'ok':
        print print_color_header(color), print_color_header('green'), msg, print_color_header(0)
    elif color == 'fail':
        print print_color_header(color), print_color_header('red'), msg, print_color_header(0)
    elif color == 'verb':
        print print_color_header(color), print_color_header('purple'), msg, print_color_header(0)
    else:
        print print_color_header(color), msg, print_color_header(0)
    printing_lock.release()


def load_page(localpath):
    with open(localpath, 'rb') as indexfile:
        data = indexfile.readlines()
    return "".join(data)


def showoff():
    template = "\033[%d%dm@"
    print "  0 1 2 3 4 5 6 7 8 9"
    for i in range(0, 9):
        print '%d' % i,
        for j in range(0, 9):
            print "\033[%d%dm@" % (i, j),
        print ''

sensor_conf = "1:speed,0,120;" \
                      "2:rpm,0,8000;" \
                      "3:braking,0,100;" \
                      "4:throttle,0,100;" \
                      "5:wing_position,-100,100;" \
                      "6:voltage,9,14;" \
                      "7:oil_temp,60,130;" \
                      "8:water_temp,60,130;" \
                      "9:fuel_consumption,0,25;" \
                      "10:random_gague,0,256;<FIN>"