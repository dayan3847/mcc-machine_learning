import os

if __name__ == '__main__':
    if not os.path.isfile('dataCircle_fix.txt'):
        with open('dataCircle.txt', 'r') as f:
            lines = f.readlines()
        # print('lines:', lines)
        lines_fixed = [' '.join(line.split()) + '\n' for line in lines]
        # print('lines_fixed:', lines_fixed)
        with open('dataCircle_fix.txt', 'w') as f:
            f.writelines(lines_fixed)
