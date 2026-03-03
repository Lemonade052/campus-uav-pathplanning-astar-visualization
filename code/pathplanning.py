import heapq
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

matplotlib.use('TkAgg')  # 确保使用支持交互的后端

# 定义一个节点类，用于A*算法
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = float('inf')  # 从起点到当前节点的实际代价
        self.h = 0  # 启发式代价（到终点的估计代价）
        self.f = float('inf')  # 总代价 f = g + h
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

# 检查经过区域是否为障碍物
def is_obstacle(x, y, obstacles):
    for obs in obstacles:
        (x1, y1), (x2, y2) = obs
        if x1 <= x <= x2 and y1 <= y <= y2:
            return True
    return False

# 计算启发式代价（欧几里得距离）
def heuristic(a, b):
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5

# A* 算法
def astar(start, goal, obstacles, grid_size):
    open_list = []
    start_node = Node(start[0], start[1])
    goal_node = Node(goal[0], goal[1])
    start_node.g = 0
    start_node.h = heuristic(start_node, goal_node)
    start_node.f = start_node.g + start_node.h
    heapq.heappush(open_list, start_node)

    closed_list = set()
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上下左右移动

    while open_list:
        current_node = heapq.heappop(open_list)
        if current_node.x == goal_node.x and current_node.y == goal_node.y:
            path = []
            while current_node:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            return path[::-1]

        closed_list.add((current_node.x, current_node.y))

        for dx, dy in neighbors:
            neighbor_x, neighbor_y = current_node.x + dx, current_node.y + dy
            if neighbor_x < 0 or neighbor_y < 0 or neighbor_x >= grid_size or neighbor_y >= grid_size:
                continue
            if (neighbor_x, neighbor_y) in closed_list or is_obstacle(neighbor_x, neighbor_y, obstacles):
                continue

            neighbor_node = Node(neighbor_x, neighbor_y)
            neighbor_node.g = current_node.g + 1
            neighbor_node.h = heuristic(neighbor_node, goal_node)
            neighbor_node.f = neighbor_node.g + neighbor_node.h
            neighbor_node.parent = current_node

            if not any(node.x == neighbor_node.x and node.y == neighbor_node.y for node in open_list):
                heapq.heappush(open_list, neighbor_node)

    return None  # 如果没有找到路径

# 能耗计算
def calculate_energy(path):
    if not path:
        return 0
    energy = 0
    for i in range(len(path) - 1):
        energy += ((path[i][0] - path[i + 1][0]) ** 2 + (path[i][1] - path[i + 1][1]) ** 2) ** 0.5
    return energy

# 可视化
def visualize(start, goal, obstacles, path, image_path, scale):

    # 加载图片
    img = mpimg.imread(image_path)
    fig, ax = plt.subplots()

    # 根据比例尺设置坐标范围
    actual_width = img.shape[1] * scale  # 图片的实际宽度（米）
    actual_height = img.shape[0] * scale  # 图片的实际高度（米）

    ax.imshow(img, extent=(0, actual_width, 0, actual_height))  # 设置图片的显示范围

    # 绘制障碍物
    for obs in obstacles:
        (x1, y1), (x2, y2) = obs
        rect = plt.Rectangle((x1, y1), (x2 - x1), (y2 - y1), color='red', alpha=0.5)
        ax.add_patch(rect)

    # 绘制起点和终点
    ax.plot(start[0], start[1], 'go', markersize=10, label='Start')  # 绿色起点
    ax.plot(goal[0], goal[1], 'bo', markersize=10, label='Goal')  # 蓝色终点

    # 绘制路径
    if path:
        path_x, path_y = zip(*[(x, y) for x, y in path])
        ax.plot(path_x, path_y, 'k--', label='Path')

    ax.legend()
    plt.show()

# 示例输入
start = (600, 300)  # 起点
goal = (300, 400)   # 终点
obstacles = [
    ((np.float64(120.82297619047617), np.float64(118.9552380952381)), (np.float64(182.35154761904758), np.float64(174.07458333333335))), ((np.float64(149.0235714285714), np.float64(35.63529761904765)), (np.float64(219.52505952380946), np.float64(92.03648809523811))), ((np.float64(104.15898809523807), np.float64(239.4486904761905)), (np.float64(169.53309523809517), np.float64(280.4677380952381))), ((np.float64(101.59529761904756), np.float64(304.8227976190476)), (np.float64(154.1509523809523), np.float64(344.56))), ((np.float64(64.42178571428568), np.float64(379.1698214285714)), (np.float64(79.80392857142854), np.float64(426.5980952380952))), ((np.float64(113.13190476190474), np.float64(395.8338095238095)), (np.float64(154.1509523809523), np.float64(444.5439285714285))), ((np.float64(257.98041666666666), np.float64(236.885)), (np.float64(351.555119047619), np.float64(276.6222023809524))), ((np.float64(365.6554166666666), np.float64(235.60315476190476)), (np.float64(428.4658333333333), np.float64(276.6222023809524))), ((np.float64(269.5170238095237), np.float64(358.66029761904764)), (np.float64(354.11880952380943), np.float64(384.2972023809524))), ((np.float64(365.6554166666666), np.float64(356.0966071428571)), (np.float64(415.6473809523809), np.float64(386.86089285714286))), ((np.float64(250.2893452380952), np.float64(420.18886904761905)), (np.float64(343.8640476190476), np.float64(517.6091071428572))), ((np.float64(481.02148809523806), np.float64(353.53291666666667)), (np.float64(547.6774404761904), np.float64(399.67934523809527))), ((np.float64(498.9673214285714), np.float64(242.01238095238097)), (np.float64(592.5420238095237), np.float64(290.7225))), ((np.float64(596.3875595238095), np.float64(317.64125)), (np.float64(656.6342857142856), np.float64(381.7335119047619))), ((np.float64(692.5259523809523), np.float64(463.7716071428572)), (np.float64(725.8539285714285), np.float64(522.7364880952381))), ((np.float64(692.5259523809523), np.float64(536.8367857142857)), (np.float64(741.2360714285713), np.float64(645.7936309523809))), ((np.float64(629.7155357142857), np.float64(638.1025595238095)), (np.float64(688.6804166666666), np.float64(679.1216071428571)))
]#障碍物区域坐标（已经过比例处理）
image_path = 'D:\\desktop\\uav-project\\results\\campus_map.jpg'  # 图片路径
scale = 0.165  # 比例尺

# 路径规划
img = mpimg.imread(image_path)
path = astar(start, goal, obstacles, grid_size = max(img.shape[1], img.shape[0]) * scale)#网格大小（判断路径是否有效）
if path:
    print("飞行路径：", path)
    energy = calculate_energy(path)
    print("总能耗：", energy)
    visualize(start, goal, obstacles, path, image_path, scale)
else:
    print("无法找到路径")