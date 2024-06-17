
def detection_file_lines_to_list(path):
    # open txt file lines to a list
    with open(path, errors='ignore',encoding='utf-8') as f:
        content = f.readlines()
    # remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    return content

def file_lines_to_list(path):
    # open txt file lines to a list
    with open(path, errors='ignore') as f:
        content = f.readlines()
    # remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    return content

# print(file_lines_to_list('D:/YOLO/yolov4-pytorch/input/ground-truth/tree_201_xh2_20200322081300.txt'))
print(detection_file_lines_to_list('D:/YOLO/yolov4-pytorch/input/detection-results/tree_202_xh6_20200324144100.txt'))