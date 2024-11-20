if __name__ == '__main__':
    n=int(input("enter number of smarks"))
    student_marks = {}
    for i in range(n):
        name=input("enter names: ").split()
        scores=input("enter score").split()
        scores=list(map(float,scores))
        student_marks[name] = scores
        print(student_marks)