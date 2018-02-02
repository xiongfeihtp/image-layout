import cv2
org_path="./convert_image/test/juchao-1.jpeg"
img = cv2.imread(org_path,-1)
height,width=img.shape[0],img.shape[1]
compensation=5
x1=height-875-compensation
x2=height-696+compensation
y1=188-compensation
y2=702+compensation
crop_img = img[x1:x2,y1:y2]
cv2.imshow("image", crop_img)
cv2.waitKey(0)