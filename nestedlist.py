if __name__ == '__main__' :
    nested_list=[]
    n=int(input("enter the no of times"))
    for i in range(n):
        name=input("enter sname")
        score=float(input("enter marks"))
        nested_list.append([name, score])
    scores=[sublist[1] for sublist in nested_list]
    unique_scores=list(set(scores))
    unique_scores.sort()

    #if len(nested_list)> 1:
        #sec_max=nested_list[1]
        #print(sec_max)
    #print(sec_max)
    print(nested_list)
    if len(unique_scores)> 1:
        sec_max=unique_scores[1]
        print(sec_max)
    sec_low_names=[sublist[0] for sublist in nested_list if sublist[1]==sec_max]
    sec_low_names.sort()
    print(sec_low_names)
    for name in sec_low_names:
        print(name)


    
