if __name__ == '__main__':
    list=[]
    N = int(input())
    for i in range(N):
        element=input().split()
        if element[0]=="insert":
            index=int(element[1])
            number=int(element[2])
            list.insert(index,number)
            print(list)
        elif element[0]=="print":
            print(list)  
        elif element[0]=="remove":
            number=int(element[1])
            list.remove(number)
        elif element[0]=="append":
            number=int(element[1])
            list.append(number)
        elif element[0]=="sort":
            list.sort()
        elif element[0]=="pop":
            list.pop()
        elif element[0]=="reverse":
            list.reverse()

    