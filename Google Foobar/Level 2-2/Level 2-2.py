
def solution(l):

    ''' Start from the largest solutions because thats what we are trying to find
        Also, the condition for divisibility by 3 is that the sum of digits is equal to
        to 3. Because of this is always better to use the largest digits at the start of
        the number.
        Not using binary masks and instead creating all the combinations between digits in
        any order will exceed time and space constraints'''
    l.sort(reverse=True)

    # set initial values
    binary = 0
    sol = 0

    # loop through all the combinations of digits that can be created using the list to form numbers
    while binary < 2**len(l)-1:
        # Get a binary mask to define a number from a subset of digits in the list
        mask = get_mask(binary, len(l)+1)

        # define temporary list of "usable" digits
        tmp = [i for (i, v) in zip(l, mask) if not v]

        # Check for divisibility by 3
        if sum(tmp) % 3 == 0:

            # Validate if the candidate is greater than the current largest solution and attribute if it is
            candidate = int(''.join(map(str,tmp)))
            if candidate > sol:
                sol = candidate

        binary += 1

    return sol
# Creates a binary mask for the list based on the lenght of the list and the current binary value
def get_mask(binary, length):
    # Get binary representation of passed binary value
    tmp = list(bin(binary)[2:])
    # Create list of the digits in the binary value
    tmp = [int(x) for x in tmp]

    # zero-pad the list
    if len(tmp) < length:
        zero_padded = [0]*(length-len(tmp)-1)
        zero_padded.extend(tmp)

    return zero_padded

l = [3, 1, 4, 1, 5, 9]
a = solution(l)
