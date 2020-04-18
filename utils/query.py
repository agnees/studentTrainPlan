import json

import pymysql
from config import config  # 配置模块


def query(sql):
    """
    功能; 使用sql语句查询数据库中学生选课信息.
    参数: sql(string)
    """
    db = pymysql.connect(config['MYSQL_HOST'], 'root', config['MYSQL_PASSWORD'], config['DATABASE_NAME'],
                         charset='utf8')
    cur = db.cursor()  # 使用cursor（）获取操作游标
    try:
        print(sql)
        cur.execute(sql)  # 执行sql语句
        result = cur.fetchall()  # 获取所有列表记录
        db.commit()  # 提交到数据库执行
        print('query success')
        return result

        # print('query success')
    except Exception as err:
        print(err.args)
        print('query loss')
        db.rollback()
    finally:
        cur.close()
        db.close()
    return


def update(sql):
    """ `
    功能; 使用sql语句更新数据库中学生选课信息。
    参数: sql(string)
    """
    db = pymysql.connect(config['MYSQL_HOST'], 'root', config['MYSQL_PASSWORD'], config['DATABASE_NAME'],
                         charset='utf8')
    cur = db.cursor()
    try:
        cur.execute(sql) # 执行sql语句
        db.commit() # 提交数据库执行
        # print('update success')
        # print('update success')
    except:
        # print('update loss')
        db.rollback()
    cur.close()
    db.close()


def get_plan_tree(stu_id):
    # 为课程大类设置学分
    calssfication_config = {'通识理论必修': 36, '通识理论选修（公选）': 8, '通识实践必修': 3, '实践选修': 6, '学科理论必修': 52.5, "学科实践必修": 6,
                            '专业理论必修': 24, '专业理论选修': 12, '专业实践必修': 22.5, '第二课堂': 12}
    """
    功能: 传入学生stu_id,然后利用stu_id从数据库查询得到该学生选课信息，再转换为计划树所需的json格式
    :param stud_id:
    :return: 学生选课计划树Json数据
    """
    # 在学生课程信息表，根据学号查询到课程序列finished_co
    sql = "select FINISHED_CO from EDU_STU_PLAN WHERE STU_NO='%s'" % stu_id
    result = query(sql)
    # 以finished_co表示查询结果
    finished_co = result[0][0]
    print(finished_co)

    # 从CHOOSE表获取课程编号co_no和评分comment，用学号查找
    sql = "SELECT CO_NO,COMMENT FROM CHOOSE WHERE STU_NO='%s'" % stu_id
    # 将查询结果定义为course2score
    course2score = query(sql)
    # 建立co2score字典
    co2score = {}
    # 对当前查到的课程在course2score进行遍历，结果填入字典co2score={课程编号：评分}
    for cur in course2score:
        co2score[cur[0]] = cur[1]

    # 在教学计划表中查询课程信息，用课程序列号co_100>0查询
    sql = "select CLASSIFICATION, START_TIME, CO_NAME, IS_MUST, CREDITS, CO_NO,AD_YEAR,CO_100 " \
          "from EDUCATION_PLAN WHERE CO_100>'%s'" % '0'
    # 查询结果用course表示
    courses = query(sql)

    co2course = {} # 存数据
    classfication_index = set()  # 建集合存大类
    ad_year_calssfaiction_index = {}  # key: 大类： value : 2016_大类
    ad_year_calssfaiction_is_must_index = {}  # key :2016_大类 value :选修_2016_大类
    ad_year_calssfaiction_is_must_data = {}
    # 遍历去重
    for course in courses:
        # 找出course(co_no) = course(co_no)
        co2course[course[5]] = course
        # 将classification字段添加在classification_index集合中
        classfication_index.add(course[0])

        # 如果有哪个classification不在字典ad_year_classification返回的keys中
        if course[0] not in ad_year_calssfaiction_index.keys():
            # 以classification为key创建集合ad_year_classification
            ad_year_calssfaiction_index[course[0]] = set()
            # 将(ad_year)_(classification)设置为value添加到集合
        ad_year_calssfaiction_index[course[0]].add('%s_%s' % (course[6], course[0]))

        # 如果(ad_year)_(classification)不在 ad_year_is_must_index字典的keys中
        if '%s_%s' % (course[6], course[0]) not in ad_year_calssfaiction_is_must_index.keys():
            # 建立集合 ad_year_is_must_index,以(ad_year)_(classification)为key
            ad_year_calssfaiction_is_must_index['%s_%s' % (course[6], course[0])] = set()
            # 将（is_must)_(ad_year)_(classification)设置为value添加到集合
        ad_year_calssfaiction_is_must_index['%s_%s' % (course[6], course[0])].add(
            '%s_%s_%s' % (course[3], course[6], course[0]))

        # 如果（is_must)_(ad_year)_(classification)不在ad_year_classifiction_is_must_data字典的keys中
        if '%s_%s_%s' % (course[3], course[6], course[0]) not in ad_year_calssfaiction_is_must_data.keys():
            # 创建包含所有(is_must)_(ad_year)_(classification)的列表
            ad_year_calssfaiction_is_must_data['%s_%s_%s' % (course[3], course[6], course[0])] = []

        # 处理data叶子节点,学分设置浮点型，评分设置整数型，颜色为红色
        course_data = {'name': course[2], 'value': float(course[4]), 'score': int(co2score[course[5]]),
                       'itemStyle': {'borderColor': 'red'}}

        # 如果课程序列finished_co(用co_100-1来遍历）=1
        if finished_co[int(course[7]) - 1] == '1':
            # 颜色变为绿色
            course_data['itemStyle'] = {'borderColor': 'green'}

        # 将course_data添加到ad_year_calssfaiction_is_must_data列表
        ad_year_calssfaiction_is_must_data['%s_%s_%s' % (course[3], course[6], course[0])].append(course_data)

    # 进行树的处理
    # 建立父节点和第二层子节点
    data = {}
    data['name'] = '总进度'
    childrens = []
    # 遍历拿到第二层所有节点，生成列表
    classfication_index = list(classfication_index)
    # 数组排序
    classfication_index.sort()

    # 遍历课程大类
    for classfication in classfication_index:
        # 在第二层子节点加入{课程大类：学分}
        children = {'name': classfication, 'value': calssfication_config[classfication]}

        # 建立第三层子节点
        third_childrens = []
        # 索引第三层节点，建立列表ad_year_calssfaiction_index，并排序
        adindexs = list(ad_year_calssfaiction_index[classfication])
        adindexs.sort()
        # 遍历adindexs
        for ad_year_calssfaiction in adindexs:
            print(ad_year_calssfaiction)
            # 填入第三层子节点，将(ad_year)_(classification)以_分开，取ad_year为名字
            third_children = {'name': ad_year_calssfaiction.split("_")[0]}


            # 建立第四层子节点
            fourth_childrens = []
            # 找第四层索引，直接遍历
            for must in ad_year_calssfaiction_is_must_index[ad_year_calssfaiction]:
                # 添加名字为选修
                name = "选修"
                # 如果以_分割后，第一位是1，那么名字为必修
                if must.split("_")[0] == "1":
                    name = "必修"
                # 填入第四层子结点，这只名字和孩子
                fourth_children = {'name': name, 'children': ad_year_calssfaiction_is_must_data[must]}
                # 添加到第四层，生成列表
                fourth_childrens.append(fourth_children)

            # 设置第三层子结点孩子
            third_children['children'] = fourth_childrens
            third_childrens.append(third_children)

        # 设置第二层子结点孩子
        children["children"] = third_childrens
        childrens.append(children)

    # 设置父节点孩子
    data["children"] = childrens

    return data


def getPlanTreeJson(stu_id):
    """
    功能: 传入学生stu_id,然后利用stu_id从数据库查询得到该学生选课信息，再转换为计划树所需的json格式
    :param stu_id: 唯一标识学生的id号
    :return: 学生选课计划树Json数据
    """
    # 根据main.py从浏览器获取的学号查询课程号finished_co
    print(stu_id)
    sql = "select FINISHED_CO from EDU_STU_PLAN WHERE STU_NO='%s'" % stu_id
    result = query(sql)
    print(result)
    # 定义finished_co
    finished_co = result[0][0]
    print(finished_co)

    # 建立父节点data，命名为总进度
    data = {}
    data['name'] = '总进度'
    children = []

    # 建立第二层孩子结点children1~n，存放课程种类；并建立第三层孩子结点children1~n_list
    children1 = {}
    children1['name'] = '思想政治理论'
    children1_list = []
    children2 = {}
    children2['name'] = '外语'
    children2_list = []
    children3 = {}
    children3['name'] = '文化素质教育必修'
    children3_list = []
    children4 = {}
    children4['name'] = '体育'
    children4_list = []
    children5 = {}
    children5['name'] = '军事'
    children5_list = []
    children6 = {}
    children6['name'] = '健康教育'
    children6_list = []
    children7 = {}
    children7['name'] = '数学'
    children7_list = []
    children8 = {}
    children8['name'] = '物理'
    children8_list = []
    children9 = {}
    children9['name'] = '计算机'
    children9_list = []
    children10 = {}
    children10['name'] = '学科基础'
    children10_list = []
    children11 = {}
    children11['name'] = '专业选修'
    children11_list = []
    # 遍历000000列表，起始位置是1，第二位是2
    aid = 1

    score = [0.0] * 15

    # 建立课程+时间序列add_time_list，共11门课， 4个年份，11*4=44
    add_time_list = []
    for j in range(44):
        add_time_list.append([])  # 在末尾添加新对象

    # 从CHOOSE表获取课程序列号和评分，用stu_id查找
    sql = "SELECT CO_NO,COMMENT FROM CHOOSE WHERE STU_NO='%s'" % stu_id
    # 将查询结果定义为course2score
    course2score = query(sql)
    co2score = {}
    # 对当前查到的课程在course2score进行遍历，生成字典{课程序列号：评分}
    for cur in course2score:
        co2score[cur[0]] = cur[1]

    # print(co2score)

    # 在finished_co中遍历co,co 就是finished_co中的每一位000111
    for co in finished_co:
        course_add = {}
        # aid_str就是构建aid字符串
        aid_str = str(aid)
        # 从educatin_plan表中以co_100=str(aid)为标准，查询课程信息
        # co_100是对所有课从1-100编号
        sql = "select CLASSIFICATION, START_TIME, CO_NAME, IS_MUST, CREDITS, CO_NO " \
              "from EDUCATION_PLAN WHERE CO_100='%s'" % aid_str
        # 查询到的数据条命名为co_name
        co_name = query(sql)
        # print('数据库查询结果')
        # print(co_name)
        aid = aid + 1
        add_is_list = []
        add_curse = {}
        add_is = {}

        # 学分add_score是co_name数据条中的第5位，float浮点型
        add_score = float(co_name[0][4])
        # 如果课程还没有被选过，co=0
        if co == '0':
            # 在add_curse 字典里加上课程名name, co_name数据条第三位
            add_curse['name'] = co_name[0][2]
            # 加上颜色，红色代表没被选过
            add_curse['itemStyle'] = {'borderColor': 'red'}
            # 加上学分value = add_score
            add_curse['value'] = add_score
            # 加上评分，根据co_name数据条获取co_number,然后在co2score{序号：评分}字典中获取评分
            add_curse['score'] = int(co2score[co_name[0][5]])

            # is_must判断，必修=1,选修=0，作为name加入到add_is字典中
            if co_name[0][3] == 1:
                add_is['name'] = '必修'
            else:
                add_is['name'] = '选修'

            # 将add_curse,添加到add_is_list的末尾
            add_is_list.append(add_curse)
            # todo
            # 将add_is_list设为add_is的孩子
            add_is['children'] = add_is_list
            # add_time['name'] = str(co_name[0][1])
            # add_time_list.append(add_is)
            # add_time['children'] = add_time_list
        else:
            # 选过的课，co = 1
            add_curse['name'] = co_name[0][2]
            # 表示为绿色
            add_curse['itemStyle'] = {'borderColor': 'green'}
            add_curse['value'] = add_score
            add_curse['score'] = int(co2score[co_name[0][5]])

            if co_name[0][3] == 1:
                add_is['name'] = '必修'
            else:
                add_is['name'] = '选修'

            # 将add_curse,添加到add_is_list的末尾
            add_is_list.append(add_curse)
            # 将add_is_list设为add_is的孩子
            add_is['children'] = add_is_list
            # add_time['name'] = str(co_name[0][1])
            # add_time_list.append(add_is)
            # add_time['children'] = add_time_list

        # 课程开始时间为co_time，6789代表年份
        str_co_time = str(co_name[0][1])
        # 如果classification是思想政治理论，通过co_name数据条判断
        if co_name[0][0] == '思想政治理论':
            # 如果当前是2016年,第三位是6
            if str_co_time[3] == '6':
                # 将add_is添加到add_time_list0~3里面
                add_time_list[0].append(add_is)
            if str_co_time[3] == '7':
                add_time_list[1].append(add_is)
            if str_co_time[3] == '8':
                add_time_list[2].append(add_is)
            if str_co_time[3] == '9':
                add_time_list[3].append(add_is)
        if co_name[0][0] == '外语':
            if str_co_time[3] == '6':
                add_time_list[4].append(add_is)
            if str_co_time[3] == '7':
                add_time_list[5].append(add_is)
            if str_co_time[3] == '8':
                add_time_list[6].append(add_is)
            if str_co_time[3] == '9':
                add_time_list[7].append(add_is)
        if co_name[0][0] == '文化素质教育必修':
            if str_co_time[3] == '6':
                add_time_list[8].append(add_is)
            if str_co_time[3] == '7':
                add_time_list[9].append(add_is)
            if str_co_time[3] == '8':
                add_time_list[10].append(add_is)
            if str_co_time[3] == '9':
                add_time_list[11].append(add_is)
        if co_name[0][0] == '体育':
            if str_co_time[3] == '6':
                add_time_list[12].append(add_is)
            if str_co_time[3] == '7':
                add_time_list[13].append(add_is)
            if str_co_time[3] == '8':
                add_time_list[14].append(add_is)
            if str_co_time[3] == '9':
                add_time_list[15].append(add_is)
        if co_name[0][0] == '军事':
            if str_co_time[3] == '6':
                add_time_list[16].append(add_is)
            if str_co_time[3] == '7':
                add_time_list[17].append(add_is)
            if str_co_time[3] == '8':
                add_time_list[18].append(add_is)
            if str_co_time[3] == '9':
                add_time_list[19].append(add_is)
        if co_name[0][0] == '健康教育':
            if str_co_time[3] == '6':
                add_time_list[20].append(add_is)
            if str_co_time[3] == '7':
                add_time_list[21].append(add_is)
            if str_co_time[3] == '8':
                add_time_list[22].append(add_is)
            if str_co_time[3] == '9':
                add_time_list[23].append(add_is)
        if co_name[0][0] == '数学':
            if str_co_time[3] == '6':
                add_time_list[24].append(add_is)
            if str_co_time[3] == '7':
                add_time_list[25].append(add_is)
            if str_co_time[3] == '8':
                add_time_list[26].append(add_is)
            if str_co_time[3] == '9':
                add_time_list[27].append(add_is)
        if co_name[0][0] == '物理':
            if str_co_time[3] == '6':
                add_time_list[28].append(add_is)
            if str_co_time[3] == '7':
                add_time_list[29].append(add_is)
            if str_co_time[3] == '8':
                add_time_list[30].append(add_is)
            if str_co_time[3] == '9':
                add_time_list[31].append(add_is)
        if co_name[0][0] == '计算机':
            if str_co_time[3] == '6':
                add_time_list[32].append(add_is)
            if str_co_time[3] == '7':
                add_time_list[33].append(add_is)
            if str_co_time[3] == '8':
                add_time_list[34].append(add_is)
            if str_co_time[3] == '9':
                add_time_list[35].append(add_is)
        if co_name[0][0] == '学科基础':
            if str_co_time[3] == '6':
                add_time_list[36].append(add_is)
            if str_co_time[3] == '7':
                add_time_list[37].append(add_is)
            if str_co_time[3] == '8':
                add_time_list[38].append(add_is)
            if str_co_time[3] == '9':
                add_time_list[39].append(add_is)
        if co_name[0][0] == '专业选修':
            if str_co_time[3] == '6':
                add_time_list[40].append(add_is)
            if str_co_time[3] == '7':
                add_time_list[41].append(add_is)
            if str_co_time[3] == '8':
                add_time_list[42].append(add_is)
            if str_co_time[3] == '9':
                add_time_list[43].append(add_is)

    # 创建add_time字典，设置姓名为2016-2019，children为add_time_list的43行
    add_time = {}
    add_time['name'] = '2016'
    add_time['children'] = add_time_list[0]
    # 将add_time接在children1-n_list中，每四年占一个chilidren_list
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
    add_time['name'] = '2017'
    add_time['children'] = add_time_list[5]
    children2_list.append(add_time)
    add_time = {}
    add_time['name'] = '2018'
    add_time['children'] = add_time_list[6]
    children2_list.append(add_time)
    add_time = {}
    add_time['name'] = '2019'
    add_time['children'] = add_time_list[7]
    children2_list.append(add_time)

    add_time = {}
    add_time['name'] = '2016'
    add_time['children'] = add_time_list[8]
    children3_list.append(add_time)
    add_time = {}
    add_time['name'] = '2017'
    add_time['children'] = add_time_list[9]
    children3_list.append(add_time)
    add_time = {}
    add_time['name'] = '2018'
    add_time['children'] = add_time_list[10]
    children3_list.append(add_time)
    add_time = {}
    add_time['name'] = '2019'
    add_time['children'] = add_time_list[11]
    children3_list.append(add_time)

    add_time = {}
    add_time['name'] = '2016'
    add_time['children'] = add_time_list[12]
    children4_list.append(add_time)
    add_time = {}
    add_time['name'] = '2017'
    add_time['children'] = add_time_list[13]
    children4_list.append(add_time)
    add_time = {}
    add_time['name'] = '2018'
    add_time['children'] = add_time_list[14]
    children4_list.append(add_time)
    add_time = {}
    add_time['name'] = '2019'
    add_time['children'] = add_time_list[15]
    children4_list.append(add_time)

    add_time = {}
    add_time['name'] = '2016'
    add_time['children'] = add_time_list[16]
    children5_list.append(add_time)
    add_time = {}
    add_time['name'] = '2017'
    add_time['children'] = add_time_list[17]
    children5_list.append(add_time)
    add_time = {}
    add_time['name'] = '2018'
    add_time['children'] = add_time_list[18]
    children5_list.append(add_time)
    add_time = {}
    add_time['name'] = '2019'
    add_time['children'] = add_time_list[19]
    children5_list.append(add_time)

    add_time = {}
    add_time['name'] = '2016'
    add_time['children'] = add_time_list[20]
    children6_list.append(add_time)
    add_time = {}
    add_time['name'] = '2017'
    add_time['children'] = add_time_list[21]
    children6_list.append(add_time)
    add_time = {}
    add_time['name'] = '2018'
    add_time['children'] = add_time_list[22]
    children6_list.append(add_time)
    add_time = {}
    add_time['name'] = '2019'
    add_time['children'] = add_time_list[23]
    children6_list.append(add_time)

    add_time = {}
    add_time['name'] = '2016'
    add_time['children'] = add_time_list[24]
    children7_list.append(add_time)
    add_time = {}
    add_time['name'] = '2017'
    add_time['children'] = add_time_list[25]
    children7_list.append(add_time)
    add_time = {}
    add_time['name'] = '2018'
    add_time['children'] = add_time_list[26]
    children7_list.append(add_time)
    add_time = {}
    add_time['name'] = '2019'
    add_time['children'] = add_time_list[27]
    children7_list.append(add_time)

    add_time = {}
    add_time['name'] = '2016'
    add_time['children'] = add_time_list[28]
    children8_list.append(add_time)
    add_time = {}
    add_time['name'] = '2017'
    add_time['children'] = add_time_list[29]
    children8_list.append(add_time)
    add_time = {}
    add_time['name'] = '2018'
    add_time['children'] = add_time_list[30]
    children8_list.append(add_time)
    add_time = {}
    add_time['name'] = '2019'
    add_time['children'] = add_time_list[31]
    children8_list.append(add_time)

    add_time = {}
    add_time['name'] = '2016'
    add_time['children'] = add_time_list[32]
    children9_list.append(add_time)
    add_time = {}
    add_time['name'] = '2017'
    add_time['children'] = add_time_list[33]
    children9_list.append(add_time)
    add_time = {}
    add_time['name'] = '2018'
    add_time['children'] = add_time_list[34]
    children9_list.append(add_time)
    add_time = {}
    add_time['name'] = '2019'
    add_time['children'] = add_time_list[35]
    children9_list.append(add_time)

    add_time = {}
    add_time['name'] = '2016'
    add_time['children'] = add_time_list[36]
    children10_list.append(add_time)
    add_time = {}
    add_time['name'] = '2017'
    add_time['children'] = add_time_list[37]
    children10_list.append(add_time)
    add_time = {}
    add_time['name'] = '2018'
    add_time['children'] = add_time_list[38]
    children10_list.append(add_time)
    add_time = {}
    add_time['name'] = '2019'
    add_time['children'] = add_time_list[39]
    children10_list.append(add_time)

    add_time = {}
    add_time['name'] = '2016'
    add_time['children'] = add_time_list[40]
    children11_list.append(add_time)
    add_time = {}
    add_time['name'] = '2017'
    add_time['children'] = add_time_list[41]
    children11_list.append(add_time)
    add_time = {}
    add_time['name'] = '2018'
    add_time['children'] = add_time_list[42]
    children11_list.append(add_time)
    add_time = {}
    add_time['name'] = '2019'
    add_time['children'] = add_time_list[43]
    children11_list.append(add_time)

    # 对第二层结点，也就是每类课的学分规定要求
    children1['value'] = 16
    children2['value'] = 8
    children3['value'] = 5.5
    children4['value'] = 4
    children5['value'] = 5
    children6['value'] = 0.5
    children7['value'] = 21.5
    children8['value'] = 9
    children9['value'] = 4.0
    children10['value'] = 24.5
    children11['value'] = 21.5

    # 把第三层子节点导入作为第二层的children
    children1['children'] = children1_list
    children2['children'] = children2_list
    children3['children'] = children3_list
    children4['children'] = children4_list
    children5['children'] = children5_list
    children6['children'] = children6_list
    children7['children'] = children7_list
    children8['children'] = children8_list
    children9['children'] = children9_list
    children10['children'] = children10_list
    children11['children'] = children11_list

    # 往父节点把所有的数据导入children.append
    children.append(children1)
    children.append(children2)
    children.append(children3)
    children.append(children4)
    children.append(children5)
    children.append(children6)
    children.append(children7)
    children.append(children8)
    children.append(children9)
    children.append(children10)
    children.append(children11)
    data['children'] = children
    return data


# 模拟选课调用的方法
def updateDatabase(stu_id, train_plan):
    """
    功能: 用户在“培养计划”界面点击“提交”按钮后，使用最新“计划树”信息更新数据库
    :param stu_id: 唯一标识学生的id
    :param train_plan: “培养计划”界面“计划树”数据的json格式
    :return: 无
    """

    if len(train_plan) <= 0:
        return

    sql = "select CO_100,co_name from EDUCATION_PLAN WHERE CO_100 >='0'"
    results = query(sql)
    coname2co = {}
    for result in results:
        coname2co[result[1]] = result[0]

    data = train_plan['children']
    if len(data) <= 0:
        return

    # 120门课
    array_finish = [0] * len(results)
    # print(array_finish)
    # 第2层遍历
    for data_children in data:
        data_childrens = data_children['children']
        # print(data_children)
        # 第3层遍历
        for data_children_child_1 in data_childrens:
            # print('data_children_child', data_children_child)
            data_children_child_1s = data_children_child_1['children']
            # 第4层遍历
            for data_children_child in data_children_child_1s:
                data_childs = data_children_child['children']

                for child in data_childs:
                    name = child['name']
                    color = child['itemStyle']['borderColor']
                    # print(name, color)
                    co_100 = coname2co[name]
    `
                    # 根据颜色设置01，红色未完成：0，绿色完成：1
                    if color == 'red':
                        array_finish[int(co_100) - 1] = 0
                    else:
                        print("-----")
                        print(name)
                        array_finish[int(co_100) - 1] = 1
    # 根据刚才生成的01，对应到finish_co字段
    finish_co = ''
    for i in range(0, len(array_finish)):
        if array_finish[i] == 1:
            finish_co += '1'
        else:
            finish_co += '0'
    print(finish_co)
    # print(array_finish)
    # 更新finished_co
    sql = "UPDATE EDU_STU_PLAN SET FINISHED_CO='%s' WHERE STU_NO='%s'" % (finish_co, stu_id)
    update(sql)


def updateScore(stu_id, scores):
    sql = "SELECT CO_NO, CO_NAME FROM EDUCATION_PLAN"
    # 变成字典{co_name:co_no}
    name2no = {}
    result = query(sql)
    for cur in result:
        name2no[cur[1]] = cur[0]

    for cur in scores:
        # 更新选课表
        sql = "UPDATE CHOOSE SET COMMENT='%d' and PASS='%d' WHERE STU_NO='%s' AND CO_NO='%s'" % (
            scores[cur].get('score'), scores[cur].get('pass'), stu_id, name2no[cur])
        # print(sql)
        update(sql)


if __name__ == '__main__':
    config['DATABASE_NAME'] = "studenttrainplan2"
    print(json.dumps(get_plan_tree(2016012107)))

    # arrarys = [0, 1, 3, 4, 5]
    # for i in range(0, len(arrarys)):
    #     print(arrarys[i])
