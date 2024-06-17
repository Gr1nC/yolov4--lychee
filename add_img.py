import cv2
import matplotlib.pyplot as plt
import numpy as np

# 加载图像
image = cv2.imread('img/tree_201_xh7_20210319064500.jpg')

# 调整亮度
bright_image = cv2.convertScaleAbs(image, alpha=1.2, beta=10)

# 应用滤镜
blurred_image = cv2.GaussianBlur(image, (15, 15), 0)

# 调整图像亮度和对比度
brightness = -50
contrast = 0.5
ni_image = np.clip(image * contrast + brightness, 0, 255).astype(np.uint8)


# 创建一个2x2的图像网格
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# 在网格中显示原图
axes[0, 0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
axes[0, 0].set_title('原图')

# 在网格中显示亮度调整后的图
axes[0, 1].imshow(cv2.cvtColor(bright_image, cv2.COLOR_BGR2RGB))
axes[0, 1].set_title('正光')

# 在网格中显示滤镜后的图
axes[1, 0].imshow(cv2.cvtColor(blurred_image, cv2.COLOR_BGR2RGB))
axes[1, 0].set_title('雾中')

# 在网格中显示滤镜后的图
axes[1, 1].imshow(cv2.cvtColor(ni_image, cv2.COLOR_BGR2RGB))
axes[1, 1].set_title('逆光')

# 调整图像网格之间的间距
plt.tight_layout()

# 显示图像
plt.show()
