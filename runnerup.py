if __name__ == '__main__':
    n = int(input("enter no of elements"))
    arr = map(int, input().split())
    storing=[]
for i in range(n):
    value=input(f"enter ele {i}")
    storing.append(value)
    print(storing)
my_list=list(set(storing))
sorted_list=my_list.sort()
print(sorted_list)
print(my_list)
second_max=my_list[-2]
print(second_max)