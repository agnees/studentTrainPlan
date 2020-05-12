from utils.query import query


def get_map_student():
    # {0:[白雪,12321],1:[xxx,1231]}
    map_student = {}

    # {12321: 0 ,1231:1}
    stuNo2MatNo = {}
    # 获取非admin 所有用户
    sql = "SELECT NAME, STU_NO FROM STUDENT WHERE STU_NO<>'admin'"
    result = query(sql)
    # 将查询结果从0开始编号
    map_student_id = 0
    for cur in result:
        # 把name,stu_no,变成数组命名为value
        values = list(cur)
        # 规定字典样式{map_stu_id:value}
        map_student[map_student_id] = values
        # map_student_id自增
        map_student_id = map_student_id + 1

    # {0: co_name}
    map_course = {}
    # 查找所有课程名
    sql = "SELECT CO_NAME FROM EDUCATION_PLAN "
    result = query(sql)
    # 从0开始编号
    map_course_id = 0
    for cur in result:
        # 建立字典样式{map_course_id: co_name}
        map_course[map_course_id] = cur[0]
        # map_course_id自增
        map_course_id = map_course_id + 1
    # 遍历map_student的长度，为idx
    for idx in range(len(map_student)):
        # 以idx为索引在map_student里面找到学生学号，生成字典{stu_no:idx}
        # {12321: 0 ,1231:1}
        stuNo2MatNo[map_student[idx][1]] = idx

    return map_student, map_course, stuNo2MatNo


def get_matrix(map_student):
    '''
    {0:[名字，学号]}
    '''
    # 生成30*118的矩阵，30人，每个人有118门课；每个元素代表每个人对这门课的评分
    comment_matrix = []
    pass_matrix = []
    for i in range(0, len(map_student)):
        comment_matrix.append([])
        pass_matrix.append([])
    for i in range(0, len(map_student)):
        # 在 map_student里面找到stu_no，作为[i]
        stu_no = map_student[i][1]
        # print(stu_no)
        # 用stu_no查找到评分
        sql = "SELECT COMMENT,PASS FROM CHOOSE a left join EDUCATION_PLAN  b on a.CO_NO=b.CO_NO  WHERE a.STU_NO='%s'" % (
            stu_no)
        # 查询结果用score定义
        score = query(sql)
        # print(score)
        for j in range(0, len(score)):
            # 将score作为[j]添加到矩阵，取第一列
            comment_matrix[i].append(int(score[j][0]))
            pass_matrix[i].append(score[j][1])

    return comment_matrix, pass_matrix


def get_count_by_choose_column(stu_no, column_name):
    '''

    :param stu_no: 学号
    :return:  容不容易过的课程，知识丰富都，课程趣味程度，新用户推荐不同
    '''

    # 在学生课程信息表，根据学号查询到课程序列finished_co
    sql = "select FINISHED_CO from EDU_STU_PLAN WHERE STU_NO='%s'" % stu_no
    plan = query(sql)
    finished_co = plan[0][0]
    # 在教学计划表中查询课程信息，用课程序列号co_100>0查询
    sql = "select CLASSIFICATION, START_TIME, CO_NAME, IS_MUST, CREDITS, CO_NO,AD_YEAR,CO_100,END_TIME,CLASS_TIME " \
          "from EDUCATION_PLAN WHERE CO_100>'%s'" % '0'
    # 查询结果用course表示
    courses = query(sql)

    courses2map = {}
    for course in courses:
        courses2map[course[5]] = {'co_name': course[2], 'choose': 0, 'is_must': int(course[3])}
        if finished_co[int(course[7]) - 1] == '1':
            courses2map[course[5]]['choose'] = 1

    sql = "SELECT CO_NO, sum(%s) as total FROM CHOOSE GROUP BY CO_NO order by total desc" % column_name

    results = query(sql)
    jsonData = {"source": []}
    for result in results:
        if len(jsonData) == 10:
            break
        if courses2map[result[0]].get('choose') == 0:
            continue
        if courses2map[result[0]].get('is_must') == 1:
            continue
        jsonData.get('source').append([int(result[1]), courses2map[result[0]].get('co_name')])

    return jsonData
