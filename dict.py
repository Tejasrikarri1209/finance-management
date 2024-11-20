if __name__ == '__main__':
    n=int(input())
    student_marks= {}
    for i in range(n):
        name=input("enter names").split()
        scores=input
        student_marks[name]=scores
        query_name=input("enter query name")
        average=sum(scores)/len(scores)
        print(average)
    print(student_marks)