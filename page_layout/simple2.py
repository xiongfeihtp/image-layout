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
        filenames.sort(key=lambda x: int(re.findall('(\d*).jpg',x)[0]))
        for filename in filenames:
            print(filename)
            if fnmatch.fnmatch(filename, "*.jpg"):
                org_path = os.path.join(dirpath, filename)
                print("layout analysis {}".format(org_path))
                im = Image.open(org_path)  # the second one
                text = pytesseract.image_to_string(Image.open(org_path),lang="eng",
                                                   config="--psm 7 -c Recognize_choice=True -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
                # #纠错
                # for r in rep:
                #     text = text.replace(r, rep[r])
                print(text)
if __name__ == '__main__':
    root_path="./sampel2"
    execute(root_path)