if __name__ == '__main__':
    x = int(input("enter length"))
    y = int(input("enter ht"))
    z = int(input("enter wd"))
    n = int(input("enter volume"))
coordinates=[[i,j,k] for i in range(x+1) for j in range(y+1)
for k in range(z+1) if(i+j+k!=n)] 
print(coordinates)


                    
