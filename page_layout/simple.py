import pytesseract
from PIL import Image
import os
import os.path
import fnmatch
import re
#纠错
rep = {
       'F': '于',
       '人': '1',
       '竺': '等',
       '丢': '等',
       '入': '等',
       '74于':'7',
       '和': '等于'
       }
#计算
def calculate(text):
    list=text.split()
    num_first=int(list[0])
    #防止数组越界
    try:
        if list[3] in '0123456789':
            num_two=int(list[2]+list[3])
        else:
            num_two=int(list[2])
    except Exception as e:
        num_two=int(list[2])
    cal=list[1]
    if cal=='加':
        return num_first+num_two
    elif cal=='乘':
        return num_first*num_two
    elif cal=='除':
        return int(num_first/num_two)
    elif cal=='减':
        return num_first-num_two

def execute(root_path):
    #遍历验证码文件夹
    for dirpath, _, filenames in os.walk(root_path):
        med=filenames.copy()
        #去除隐藏文件
        for filename in med:
            if filename.startswith('.'):
                filenames.remove(filename)
        print(filenames)
        #图片格式为png
        filenames.sort(key=lambda x: int(re.findall('(\d*).png',x)[0]))
        for filename in filenames:
            print(filename)
            if fnmatch.fnmatch(filename, "*.png"):
                org_path = os.path.join(dirpath, filename)
                print("layout analysis {}".format(org_path))
                im = Image.open(org_path)  # the second one
                text = pytesseract.image_to_string(Image.open(org_path),lang="chi_sim_lstm",
                                                   config="--psm 7 -c Recognize_choice=True -c tessedit_char_whitelist=0123456789加减乘除等于")
                #纠错
                for r in rep:
                    text = text.replace(r, rep[r])
                print(text)
                print('cal result: {}'.format(calculate(text)))
if __name__ == '__main__':
    root_path="./sample"
    execute(root_path)