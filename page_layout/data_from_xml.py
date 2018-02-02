# 遍历某个文件夹下所有xml文件
import sys
import glob
import os
import lxml.etree as etree
def get_root(file_path):
    try:
        tree = etree.ElementTree(file=file_path)
        root = tree.getroot()
        return [root, tree]
    except Exception as e:
        print(file_path," can't parse!!")
        return None,None


def get_node(root, tag):
    node_list = []
    for node in root.iter(tag):
        node_list.append(node)
    return node_list


def traversalDir_XMLFile(path):
    # 判断路径是否存在
    if (os.path.exists(path)):
        # 得到该文件夹路径下下的所有xml文件路径
        f = glob.glob(path + '/*.xml')
        for file in f:
            print(file)
            root, tree = get_root(file)
            if root:
                node_list=get_node(root,'text')
                file_txt=os.path.split(file)[-1].replace('.xml','.txt')
                print(file_txt)
                path_txt='./txt_data/'+file_txt
                with open(path_txt, 'a') as f:
                    for node in node_list:
                        if node.text:
                            f.write(node.text)
            # 打开xml文档
path = '/Users/xiongfei/Downloads/平安科技图表项目/数据/reduce/年报xml'
traversalDir_XMLFile(path)
