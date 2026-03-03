import matplotlib
matplotlib.use('TkAgg')  # 确保使用支持交互的后端
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.font_manager import FontProperties

# 设置支持中文的字体
font_path = 'C:/Windows/Fonts/simhei.ttf'  # 黑体字体路径（Windows 系统）
font = FontProperties(fname=font_path, size=12)

# 定义图片路径
image_path = 'D:\\desktop\\课程设计\\campus_map.jpg'  # 图片路径

# 定义比例尺
scale = 0.165  # 比例尺（米/像素）

# 加载图片
try:
    img = mpimg.imread(image_path)
except FileNotFoundError:
    print(f"错误：文件 {image_path} 未找到，请检查路径是否正确！")
    exit()

# 获取图片的像素尺寸
img_height, img_width = img.shape[:2]

# 计算图片的实际宽度和高度（以米为单位）
actual_width = img_width * scale
actual_height = img_height * scale

# 显示图片，并设置坐标范围
plt.imshow(img, extent=[0, actual_width, 0, actual_height])
plt.title("请点击建筑的左下角和右上角来标注障碍物（按回车键结束）")

# 开启交互模式
plt.ion()

# 初始化障碍物列表
obstacles = []

# 获取多组坐标
while True:
    print("请点击建筑的左下角和右上角来标注障碍物（按回车键结束）")
    try:
        # 设置 timeout 参数，例如 60 秒
        points = plt.ginput(2, timeout=60)  # 获取两个点的坐标
        if len(points) != 2:
            print("错误：需要标注两个点来定义障碍物的左下角和右上角！")
            continue
    except Exception as e:
        print(f"获取用户输入时出错：{e}")
        break

    # 记录障碍物坐标
    x1, y1 = points[0]
    x2, y2 = points[1]
    obstacles.append(((x1, y1), (x2, y2)))

    # 询问用户是否继续
    response = input("是否继续标注障碍物？(y/n): ")
    if response.lower() != 'y':
        break

# 关闭交互模式
plt.ioff()

# 打印所有障碍物坐标
print("所有障碍物坐标：", obstacles)

# 显示图形窗口
plt.show()
