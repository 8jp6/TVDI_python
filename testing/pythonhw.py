import random
'''1'''
# onf = True
# gradelist = []
# countpass = 0
# countpassnt = 0
# while onf:
#     a = int(input("grade"))
#     if a == 9999:break
#     if a >= 90:
#         print('優秀')
#     elif a < 60:
#         print('不及格')
#     gradelist.append(a)
# for i in gradelist:
#     if i > 60:countpass+=1
#     if i <= 60:countpassnt+=1
# print(f'及格{countpass}人不及格{countpassnt}人')

'''2'''
# a = []
# b = []
# osu = 0
# gisu = 0
# while len(b) < 20:
#     a.append(random.randint(1,100))
#     b = set(a)
# for i in b:
#     if i % 2 == 0:osu+=1
#     if i % 2 != 0:gisu+=1
# print(b)
# print(f'偶數{osu},奇數{gisu}')

'''3'''
# a = tuple(input('字串'))
# a = list(a)
# for i in range(len(a)-1,-1,-1):
#     print(a[i],end="")

'''4'''
# def count(low,high):
#     a = 0
#     for i in range(low,high+1):
#         a+=i
#     print(a,a/(high-low+1))
# count(int(input('範圍低')),int(input('範圍高')))

'''5'''
# a=[]
# b=0
# for i in range(5):
#     a.append(int(input('數字')))
# for i in a:
#     b+=i
# meanb = b/5
# print(set(a))
# print(f'總和{b},平均數{meanb}')