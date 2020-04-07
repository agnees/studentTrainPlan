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
    sql = "SELECT CO_NAME FROM EDUCATION_PLAN"
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
    matrix = []
    for i in range(30):
        matrix.append([])
    for i in range(30):
        # 在 map_student里面找到stu_no，作为[i]
        stu_no = map_student[i][1]
        #print(stu_no)
        # 用stu_no查找到评分
        sql = "SELECT COMMENT FROM CHOOSE WHERE STU_NO='%s'" % (stu_no)
        # 查询结果用score定义
        score = query(sql)
        #print(score)
        for j in range(118):
            # 将score作为[j]添加到矩阵，取第一列
            matrix[i].append(int(score[j][0]))

    return matrix

