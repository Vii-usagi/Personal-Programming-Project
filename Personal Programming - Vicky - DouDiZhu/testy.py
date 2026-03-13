'''
from os import system
from time import sleep

CODE = "\x1b[38;2;{};{};{}m"
# full RGB colour
pause = 0.5

system("cls")
i = 0
for r in range(0, 256, 3):
    for g in range(0, 256, 3):
        for b in range(0, 256, 3):
            print(CODE.format(r, g, b), end="")
            try:
                print(chr(i), end="")
            except UnicodeEncodeError:
                i = 0
            i += 1
            
            pause = pause * 0.9  # 10 % smaller
            

'''
# what will happen?!

'''
from os import system
from time import sleep


print("Player 1 look away now")
for i in range(5, -1, -1):
    print(i)
    sleep(1)
system("cls")
print("player 2 look now...")
sleep(5)
'''

a = int()
b = int()
c= int()
oi= 0.5*a*b**2
oi2 = a*10*c
print(oi+oi2)