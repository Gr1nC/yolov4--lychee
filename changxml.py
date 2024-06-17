import os.path
import xml.dom.minidom

# 将"白色口罩、蓝色口罩、黑色口罩"都替换为："已佩戴口罩"
# path为需要替换标签的目标文件夹
path = 'D:\YOLO\yolov4-pytorch\VOCdevkit\VOC2007\Annotations'
files = os.listdir(path)  # 得到文件夹下所有文件名称
s = []
print('------------开始替换标签名称！--------------')
for xmlFile in files:  # 遍历原标签文件夹

    if not os.path.isdir(xmlFile):  # 判断是否是文件夹，不是文件夹才打开
        dom = xml.dom.minidom.parse(os.path.join(path, xmlFile))
        root = dom.documentElement
        #替换节点，除了name也可以替换为其他节点
        pathNode = root.getElementsByTagName('name')
        print(pathNode)
        print(len(pathNode))
        j = len(pathNode)
        for i in range(j):
            if pathNode[i].firstChild.data == "抽穗期" :#or pathNode[i].firstChild.data == "蓝色口罩"  :
                print("替换前的名称为：", pathNode[i].firstChild.data)
                pathNode[i].firstChild.data = "Abstraction period"
                print("i为:", i)
                print("替换后的名称为：", pathNode[i].firstChild.data)
                i = i + 1
                with open(os.path.join(path, xmlFile), 'w',encoding='utf8') as fh:
                    dom.writexml(fh)
print('------------标签名称替换成功！--------------')
