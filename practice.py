from flask import Flask, url_for, render_template, redirect, request, session
from utils import map_student_course, query, recommed_module, resource
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gsolvit'

def getPlanTreeJson(stu_id):
    """
    功能: 传入学生stu_id,然后利用stu_id从数据库查询得到该学生选课信息，再转换为计划树所需的json格式
    :param stu_id: 唯一标识学生的id号
    :return: 学生选课计划树Json数据
    """
    # 根据main.py从浏览器获取的学号查询课程号finished_co
    sql = "SELECT FINISHED_CO FROM STU_EDU_PLAN WHERE STU_NO = '%s'" % stu_id
    finished_co = query(sql)
    finished_co = [0][0]
    # 定义finished_co
# 建立父节点data，命名为总进度
    data = {}
    data['name'] = '总进度'
    children = []
# 建立第二层孩子结点children1~n，存放课程种类；并建立第三层孩子结点children1~n_list
    children1 = {}
    children1['name'] = '我'
    children1_list = []
    children2 = {}
    children2['name'] = '和'
    children2_list = []
    children3 = {}
    children3['name'] = '你'
    children3_list = []
    children4 = {}
    children4['name'] = '心'
    children4_list = []
    children5 = {}
    children5['name'] = '在'
    children5_list = []
    children6 = {}
    children6['name'] = '一'
    children6_list = []
    children7 = {}
    children7['name'] = '起'
    children7_list = []
    children8 = {}
    children8['name'] = '不'
    children8_list = []
    children9 = {}
    children9['name'] = '分'
    children9_list = []
    children10 = {}
    children10['name'] = '离'
    children10_list = []
    children11 = {}
    children11['name'] = '了'
    children11_list = []
    aid = 1


    # 遍历000000列表，起始位置是1，第二位是2

# 建立课程+时间序列add_time_list，共11门课， 4个年份，11*4=44
    add_time_list = []
    for j in range(44):
        add_time_list.append([])

    # 从CHOOSE表获取课程序列号和评分，用stu_id查找
    sql = "SELECT CO_NO,COMMENT FROM CHOOSE WHERE STU_NO = '%s'" % stu_id
    course2score = query.query(sql)
    cos2score = {}
    for cur in course2score:
        cos2score[course2score[0]]: course2score[1]

    # 对当前查到的课程进行遍历，生成字典{课程序列号：评分}


    # print(co2score)

    for co in finished_co:
        aid_str = str(aid)
        sql = "SELECT CLASSIFICATIN,CO_NO,IS_MUST,CO_NAME,CREDITS,START_TIME FROM EDUCATION_PLAN WHERE CO_100 = '%s'" \
              "% aid_str"
        co_name = query.query(sql)
        aid = aid + 1
        add_is_list = []
        add_curse = {}
        add_is = {}

        # 学分add_score是co_name数据条中的第5位，float浮点型
        add_score = float(co_name[0][4])
        # 如果课程还没有被选过，co=0
        if co == '0':
            add_curse['name'] = co_name[0][3]

            # 在add_curse 字典里加上课程名name, co_name数据条第三位
            add_curse['item_Style'] = {'borderColor': 'red'}
            # 加上颜色，红色代表没被选过
            add_curse['value'] = add_score
            # 加上学分value = add_score
            add_curse['score'] = int(cos2score(co_name[0][1]))

            if co_name[0][2] == 1:
                add_is['name'] = '必修'
            else:
                add_is['name'] = '选修'

            add_is_list.append(add_curse)
            add_is['children'] = add_is_list
        else:
            add_curse['name'] = co_name[0][3]

            # 在add_curse 字典里加上课程名name, co_name数据条第三位
            add_curse['item_Style'] = {'borderColor': 'green'}
            # 加上颜色，红色代表没被选过
            add_curse['value'] = add_score
            # 加上学分value = add_score
            add_curse['score'] = int(cos2score(co_name[0][1]))

            if co_name[0][2] == 1:
                add_is['name'] = '必修'
            else:
                add_is['name'] = '选修'
            add_is_list.append(add_curse)
            add_is['children'] = add_is_list


    co_time = str(co_name[0][5])
    if co_name[0][0] == '我':
        if co_time[3] == '6':
            add_time_list[0].append(add_is)
        if co_time[3] == '7':
            add_time_list[1].append(add_is)
        if co_time[3] == '8':
            add_time_list[2].append(add_is)
        if co_time[3] == '9':
            add_time_list[3].append(add_is)

    if co_name[0][0] == '和':
        if co_time[3] == '6':
            add_time_list[4].append(add_is)
        if co_time[3] == '7':
            add_time_list[5].append(add_is)
        if co_time[3] == '8':
            add_time_list[6].append(add_is)
        if co_time[3] == '9':
            add_time_list[7].append(add_is)
    if co_name[0][0] == '你':
        if co_time[3] == '6':
            add_time_list[8].append(add_is)
        if co_time[3] == '7':
            add_time_list[9].append(add_is)
        if co_time[3] == '8':
            add_time_list[10].append(add_is)
        if co_time[3] == '9':
            add_time_list[11].append(add_is)
    if co_name[0][0] == '心':
        if co_time[3] == '6':
            add_time_list[12].append(add_is)
        if co_time[3] == '7':
            add_time_list[13].append(add_is)
        if co_time[3] == '8':
            add_time_list[14].append(add_is)
        if co_time[3] == '9':
            add_time_list[15].append(add_is)

    if co_name[0][0] == '在':
        if co_time[3] == '6':
            add_time_list[16].append(add_is)
        if co_time[3] == '7':
            add_time_list[17].append(add_is)
        if co_time[3] == '8':
            add_time_list[18].append(add_is)
        if co_time[3] == '9':
            add_time_list[19].append(add_is)

    if co_name[0][0] == '一':
        if co_time[3] == '6':
            add_time_list[20].append(add_is)
        if co_time[3] == '7':
            add_time_list[21].append(add_is)
        if co_time[3] == '8':
            add_time_list[22].append(add_is)
        if co_time[3] == '9':
            add_time_list[23].append(add_is)

    if co_name[0][0] == '起':
        if co_time[3] == '6':
            add_time_list[24].append(add_is)
        if co_time[3] == '7':
            add_time_list[25].append(add_is)
        if co_time[3] == '8':
            add_time_list[26].append(add_is)
        if co_time[3] == '9':
            add_time_list[27].append(add_is)

    if co_name[0][0] == '不':
        if co_time[3] == '6':
            add_time_list[28].append(add_is)
        if co_time[3] == '7':
            add_time_list[29].append(add_is)
        if co_time[3] == '8':
            add_time_list[30].append(add_is)
        if co_time[3] == '9':
            add_time_list[31].append(add_is)

    if co_name[0][0] == '分':
        if co_time[3] == '6':
            add_time_list[32].append(add_is)
        if co_time[3] == '7':
            add_time_list[33].append(add_is)
        if co_time[3] == '8':
            add_time_list[34].append(add_is)
        if co_time[3] == '9':
            add_time_list[35].append(add_is)

    if co_name[0][0] == '离':
        if co_time[3] == '6':
            add_time_list[36].append(add_is)
        if co_time[3] == '7':
            add_time_list[37].append(add_is)
        if co_time[3] == '8':
            add_time_list[38].append(add_is)
        if co_time[3] == '9':
            add_time_list[39].append(add_is)

    if co_name[0][0] == '啊':
        if co_time[3] == '6':
            add_time_list[40].append(add_is)
        if co_time[3] == '7':
            add_time_list[41].append(add_is)
        if co_time[3] == '8':
            add_time_list[42].append(add_is)
        if co_time[3] == '9':
            add_time_list[43].append(add_is)

    # 创建add_time字典，设置姓名为2016-2019，children为add_time_list的43行
    add_time = {}
    add_time['name'] = '2016'
    add_time['children'] = add_time_list[0]
    children1_list.append(add_time)
    add_time = {}
    add_time['name'] = '2017'
    add_time['children'] = add_time_list[1]
    children1_list.append(add_time)
    add_time = {}
    add_time['name'] = '2018'
    add_time['children'] = add_time_list[2]
    children1_list.append(add_time)
    add_time = {}
    add_time['name'] = '2019'
    add_time['children'] = add_time_list[3]
    children1_list.append(add_time)

    add_time = {}
    add_time['name'] = '2016'
    add_time['children'] = add_time_list[4]
    children2_list.append(add_time)
    add_time = {}
    add_time['name'] = '2016'
    add_time['children'] = add_time_list[0]
    children2_list.append(add_time)
    add_time = {}
    add_time['name'] = '2016'
    add_time['children'] = add_time_list[0]
    children2_list.append(add_time)
    add_time = {}
    add_time['name'] = '2016'
    add_time['children'] = add_time_list[0]
    children2_list.append(add_time)

    add_time = {}
    add_time['name'] = '2016'
    add_time['children'] = add_time_list[0]
    children1_list.append(add_time)
    add_time = {}
    add_time['name'] = '2016'
    add_time['children'] = add_time_list[0]
    children1_list.append(add_time)
    add_time = {}
    add_time['name'] = '2016'
    add_time['children'] = add_time_list[0]
    children1_list.append(add_time)
    add_time = {}
    add_time['name'] = '2016'
    add_time['children'] = add_time_list[0]
    children1_list.append(add_time)

 # 对第二层结点，也就是每类课的学分规定要求
    children1['value'] = 10

# 把第三层子节点导入
    children1['children'] = children1_list

# 往父节点把所有的数据导入
    children.append(children1)



# 模拟选课调用的方法
def updateDatabase(stu_id, train_plan):
    """
    功能: 用户在“培养计划”界面点击“提交”按钮后，使用最新“计划树”信息更新数据库
    :param stu_id: 唯一标识学生的id
    :param train_plan: “培养计划”界面“计划树”数据的json格式
    :return: 无
    """
    data = train_plan['children']
    # 120门课
    array_finished = [0] * 120
    # print(array_finish)
    for data_children in data:
        data_children = data_children['children']
        for data_children_child1 in data_children:
            data_children_child1 = data_children_child1['children']
            for data_children_child in data_children_child1:
                name = data_children_child['children'][0]['name']
                color =data_children_child['children'][0]['itemStyle']
                sql = "SELECT CO_100 FROM EDUCATION_STU_PLAN WHERE STU_NO = '%s'" % stu_id
                co_100 = query(sql)
                co_100 = [0][0]

                if color == 'red':
                   array_finished[int(co_100)] == 0
                else:
                    array_finished[int(co_100)] == 1
    # 第2层遍历

        finished_co = ''
        for i in range(0,119):
            if array_finished[i] == 1:
                finished_co += '1'
            else:
                finished_co += '0'

        sql = "UPDATE STU_EDU_PLAN SET FINISHED_CO = '%s' WHERE STU_NO = '%s'" % (finished_co,stu_id)
        update(sql)
        # 第3层遍历

            # 第4层遍历

                # print(name, color)


                # 根据颜色设置01，红色未完成：0，绿色完成：1

    # 根据刚才生成的01，对应到finish_co字段

    # print(array_finish)
    # 更新finished_co


def updateScore(stu_id, scores):
    name2no = {}
    sql = "SELECT CO_NO,CO_NAME FROM EDUCATION_PLAN"
    result = query(sql)
    for cur in result:
        name2no[cur[1]]: cur[0]
    # 变成字典{co_name:co_no}
    for cur in scores:
        sql = "UPDATE STU_EDU_PLAN SET COMMENT = '%s' WHERE STU_NO = '%s' AND CO_NO = '%s'"\
              % (scores(cur), stu_id, name2no(cur))
        update(sql)

        # 更新选课表




















