import cv2


img = cv2.imread('/Users/hzh/Desktop/WechatIMG77575.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 图像预处理：使用高斯模糊去噪
blur = cv2.GaussianBlur(gray, (5, 5), 0)

edges = cv2.Canny(blur, 50, 200)

contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)


rectangle_list = []
for contour in contours:
    area = cv2.contourArea(contour)

    if area > 240 * 43:
        x, y, w, h = cv2.boundingRect(contour)
        print(x, y, w, h)
        if [x, y, w, h] not in rectangle_list:
            rectangle_list.append([x, y, w, h])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 绘制矩形框
            center = (x + w // 2, y + h // 2)

rectangle_list_sort = sorted(rectangle_list, key=lambda x: (x[0], x[1]))
col_project = rectangle_list_sort[0][0]
col_year = rectangle_list_sort[len(rectangle_list_sort) // 2][0]
col_month = rectangle_list_sort[-1][0]

project_w, project_h = rectangle_list_sort[0][2], rectangle_list_sort[0][3]
year_w, year_h = rectangle_list_sort[-1][2] + 10, rectangle_list_sort[-1][3]

project_list = [rec for rec in rectangle_list_sort if rec[0] < col_project + 50]
year_list = [rec for rec in rectangle_list_sort if col_year - 50 < rec[0] < col_year + 50]
month_list = [rec for rec in rectangle_list_sort if col_month - 50 < rec[0] < col_month + 50]

length = max(len(project_list), len(year_list), len(month_list))
l_project, l_year, l_month = 0, 0, 0
n = 0
while l_project <= length and l_year <= length and l_month <= length:
    rec_project = project_list[l_project]
    rec_year = year_list[l_year]
    rec_month = month_list[l_month]
    min_y = min(rec_project[1], rec_year[1], rec_month[1])

    if min_y + 40 < rec_project[1]:  # 说明没有找到框，我们按照规律给他生成
        rec_project = [col_project, min_y, project_w, project_h]
    else:
        l_project += 1
    if min_y + 40 < rec_year[1]:  # 说明没有找到框，我们按照规律给他生成
        rec_year = [col_year, min_y, year_w, year_h]
    else:
        l_year += 1
    if min_y + 40 < rec_month[1]:  # 说明没有找到框，我们按照规律给他生成
        rec_month = [col_month, min_y, year_w, year_h]
    else:
        l_month += 1

    cv2.imwrite(f'/Users/hzh/Desktop/img/{n}_项目.jpg',
                img[rec_project[1]:rec_project[1] + rec_project[3], rec_project[0]:rec_project[0] + rec_project[2]])
    cv2.imwrite(f'/Users/hzh/Desktop/img/{n}_月.jpg',
                img[rec_month[1]:rec_month[1] + rec_month[3], rec_month[0]:rec_month[0] + rec_month[2]])
    cv2.imwrite(f'/Users/hzh/Desktop/img/{n}_年.jpg',
                img[rec_year[1]:rec_year[1] + rec_year[3], rec_year[0]:rec_year[0] + rec_year[2]])
    n += 1



