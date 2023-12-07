import sys

def count_to_3():
    count = 0
    while count < 3:
        input('Press Enter to count: ')
        count += 1
        print(count)

if __name__ == '__main__':
    count_to_3()