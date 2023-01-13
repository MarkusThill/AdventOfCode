import numpy as np

def day8_1():
    # Using readlines()
    file1 = open('input8_1.txt', 'r')
    lines = file1.readlines()
    lines = [l.strip() for l in lines]
    lines = [list(l) for l in lines]

    lines = [ [int(ll) for ll in l] for l in lines]

    X = np.array(lines)

    M_global = (np.zeros_like(X) != 0)

    # Rows down
    x = -np.ones_like(X[0])
    M = (np.zeros_like(X) != 0)
    for i in range(X.shape[0]):
        M[i] = (X[i] > x)
        x = np.maximum(x, X[i])
        # print(x)
    M_global |= M

    # Rows up
    x = -np.ones_like(X[0])
    M = (np.zeros_like(X) != 0)
    for i in reversed(range(X.shape[0])):
        M[i] = (X[i] > x)
        x = np.maximum(x, X[i])
        # print(x)
    M_global |= M

    # Cols down
    x = -np.ones_like(X[1])
    M = (np.zeros_like(X) != 0)
    for i in range(X.shape[0]):
        M[:,i] = (X[:, i] > x)
        x = np.maximum(x, X[:, i])
        # print(x)
    M_global |= M

    # Cols up
    x = -np.ones_like(X[1])
    M = (np.zeros_like(X) != 0)
    for i in reversed(range(X.shape[0])):
        M[:, i] = (X[:, i] > x)
        x = np.maximum(x, X[:, i])
        # print(x)
    M_global |= M


    print("Solution day 8.1:", M_global.sum())



def day8_2():
    # Using readlines()
    file1 = open('input8_1.txt', 'r')
    lines = file1.readlines()
    lines = [l.strip() for l in lines]
    lines = [list(l) for l in lines]

    lines = [ [int(ll) for ll in l] for l in lines]

    X = np.array(lines)

    M_global = np.ones_like(X)

    # Rows down
    M = np.zeros_like(X)
    for i in range(X.shape[0]):
        x = (np.zeros_like(X[0]) == 0)
        inc = np.zeros_like(X[0])
        for j in range(i+1, X.shape[0]):
            inc[x] += 1
            x &= (X[i] > X[j])
        M[i] = inc
    M_global *= M

    # Rows up
    M = np.zeros_like(X)
    for i in reversed(range(X.shape[0])):
        x = (np.zeros_like(X[0]) == 0)
        inc = np.zeros_like(X[0])
        for j in reversed(range(i)):
            inc[x] += 1
            x &= (X[i] > X[j])
        M[i] = inc
    M_global *= M

    ##
    # Cols down
    M = np.zeros_like(X)
    for i in range(X.shape[1]):
        x = (np.zeros_like(X[0]) == 0)
        inc = np.zeros_like(X[0])
        for j in range(i + 1, X.shape[1]):
            inc[x] += 1
            x &= (X[:,i] > X[:,j])
        M[:,i] = inc
    M_global *= M

    # Cols up
    M = np.zeros_like(X)
    for i in reversed(range(X.shape[1])):
        x = (np.zeros_like(X[0]) == 0)
        inc = np.zeros_like(X[0])
        for j in reversed(range(i)):
            inc[x] += 1
            x &= (X[:,i] > X[:,j])
        M[:,i] = inc
    M_global *= M

    print("Solution day 8.2:\n", M_global.max())




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    day8_2()
