from flask import Flask, render_template, request, flash, jsonify, redirect, url_for, session
from utils import query, map_student_course, recommed_module
import json
import time
import os

# 创建flask对象，配置秘钥
app = Flask(__name__)
app.config['SECRET_KEY'] = 'gsolvit'


# 为首页绑定路由
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# 登录admin进入管理员界面配置路由，查询sql表显示学生信息
@app.route('/manager', methods=['GET', 'POST'])
def manager():
    sql = "select * from STUDENT"
    result = query.query(sql)
    return render_template('manager.html', result=result)


# 管理员添加学生页
@app.route('/managerAdd', methods=['GET', 'POST'])
def managerAdd():
    stu_id = session.get('stu_id')  # 获取登录网站时的stu_id
    # print(stu_id)
    if stu_id == 'admin':  # 验证是否为admin
        if request.method == 'GET':  # 获取信息，跳转html
            return render_template('managerAdd.html')
        else:
            # 获取添加的name\sex\stu_no\college\major\ad_year\password
            name = request.form.get('name')
            sex = request.form.get('sex')
            stu_no = request.form.get('stu_no')
            college = request.form.get('college')
            major = request.form.get('major')
            ad_year = request.form.get('ad_year')
            password = request.form.get('password')
            # 插入数据库student表中
            sql = "INSERT INTO STUDENT VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % (
                name, sex, stu_no, college, major, ad_year, password, stu_no)

            # 更新数据库
            query.update(sql)
            # 跳转到manager函数
            return redirect(url_for('manager'))
    else:
        return u'页面不存在'


# 管理员删除学生
@app.route('/managerDelete', methods=['GET', 'POST'])
def managerDelete():
    # 获取登录网站时的ID
    stu_id = session.get('stu_id')
    # 验证是否为管理员用户
    if stu_id == 'admin':
        # 获取信息跳转html
        if request.method == 'GET':
            return render_template('managerDelete.html')
        else:
            # 获取要删除的学生学号，用sql语句在数据库中删除
            stu_no = request.form.get('stu_no')
            sql = "DELETE FROM STUDENT WHERE STU_NO='%s'" % stu_no
            # 更新删除后的数据库，跳转到manager函数
            query.update(sql)
            return redirect(url_for('manager'))
    else:
        return u'页面不存在'


# 管理员编辑学生信息
@app.route('/managerEdit', methods=['GET', 'POST'])
def managerEdit():
    # 获取登录ID验证是否为admin
    stu_id = session.get('stu_id')
    if stu_id == 'admin':
        # 获取信息跳转html
        if request.method == 'GET':
            return render_template('managerEdit.html')

        else:
            # 从浏览器获取要编辑的学生学号，和修改的name,sex,college,major,ad_year,password
            stu_no = request.form.get('stu_no')
            name = request.form.get('name')
            sex = request.form.get('sex')
            college = request.form.get('college')
            major = request.form.get('major')
            ad_year = request.form.get('ad_year')
            password = request.form.get('password')
            # 根据学号查询数据表中被修改的学生
            sql = "select * from STUDENT WHERE STU_NO='%s'" % stu_no
            result = query.query(sql)
            # 将新的信息替换到原有的位置
            if name == '':
                name = result[0][0]
            if sex == '':
                sex = result[0][1]
            if college == '':
                college = result[0][3]
            if major == '':
                major = result[0][4]
            if ad_year == '':
                ad_year = result[0][5]
            # 更新在数据库，跳转回manager函数
            sql = "UPDATE STUDENT SET NAME = '%s', SEX = '%s', COLLEGE = '%s', MAJOR = '%s', AD_YEAR = '%s', PASSWORD = '%s', ID = '%s' WHERE STU_NO = '%s'" % (
                name, sex, college, major, ad_year, password, stu_no, stu_no)
            query.update(sql)
            return redirect(url_for('manager'))
    else:
        return u'页面不存在'


# 发布话题界面
@app.route('/course_discussion', methods=['GET', 'POST'])
def course_discussion():
    # 获取信息跳转html
    if request.method == 'GET':
        return render_template('course_discussion.html')
    else:
        # 获取发布话题topic/comments
        topic = request.form.get('topic')
        comments = request.form.get('comments')
        # commenter = request.form.get('commenter')
        # 获取登录stu_id，并在student表中查询该学生信息
        # 从session中get ID 有效防止冒名顶替
        stu_id = session.get('stu_id')
        # 在student表查找姓名
        sql = "select NAME from STUDENT where STU_NO = '%s'" % stu_id
        stu_name = query.query(sql)
        # 获取学生姓名
        stu_name = stu_name[0][0]
        # 获取当前时间
        now = time.time()
        now = time.strftime('%Y-%m-%d', time.localtime(now))
        now = str(now)
        # 生成news_id 学生姓名+时间 简单，能在列表上清晰看到 名字重复了怎么办？
        news_id = stu_name + now
        # 将new信息插入到news表
        sql = "INSERT INTO NEWS(TOPIC, COMMENTS, COMMENTER, CREATE_TIME, NEWS_ID,IS_FIRST)" \
              "VALUES ('%s', '%s', '%s','%s','%s','%s')" % (topic, comments, stu_name, now, news_id, 0)

        print(sql)
        # 后端更新数据表，并返回news_center函数
        query.update(sql)
        return render_template('news_center.html')


# 为登录界面登录绑定路由，以及设置打开浏览器的自动呈现界面
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    # 服务器端获取数据
    if request.method == 'GET':
        return render_template('login.html')
    else:
        # 获取浏览器端输入的账号密码
        stu_id = request.form.get('stu_id')
        password = request.form.get('password')
        # 用sql在student表查询
        sql = "select * from STUDENT where STU_NO = '%s'" % stu_id
        result = query.query(sql)
        print(result)
        # 如果查询结果长度不为0
        if len(result) != 0:
            # print(result[0][6], password)
            # 如果查询数据条的第7位和输入的password相等
            if result[0][6] == password:
                # 登录浏览器的stu_id session为查询结果数据条中第三位
                session['stu_id'] = result[0][2]
                # 保留31天
                session.permanent = True
                # 如果登录的stu_id是admin,跳转到manager方法
                if stu_id == 'admin':
                    return redirect(url_for('manager'))
                # 不是就跳转到首页index函数
                else:
                    return redirect(url_for('index'))
            # 和查询数据条中结果不一致
            else:
                return u'账号或密码错误'
        # 查询到的数据条长度为0
        else:
            return u'不存在这个用户'


# 修改密码路由绑定
@app.route('/register', methods=['GET', 'POST'])
def register():
    # 服务器获取数据，跳转网页
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # 获取填入的stu_id,user,password和password1
        stu_id = request.form.get('stu_id')
        user = request.form.get('user')
        password = request.form.get('password')
        password1 = request.form.get('password1')
        print(stu_id, user, password, password1)

        # 如果两次输入的密码一样，则提示密码不能一样
        if (password1 != password):
            return u'两次输入密码不同，请检查'
        else:
            # 在student表中查找到这个学生的信息
            sql = "select * from STUDENT where STU_NO = '%s'" % stu_id
            # print(sql)
            result = query.query(sql)
            # print(result)
            # 如果返回数据条长度为0
            if len(result) == 0:
                return u'没有这个用户了'
            else:
                # 如果数据条第7列原password和user相等，则更新数据库中的学号和密码
                if result[0][6] == user:
                    sql = "UPDATE STUDENT SET PASSWORD='%s' WHERE STU_NO='%s'" % (password, stu_id)
                    query.update(sql)
                    # 跳转回login函数
                    return redirect(url_for('login'))
                else:
                    return u'密码错误'


# 话题讨论首页路由
@app.route('/news_center', methods=['GET', 'POST'])
def news_center():
    if request.method == 'GET':
        return render_template('news_center.html')
    # 在news表查找is_first=0，也就是原创帖
    sql = "select * from NEWS WHERE IS_FIRST='0'"
    result = query.query(sql)
    print(result)
    return jsonify(result)


# 单个话题详情路由
@app.route('/detail/<question>', methods=['GET', 'POST'])
# 传入参数question
def detail(question):
    print(question)
    # question=str(question)
    # 服务器获取信息，因为要显示到话题详情，所以在news表查找topic,comments,commenter和create_time
    if request.method == 'GET':
        # 根据news_id和is_first=0查表，也就是原创帖，news_id就是question
        sql = "SELECT TOPIC, COMMENTS, COMMENTER, CREATE_TIME FROM NEWS WHERE NEWS_ID='%s' AND IS_FIRST='0'" % question
        title = query.query(sql)
        # print(title)
        # 标题为查到的这行数据条
        title = title[0]
        # 获取针对这个帖子的回复信息 is_first=question，关联具体的问题，question id在数据库自增
        sql = "SELECT * FROM NEWS WHERE IS_FIRST='%s'" % question
        result = query.query(sql)
        return render_template('detail.html', title=title, result=result)
    else:
        # 回复他人评论，获取评论和登录stu_id
        comments = request.form.get('comments')
        stu_id = session.get('stu_id')
        # 在student表查询该学生信息
        sql = "select NAME from STUDENT where STU_NO = '%s'" % stu_id
        # 根据查询数据条获取姓名
        stu_name = query.query(sql)
        stu_name = stu_name[0][0]
        # 获取当前时间
        now = time.time()
        now = time.strftime('%Y-%m-%d', time.localtime(now))
        now = str(now)
        # 合成这条new_id
        news_id = stu_name + now
        # 插入到news表,因为是针对这个帖子的回复，所以is_first = question,topic="回复"
        sql = "INSERT INTO NEWS(TOPIC, COMMENTS, COMMENTER, NEWS_ID, IS_FIRST) VALUES ('回复', '%s', '%s', '%s', '%s')" % (
            comments, stu_name, news_id, question)
        print(sql)
        query.update(sql)

        # 更新后再次显示原贴和这个帖子的回复的信息
        sql = "SELECT TOPIC, COMMENTS, COMMENTER, CREATE_TIME FROM NEWS WHERE NEWS_ID='%s' AND IS_FIRST='0'" % question
        title = query.query(sql)
        # 标题要显示查到的这一行
        title = title[0]
        sql = "SELECT * FROM NEWS WHERE IS_FIRST='%s'" % question
        result = query.query(sql)
        return render_template('detail.html', title=title, result=result)


# 课程推荐路由绑定
@app.route('/recommed', methods=['GET', 'POST'])
def recommed():
    return render_template('recommed.html')


@app.route("/getRecommedData", methods=['GET', 'POST'])
def getRecommedData():
    # 获取学号
    stu_no = session.get('stu_id')
    # {0:[白雪,12321],1:[xxx,1231]}；{0: co_name}；{12321: 0 ,1231:1}
    id2Student, id2Course, stuNo2MatId = map_student_course.get_map_student()
    # [[5.0，4.0][2.0,3.0]] 每个用户对课程的评分，行编号为学生编号，列为课程编号
    scoreMatrix, passMatrix = map_student_course.get_matrix(id2Student)
    """
    函数，recommedCourse：使用SVD进行课程推荐：
    入参： 学生对课程的评分矩阵，需要推荐的那个人的编号 推荐top20
    返回:(课程1ID， 课程1评分)
    """
    # 需要推荐的课程和人及评分
    topNCourse, _ = recommed_module.recommedCoursePerson(scoreMatrix, stuNo2MatId[stu_no], N=20)
    passTopNCourse, _ = recommed_module.recommedCoursePerson(passMatrix, stuNo2MatId[stu_no], N=10)
    """
    将得到的Course与Person装换为前端图标需要的json格式:
     {
        "source": [
            [2.3, "计算机视觉"],
            [1.1, "自然语言处理"],
            [2.4, "高等数学"],
            [3.1, "线性代数"],
            [4.7, "计算机网络"],
            [5.1, "离散数学"]
        ]
     }   
    """
    # 生成新字典{数字：姓名}
    # id2Student = {i: id2Student[i][0] for i in id2Student.keys()}
    # print(id2Student)
    # print(id2Course)
    # [评分：课程]
    courseJson = recommed_module.toBarJson(topNCourse, id2Course)
    # [评分：姓名]
    passTopNCourse = recommed_module.toBarJson(passTopNCourse, id2Course)
    courseJson = recommed_module.regularData(courseJson, 1, 5)
    passCourseJson = recommed_module.regularData(passTopNCourse, 1, 5)

    coursePersonJson = {}
    coursePersonJson['course'] = courseJson
    coursePersonJson['passCourse'] = passCourseJson
    print(coursePersonJson)
    return jsonify(coursePersonJson)


# 个人信息路由绑定
@app.route('/personal_information', methods=['GET', 'POST'])
def personal_information():
    """
    功能(个人中心界面): 根据"stu_id"从数据库中得到学生基本信息，用于个人中心信息显示
    :return:
    """
    # 从浏览器获取登录学号
    stu_no = session.get('stu_id')
    print(stu_no + ' is stu_no')
    # 在数据库查找这个学生
    sql = "SELECT * FROM STUDENT  WHERE STU_NO = '%s'" % stu_no
    result = query.query(sql)
    return render_template('personal_information.html', result=result)


@app.route('/train_plan', methods=['GET', 'POST'])
def train_plan():
    return render_template('train_plan.html')


@app.route('/get_info', methods=['GET', 'POST'])
def get_info():
    """
    功能(培养计划界面): 初始进入培养计划界面，根据stu_id从数据库中得到数据并将其转换为计划树所需json格式数据
    :return: planTree:(json) 计划树所需数据
    """
    # 获取stu_id后传入到query的getplantree方法中，转为json格式
    stu_id = session.get('stu_id')
    # planTree = query.getPlanTreeJson(stu_id)
    planTree = query.get_plan_tree(stu_id)
    print(planTree)
    return jsonify(planTree)


@app.route('/submit_train_plan', methods=['GET', 'POST'])
def submit_train_place():
    """
    功能1：实现数据库学生选课信息的更新
    功能2: 实现计划树以及进度条的提交更新。
    :return:
    """
    """功能1："""
    # 入参
    twoData = request.get_json(force=True)
    train_plan = {}
    if "tree" in twoData:
        train_plan = twoData['tree']

    scores = []
    if "scores" in twoData:
        scores = twoData['scores']

    # train_plan['name'] = "数据转换成功"
    print('反馈回来的数据是：')
    print(train_plan)
    # 从根节点找出孩子进行遍历
    # data = train_plan['children']
    # array_finish = [0] * 120
    # # print(array_finish)
    # # 遍历第二层里面的每一个孩子
    # for data_children in data:
    #     data_children = data_children['children']
    #     # print(data_children)
    #     # 对第三层遍历
    #     for data_children_child_1 in data_children:
    #         # print('data_children_child', data_children_child)
    #         data_children_child_1 = data_children_child_1['children']
    #         # 对第四层进行遍历
    #         for data_children_child in data_children_child_1:
    #             # 获取name,color
    #             name = data_children_child['children'][0]['name']
    #             color = data_children_child['children'][0]['itemStyle']['borderColor']
    #             # print(name, color)
    #             # 用name查找co_100
    #             sql = "select CO_100 from EDUCATION_PLAN WHERE CO_NAME='%s'" % name
    #             co_100 = query.query(sql)
    #             co_100 = co_100[0][0]
    #
    #             if color == 'red':
    #                 array_finish[int(co_100)] = 0
    #             else:
    #                 array_finish[int(co_100)] = 1
    # finish_co = ''
    # for i in range(1, 119):
    #     if array_finish[i] == 1:
    #         finish_co += '1'
    #     else:
    #         finish_co += '0'
    # print(finish_co)
    # print(array_finish)

    stu_id = session.get('stu_id')
    # stu_id = 2016012107
    # 更新选课计划
    query.updateDatabase(stu_id, train_plan)
    # 更新选课记录
    query.updateScore(stu_id, scores)

    """功能2："""
    train_plan_str = json.dumps(train_plan)
    # 告诉前端将已经选好的课更新为绿色
    train_plan_str = train_plan_str.replace("yellow", "green")
    train_plan = json.loads(train_plan_str)
    return jsonify(train_plan)


if __name__ == '__main__':
    app.run("0.0.0.0", debug=True)
