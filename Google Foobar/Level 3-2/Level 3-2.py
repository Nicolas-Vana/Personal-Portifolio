
# This solution relies on some properties of the problem that must be proved.
# This proofs are not inaction_counterluded but the results will be assumed here.]

def solution(n):

    n = int(n)
    action_counter = 0

    # While the number of pellets is greater than 4 do the following actions
    while n >= 4:
        # If it is divisible by two this is the most efficent way to get down to one, so do this and add one to the action_counter.
        if n % 2 == 0:
            n /= 2
            action_counter += 1
            continue

        # If it was not divisible by 3 then this number mod 4 is either 1 or 3.
        mod = n % 4

        # If mod 3 == 1 then do the action to decrease one pellet then divide by two.
        if mod == 1:
            n = (n-1)/2
            action_counter += 2

        # If mod 3 == 3 then do the action to increase one pellet then divide by two.
        else:
            n = (n+1)/2
            action_counter += 2
    # If n < 4 then its either 3, 2 or 1. In which cases there are two, one, and zero actions left, respectively.
    if n == 3:
        action_counter += 2
    elif n == 2:
        action_counter += 1

    return action_counter


n = '253'
solution = solution(n)
print(solution)
