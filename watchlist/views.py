from datetime import datetime

from flask import flash, url_for, render_template, redirect, request
from flask_login import login_required, login_user, logout_user

from watchlist import app
from watchlist.models import MovieActorRelation, MovieInfo, MovieBox, ActorInfo, User
from watchlist import db
from watchlist.untils import query_all_data, _convert_data_format_act_relation


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.filter(User.username == username).first()
        if user is None:
            flash('用户不存在')  # 如果验证失败，显示错误消息
            return redirect(url_for('login'))  # 重定向回登录页面

        print(user.password_hash)
        print(password)
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            return redirect(url_for('index'))  # 重定向到主页

        flash('Invalid username or password.')  # 如果验证失败，显示错误消息
        return redirect(url_for('login'))  # 重定向回登录页面

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name0']
        username = request.form['username']
        password = request.form['password']

        # 检查用户名是否已存在
        # Admin 用户已经存在了，使用其他用户名
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please choose a different username.")
            return render_template('register.html', )

        # 创建新用户

        new_user = User(name=name, username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash(f"User {username} registered successfully!")
        return redirect(url_for('index'))

    return render_template('register.html', )


@app.route('/logout')
@login_required  # 用于视图保护，后面会详细介绍
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index'))  # 重定向回首页


@app.route('/', methods=['GET', 'POST'])
def index():
    # 新增相关的代码
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        movie_id = request.form.get('movie_id')
        movie_name = request.form.get('movie_name')  # 传入表单对应输入字段的 name 值
        release_date = request.form.get('release_date')
        country = request.form.get('country')  # 传入表单对应输入字段的 name 值
        movie_type = request.form.get('movie_type')
        year = request.form.get('year')  # 传入表单对应输入字段的 name 值

        box = request.form.get('box')

        # 获取到的文件会是数组文件
        actors = request.form.getlist('actors')
        relations = request.form.getlist('relations')
        genders = request.form.getlist('genders')
        act_country = request.form.getlist('act_country')
        # ['张三丰', '张思枫', '张士大夫']
        # ['演员', '演员', '导演']
        print(actors)
        print(relations)

        # 验证数据
        if not movie_name or not year or len(year) > 4 or len(movie_name) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        # 保存表单数据到数据库
        # 1.插入电影表
        movie = MovieInfo(movie_id=movie_id,
                          movie_name=movie_name,
                          release_date=datetime(int(release_date[0:4]), int(release_date[5: 7]), int(release_date[8:])),
                          country=country,
                          movie_type=movie_type,
                          year=year
                          )
        db.session.add(movie)  # 添加到数据库会话
        # 2. 演员表不用插入

        # 3. 插入票房和电影关系表
        movie_box = MovieBox(movie_id=movie_id,
                             box=box)
        db.session.add(movie_box)

        # 4. 插入演员和电影关系表
        # actor_id
        # actor = ActorInfo.query.filter(ActorInfo.actor_name == actor_name).first()
        # print(actor)
        # 处理新旧演员
        for i in range(len(actors)):
            actor = ActorInfo.query.filter(ActorInfo.actor_name == actors[i]).first()
            # 如果演员不存在
            if actor is None:
                actor_0 = ActorInfo.query.all()
                last_actor_0_id = str(int(actor_0[-1].actor_id) + 1)

                actor_info = ActorInfo(actor_id=last_actor_0_id,
                                       actor_name=actors[i],
                                       gender=genders[i],
                                       country=act_country[i]
                                       )
                db.session.add(actor_info)

            actor_0 = ActorInfo.query.all()
            actor_0_id = str(int(actor_0[-1].actor_id))

            # 插入演员 id 到 演员-电影关联表
            movice_act_relas = MovieActorRelation.query.all()
            last_movice_act_rela_id = str(int(movice_act_relas[-1].id) + 1)
            movie_actor_rela = MovieActorRelation(id=last_movice_act_rela_id,
                                                  movie_id=movie_id,
                                                  actor_id=actor_0_id,
                                                  relation_type=relations[i])
            db.session.add(movie_actor_rela)

        db.session.commit()  # 提交数据库会话
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页

    # 展示相关的代码

    movies = MovieInfo.query.all()
    last_movies_id = str(int(movies[-1].movie_id) + 1)
    actors = ActorInfo().query.all()
    # 多表联查并按照box从高到低排序
    new_combined_data = query_all_data()

    return render_template('index.html', movies=movies, last_movies_id=last_movies_id, actors=actors,
                           new_combined_data=new_combined_data)


@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        search_type = request.form['searchType']
        search_input = request.form['searchInput']

        # 多表联查并按照box从高到低排序
        new_combined_data = query_all_data()
        res = []

        aaaaa = {'movie_id': '1016', 'movie_name': '你好，李焕英2', 'release_date': '2022-02-13', 'country': '冰岛',
                 'type': '喜剧2', 'year': 2022, 'box': 60.0, 'actors': [
                {'actor_id': '2035', 'actor_name': '贾玲', 'gender': '女', 'act_country': '中国',
                 'relations': [{'id': '42', 'relation_type': '导演1'}, {'id': '43', 'relation_type': '主演2'}]},
                {'actor_id': '2036', 'actor_name': '张小斐', 'gender': '女', 'act_country': '中国',
                 'relations': [{'id': '44', 'relation_type': '主演3'}]},
                {'actor_id': '2022', 'actor_name': '沈腾', 'gender': '男', 'act_country': '中国',
                 'relations': [{'id': '45', 'relation_type': '主演4'}]}]}
        # 可以扩充成其他类型过滤
        if search_type == "movieName":
            for data in new_combined_data:
                if data["movie_name"].find(search_input) != -1:
                    res.append(data)
        else:
            for data in new_combined_data:
                for actor in data["actors"]:
                    if actor["actor_name"].find(search_input) != -1:
                        res.append(data)

        movies = MovieInfo.query.all()
        last_movies_id = str(int(movies[-1].movie_id) + 1)
        actors = ActorInfo().query.all()

        return render_template('index.html', last_movies_id=last_movies_id, actors=actors,
                               new_combined_data=res)


@app.route('/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = MovieInfo.query.get_or_404(movie_id)  # 根据 movie_id 获取电影信息，如果不存在则返回 404 错误
    if request.method == 'POST':
        # 获取表单数据
        movie_name = request.form.get('movie_name')
        release_date = request.form.get('release_date')
        country = request.form.get('country')
        movie_type = request.form.get('movie_type')
        year = request.form.get('year')

        relation_type = request.form.getlist("relation_type[]")
        box = request.form.get('box')
        actor_id = request.form.getlist('actor_id[]')
        actor_names = request.form.getlist('actor_name[]')
        genders = request.form.getlist('gender')
        act_relation = _convert_data_format_act_relation(actor_names=actor_names, actor_id=actor_id,
                                                         relation_type=relation_type, genders=genders)
        print("演员 id 和关系")

        print(act_relation)

        # 验证数据
        if not movie_name or not year or len(year) > 4 or len(movie_name) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))

        # 验证数据，看看演员名 有没有重复的
        for i in range(len(act_relation)):
            actor_name = act_relation[i]["actor_name"]
            print(act_relation[i])
            print(act_relation[i]["actor_id"][0])
            actor_info = ActorInfo.query.filter(ActorInfo.actor_id == act_relation[i]["actor_id"][0]).first()
            actor_check = ActorInfo.query.filter(ActorInfo.actor_name == actor_name).first()
            ActorInfo.query.filter(ActorInfo.actor_id == actor_name).first()
            if actor_check is not None and actor_check.actor_id != actor_info.actor_id:
                flash('演员名字已经存在，请更改其他名字')
                return redirect(url_for('edit', movie_id=movie_id))

        # 更新演员信息
        for i in range(len(act_relation)):
            actor_name = act_relation[i]["actor_name"]
            gender = act_relation[i]["gender"]
            actor_info = ActorInfo.query.filter(ActorInfo.actor_id == act_relation[i]["actor_id"][0]).first()
            actor_info.actor_name = actor_name
            actor_info.gender = gender

        # 更新电影信息
        movie.movie_name = movie_name
        movie.release_date = datetime(int(release_date[0:4]), int(release_date[5: 7]), int(release_date[8:]))
        movie.country = country
        movie.movie_type = movie_type
        movie.year = year
        db.session.commit()

        # # 更新演员和关系(不能更新演员，只能更新关系)
        for i in range(len(act_relation)):

            relation_types = act_relation[i]["relation_type"]
            mov_act_relas = MovieActorRelation.query.filter_by(movie_id=movie_id,
                                                               actor_id=act_relation[i]["actor_id"][0]).all()

            for j in range(len(relation_types)):
                mov_act_relas[j].relation_type = relation_types[j]

        # # 更新票房
        movie_box = MovieBox.query.filter_by(movie_id=movie_id).first()
        movie_box.box = box
        #
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))

    new_combined_data = query_all_data()
    target = {}
    for i in new_combined_data:
        if i["movie_id"] == str(movie_id):
            target = i

    return render_template('edit.html', combined_data=target)


@app.route('/movie/detail_info/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def detail_info(movie_id):
    new_combined_data = query_all_data()
    target = {}
    for i in new_combined_data:
        if i["movie_id"] == str(movie_id):
            target = i
    return render_template('detail.html', combined_data=target)  # 传入被编辑的电影记录


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
@login_required
def delete(movie_id):
    # 1. 删除电影表
    movie = MovieInfo.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    #  2. 删除票房表
    movie_box = MovieBox.query.get_or_404(movie_id)
    db.session.delete(movie_box)

    #  3. 删除演员和电影关系表
    move_box_datas = MovieActorRelation.query.filter(MovieActorRelation.movie_id == movie_id)
    for move_box_data in move_box_datas:
        db.session.delete(move_box_data)

    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页
