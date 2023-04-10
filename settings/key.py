from random import randint

def gen():
    a = 'abcdefghijklmnopqrstuvwxyz_1234567890@№$%?&*[]/\|'
    password = ''
    for i in range(60):
        i = randint(0,len(a)-1)
        password += a[i]
    return password

