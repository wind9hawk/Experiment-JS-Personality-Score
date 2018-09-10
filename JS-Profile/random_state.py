import random
random.seed(10)
random_lst = []
for i in range(int(2868*0.8)):
    a = random.randint(1, 3868)
    random_lst.append(a)

# print JS_Users_scale[2751], '\n'
# print JS_Users_scale[2260], '\n'
# print JS_Users_scale[1242], '\n'
# print JS_Users_scale[631], '\n'
# print JS_Users_scale[1451], '\n'
for i in random_lst:
    if i == 2751:
        print i, '\n'
    if i == 2260:
        print i, '\n'
    if i == 1242:
        print i, '\n'
    if i == 631:
        print i, '\n'
    if i == 1451:
        print i, '\n'
