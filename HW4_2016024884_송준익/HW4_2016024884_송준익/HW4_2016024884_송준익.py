import numpy as np

A1 = np.matrix([ [(-2.9)*(-2.9), -2.9, 1], [(-2.1)*(-2.1), -2.1, 1], [(-0.9)*(-0.9), (-0.9), 1], [0.01, 0.1, 1], [1.21, 1.1, 1], [(1.9)*(1.9), 1.9, 1]])
B1 = np.matrix([[35.4], [19.7], [5.7], [1.2], [2.1], [8.7]])

A2 = np.matrix([ [(-2.9)*(-2.9), -2.9, 1], [(-2.1)*(-2.1), -2.1, 1], [(-0.9)*(-0.9), (-0.9), 1],  [(1.9)*(1.9), 1.9, 1], [3.1*3.1, 3.1, 1], [16.0, 4.0, 1]])
B2 = np.matrix([[35.4], [19.7], [5.7], [8.7], [25.7], [41.5]])


# d = np.linalg.pinv

x1 = np.linalg.pinv(A1) @ B1
x2 = np.linalg.pinv(A2) @ B2

print('x1 =\n',x1)

print('\nComparing x1')
y1 = A1@x1
print('\nB1 =\n', B1)
print('\nA1*x1 =\n', y1)
print('\nTrue Error =\n', B1-y1)
print('\nRelative Error (by Percentage) =\n', abs(((B1-y1)/B1)*100))

print('\nx2 =\n',x2)

print('\nComparing x2')
print('\nB2 = \n', B2)
y2 = A2@x2
print('\nA2*x2 = \n', y2)
print('\nTrue Error =\n', B2-y2)
print('\nRelative Error (by Percentage) =\n', abs(((B2-y2)/B2)*100))

