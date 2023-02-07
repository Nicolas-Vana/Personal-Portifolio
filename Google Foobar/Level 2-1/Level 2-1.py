#Naive Solution

'''def solution(x, y):
    index = 1
    for height in range(y-1):
        index += height + 1

    for lenght in range(x-1):
        index += lenght + y + 1

    return index'''

''' The solution presented above solves the problem but it fails some of tests because of time constraints.
    By using sums of arithmetic progressions we can solve this problem in constant time.
'''

def solution(x, y):
    index = 1

    index += y*(y-1)/2

    index += (2*y+x)*(x-1)/2

    return str(int(index))

sol = solution(3,2)

print(sol)
