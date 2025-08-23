> _PS:因为红明谷和NCTF时间重了导致想起来打这个这个比赛时已经快结束了就没太认真打，看到一个挺有意思的misc的题一看分数还挺高就想着挑战一下，结果遗憾离场。_
>

看了wp我才发现原来还有misc题目能用web的方法解决

题目的源码如下：

```python
from random import *
import time
import pyfiglet

text = "X1crypsc"
ascii_art = pyfiglet.figlet_format(text)
print(ascii_art)
time.sleep(1)
print('[+]I want to play a game.\n')
time.sleep(1)
print('[+]If you win the game, I will give you a gift:)\n')
time.sleep(1)
print('[+]But try to beat the monster first:)\n')
time.sleep(1)
print('[+]Good luck!\n')
print('[+]You got a weapon!\n')
damage_rng = ()
def regenerate_damage():
    global damage_rng
    base = getrandbits(16)
    add = getrandbits(16)
    damage_rng = (base ,base + add)
monster_health = getrandbits(64)
menu = '''
---Options---
[W]eapon
[A]ttack
[E]xit
'''
regenerate_damage()
print(menu)
HP = 3
while True:
    if monster_health <= 0:
        print('[+] Victory!!!')
        break
    if HP <= 0:
        print('[!] DEFEAT')
        exit(0)
    print(f'[+] Monster current HP:{monster_health}')
    print(f'[+] Your current HP: {HP}')
    opt = input('[-] Your option:')
    if opt == 'W':
        print(f'[+] Current attack value: {damage_rng[0]} ~ {damage_rng[1]}')
        if input('[+] Do you want to refresh the attack profile of the weapon([y/n])?') == 'y':
            regenerate_damage()
            print(f'[+] New weapon attack value: {damage_rng[0]} ~ {damage_rng[1]}')
    elif opt == 'A':
        print('[+] The monster sensed of an imminent danger and is about to teleport!!\n')
        print('[+] Now you have to aim at the monster\'s location to hit it!\n')
        print('[+]Input format: x y\n')
        x,y = map(int,input(f'[-] Provide the grid you\'re willing to aim:').split())
        if [x,y] ==  [randrange(2025),randrange(2025)]:
            dmg = min(int(randint(*damage_rng) ** (Random().random() * 8)),monster_health)
            print(f'[+] Decent shot! Monster was hevaily damaged! Damage value = {dmg}')
            monster_health -= dmg
        else:
            print("[+] Your bet didn't pay off, and the monster presented a counterattack on you!")
            HP -= 1     
    elif opt == 'E':
        print('[+] Bye~')
        exit(0)
    else:
        print('[!] Invalid input')
print('[+]Well done! You won the game!\n')
print('[+]And here is your gift: you got a chance to create a time capsule here and we\'ll keep it for you forever:)\n')

'''
[REDACTED]
'''
```

就是一个小游戏，连上之后有三个选项，W（刷新武器攻击力范围），A（攻击怪兽），E（退出游戏）。怪兽血量是一个20位的随机数，并且每次攻击后位置会随机生成在一个2025*2025的坐标内，一般来说只有当武器攻击力数值刷新到足够高，且攻击的坐标刚好猜中怪兽刷新位置时才能获得胜利，一句游戏只有三次机会，三次没打中血量归零，游戏失败。

比赛时花了半天时间写脚本爆破怪兽坐标，才意识到每次攻击时怪兽坐标会变，常规方法根本行不通，又试着输入非常规的东西发现有过滤，就卡在那了。直到今天看了wp才弄明白。

**第一阶段（MT19937逆向）：**

知识点在于python的内置random类采用了MT19937伪随机数算法，所以这种解法是MT19937的逆向

```python
from sage.all import *
from Crypto.Util.number import *
from tqdm import trange
from pwn import *
from random import *
 
def construct_a_row(RNG): 
    row = []
    RNG.getrandbits(64)
    RNG.getrandbits(16)
    RNG.getrandbits(16)
    for _ in range(19968//16):
        tmp = RNG.getrandbits(16)
        row += list(map(int, bin(tmp)[2:].zfill(16)))
    return row
 
# 构造线性方程组的矩阵 
L = [] 
for i in trange(19968): 
    state = [0]*624  # MT19937使用624个32位整数作为状态 
    # 构造一个只有一位为1,其他都为0的序列 
    temp = "0"*i + "1"*1 + "0"*(19968-1-i) 
    # 将这个序列分成624段,每段32位,转换为整数 
    for j in range(624): 
        state[j] = int(temp[32*j:32*j+32], 2) 
     
    RNG = Random() 
    RNG.setstate((3,tuple(state+[624]),None))
    L.append(construct_a_row(RNG)) 
 
# 将L转换为GF(2)上的矩阵（二进制域） 
L = Matrix(GF(2),L)
print(L.nrows(), L.ncols())
 
def MT19937_re(state): 
    try: 
        # 构造目标向量R 
        R = []
        for i in state:
            R += list(map(int, bin(i)[2:].zfill(16)))
         
        R = vector(GF(2), R)
        s = L.solve_left(R)  # 这里可能会抛出异常 
         
        # 将解转换为二进制字符串 
        init = "".join(list(map(str,s))) 
        state = [] 
        # 将解重新分割成624个32位整数 
        for i in range(624): 
            state.append(int(init[32*i:32*i+32],2)) 
 
        # 创建新的RNG并设置恢复出的状态 
        RNG1 = Random() 
        RNG1.setstate((3,tuple(state+[624]),None)) 
 
        return RNG1
         
    except Exception as e: 
        print(f"[-]{e}")
        pass
 
addr = "39.106.16.204:11749".split(":")
io = remote(addr[0], addr[1])
monster_hp = int(io.recvline_startswith(b"[+] Monster current HP:")[23:-1])
io.recvline()
print(monster_hp)
 
inital_weapon = None
state = []
for i in trange(19968//2//16):
    io.sendafter(b"[-] Your option:",b"W\n")
    tmp1, tmp2 = map(int,io.recvline_startswith(b"[+] Current attack value: ")[26:].split(b" ~ "))
    if inital_weapon == None:
        inital_weapon = [tmp1,tmp2-tmp1]
        print(inital_weapon)
 
    io.sendafter(b"[+] Do you want to refresh the attack profile of the weapon([y/n])?",b"y\n")
    tmp1, tmp2 = map(int,io.recvline_startswith(b"[+] New weapon attack value: ")[29:].split(b" ~ "))
    state += [tmp1,tmp2-tmp1]
    io.recvline()
    io.recvline()
 
RNG = MT19937_re(state)
RNG.getrandbits(64)
RNG.getrandbits(16)
RNG.getrandbits(16)
for _ in range(19968//2//16):
    RNG.getrandbits(16)
    RNG.getrandbits(16)
 
io.sendafter(b"[-] Your option:",b"A\n")
io.sendafter(b"[-] Provide the grid you're willing to aim:",(str(RNG.randrange(2025))+" "+str(RNG.randrange(2025))+"\n").encode())
 
io.interactive()
```

我草看不懂啊，这一块不是我的强项，先挖个坑吧，等我把另外两种解法搞明白再填（

**第二阶段（linux定时任务提权）：**



