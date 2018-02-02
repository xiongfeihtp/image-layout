import os
import fnmatch
import subprocess
def execute(root_path):
    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            if fnmatch.fnmatch(filename, u"*.pdf"):
                convert_dir="./convert_image/"+filename[:-4]
                if os.path.exists(convert_dir):
                    #os.rmdir(convert_dir)
                    os.system("rm -r {}".format(convert_dir))
                os.mkdir(convert_dir)
                org_path = os.path.join(dirpath, filename)
                png_path=convert_dir+"/"+filename.replace(".pdf", ".jpeg")
                print("convert {0} to {1}".format(org_path, png_path))
                #指令更多样
                if subprocess.call(["convert",
                                    "-verbose",
                                    #"-trim",
                                    "-density","150",
                                    #"-quality","100",
                                    #"-append",
                                    "-alpha","remove",
                                    #"-flatte",
                                    #"-sharpen","0x1.0",
                                    org_path,
                                    png_path]) != 0:
                    print("failed: {0}".format(org_path))
                #集成功能
                # convert_pdf_to_jpg(org_path,png_path)
if __name__ == '__main__':
    #root_path = input("target folder path> ")
    root_path="./target_pdf"
    execute(root_path)


