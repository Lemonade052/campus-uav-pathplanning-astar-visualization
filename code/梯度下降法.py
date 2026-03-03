import numpy as np
# 定义 sigmoid 函数
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# 定义损失函数
def compute_loss(y, y_hat):
    m = len(y)
    return (-1 / m) * np.sum(y * np.log(y_hat) + (1 - y) * np.log(1 - y_hat))

# 梯度下降法实现逻辑回归
def gradient_descent(X, y, theta, alpha, iterations):
    m = len(y)
    loss_history = []

    for i in range(iterations):
        z = np.dot(X, theta)
        y_hat = sigmoid(z)
        loss = compute_loss(y, y_hat)
        loss_history.append(loss)

        gradient = (1 / m) * np.dot(X.T, (y_hat - y))
        theta = theta - alpha * gradient

    return theta, loss_history
# 数据预处理
# X 是特征矩阵，y 是标签向量
# 示例
X = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
y = np.array([0, 0, 1, 1])
X = np.hstack((np.ones((X.shape[0], 1)), X))

# 初始化参数
theta = np.zeros(X.shape[1])
alpha = 0.1
iterations = 1000

# 训练模型
theta, loss_history = gradient_descent(X, y, theta, alpha, iterations)

# 打印结果
print("训练后的参数:", theta)
print("损失函数历史:", loss_history)

