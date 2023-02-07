
def solution(start, length):
    # Initialize variables. Flushes refers to the number of times all workers have been cleared.
    flushes = 0
    sol = 0
    current_start = start

    #Iterate through flushes until there are no more rabits in the queue that will be checked
    for i in range(length):
        # Compute current checksum
        sol = sol ^ (find_xor_range(current_start, current_start + length - flushes -1))

        # Update axiliary variables
        current_start += length
        flushes += 1

    return sol

# Uses the O(1) implementation to obtain the XOR of a sequence of number from 1 to n.
def find_xor_seq(n):
    mod = n % 4

    if mod == 0:
        return n
    elif mod == 1:
        return 1
    elif mod == 2:
        return n+1
    else:
        return 0

# Uses the previous function to obtain the XOR of a sequence of numbers from l to r in O(1)
def find_xor_range(l, r):
    return (find_xor_seq(l-1) ^ find_xor_seq(r))

print(solution(17,4))
