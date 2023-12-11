# 1. 创建数据库
from datetime import datetime

import click
from flask import redirect, url_for

from watchlist import app
from watchlist.models import MovieActorRelation, ActorInfo, MovieBox, MovieInfo, User
from watchlist import db

movie_info_data = [
    {'movie_id': '1001', 'movie_name': '战狼2', 'release_date': '2017-07-27', 'country': '中国', 'movie_type': '战争',
     'year': 2017},
    {'movie_id': '1002', 'movie_name': '哪吒之魔童降世', 'release_date': '2019-07-26', 'country': '中国',
     'movie_type': '动画', 'year': 2019},
    {'movie_id': '1003', 'movie_name': '流浪地球', 'release_date': '2019-02-05', 'country': '中国',
     'movie_type': '科幻', 'year': 2019},
    {'movie_id': '1004', 'movie_name': '复仇者联盟4', 'release_date': '2019-04-24', 'country': '美国',
     'movie_type': '科幻', 'year': 2019},
    {'movie_id': '1005', 'movie_name': '红海行动', 'release_date': '2018-02-16', 'country': '中国',
     'movie_type': '战争', 'year': 2018},
    {'movie_id': '1006', 'movie_name': '唐人街探案2', 'release_date': '2018-02-16', 'country': '中国',
     'movie_type': '喜剧', 'year': 2018},
    {'movie_id': '1007', 'movie_name': '我不是药神', 'release_date': '2018-07-05', 'country': '中国',
     'movie_type': '喜剧', 'year': 2018},
    {'movie_id': '1008', 'movie_name': '中国机长', 'release_date': '2019-09-30', 'country': '中国',
     'movie_type': '剧情', 'year': 2019},
    {'movie_id': '1009', 'movie_name': '速度与激情8', 'release_date': '2017-04-14', 'country': '美国',
     'movie_type': '动作', 'year': 2017},
    {'movie_id': '1010', 'movie_name': '西虹市首富', 'release_date': '2018-07-27', 'country': '中国',
     'movie_type': '喜剧', 'year': 2018},
    {'movie_id': '1011', 'movie_name': '复仇者联盟3', 'release_date': '2018-05-11', 'country': '美国',
     'movie_type': '科幻', 'year': 2018},
    {'movie_id': '1012', 'movie_name': '捉妖记2', 'release_date': '2018-02-16', 'country': '中国', 'movie_type': '喜剧',
     'year': 2018},
    {'movie_id': '1013', 'movie_name': '八佰', 'release_date': '2020-08-21', 'country': '中国', 'movie_type': '战争',
     'year': 2020},
    {'movie_id': '1014', 'movie_name': '姜子牙', 'release_date': '2020-10-01', 'country': '中国', 'movie_type': '动画',
     'year': 2020},
    {'movie_id': '1015', 'movie_name': '我和我的家乡', 'release_date': '2020-10-01', 'country': '中国',
     'movie_type': '剧情', 'year': 2020},
    {'movie_id': '1016', 'movie_name': '你好，李焕英', 'release_date': '2021-02-12', 'country': '中国',
     'movie_type': '喜剧', 'year': 2021},
    {'movie_id': '1017', 'movie_name': '长津湖', 'release_date': '2021-09-30', 'country': '中国', 'movie_type': '战争',
     'year': 2021},
    {'movie_id': '1018', 'movie_name': '速度与激情9', 'release_date': '2021-05-21', 'country': '中国',
     'movie_type': '动作', 'year': 2021}]

move_box_data = [
    {'movie_id': '1001', 'box_office': 56.84},
    {'movie_id': '1002', 'box_office': 50.15},
    {'movie_id': '1003', 'box_office': 46.86},
    {'movie_id': '1004', 'box_office': 42.5},
    {'movie_id': '1005', 'box_office': 36.5},
    {'movie_id': '1006', 'box_office': 33.97},
    {'movie_id': '1007', 'box_office': 31},
    {'movie_id': '1008', 'box_office': 29.12},
    {'movie_id': '1009', 'box_office': 26.7},
    {'movie_id': '1010', 'box_office': 25.47},
    {'movie_id': '1011', 'box_office': 23.9},
    {'movie_id': '1012', 'box_office': 22.37},
    {'movie_id': '1013', 'box_office': 30.10},
    {'movie_id': '1014', 'box_office': 16.02},
    {'movie_id': '1015', 'box_office': 28.29},
    {'movie_id': '1016', 'box_office': 54.13},
    {'movie_id': '1017', 'box_office': 53.48},
    {'movie_id': '1018', 'box_office': 13.92}
]

actor_info_data = [
    {'actor_id': '2001', 'actor_name': '吴京', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2002', 'actor_name': '饺子', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2003', 'actor_name': '屈楚萧', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2004', 'actor_name': '郭帆', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2005', 'actor_name': '乔罗素', 'gender': '男', 'nationality': '美国'},
    {'actor_id': '2006', 'actor_name': '小罗伯特·唐尼', 'gender': '男', 'nationality': '美国'},
    {'actor_id': '2007', 'actor_name': '克里斯·埃文斯', 'gender': '男', 'nationality': '美国'},
    {'actor_id': '2008', 'actor_name': '林超贤', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2009', 'actor_name': '张译', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2010', 'actor_name': '黄景瑜', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2011', 'actor_name': '陈思诚', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2012', 'actor_name': '王宝强', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2013', 'actor_name': '刘昊然', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2014', 'actor_name': '文牧野', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2015', 'actor_name': '徐峥', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2016', 'actor_name': '刘伟强', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2017', 'actor_name': '张涵予', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2018', 'actor_name': 'F·加里·格雷', 'gender': '男', 'nationality': '美国'},
    {'actor_id': '2019', 'actor_name': '范·迪塞尔', 'gender': '男', 'nationality': '美国'},
    {'actor_id': '2020', 'actor_name': '杰森·斯坦森', 'gender': '男', 'nationality': '美国'},
    {'actor_id': '2021', 'actor_name': '闫非', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2022', 'actor_name': '沈腾', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2023', 'actor_name': '安东尼·罗素', 'gender': '男', 'nationality': '美国'},
    {'actor_id': '2024', 'actor_name': '克里斯·海姆斯沃斯', 'gender': '男', 'nationality': '美国'},
    {'actor_id': '2025', 'actor_name': '许诚毅', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2026', 'actor_name': '梁朝伟', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2027', 'actor_name': '白百何', 'gender': '女', 'nationality': '中国'},
    {'actor_id': '2028', 'actor_name': '井柏然', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2029', 'actor_name': '管虎', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2030', 'actor_name': '王千源', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2031', 'actor_name': '姜武', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2032', 'actor_name': '宁浩', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2033', 'actor_name': '葛优', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2034', 'actor_name': '范伟', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2035', 'actor_name': '贾玲', 'gender': '女', 'nationality': '中国'},
    {'actor_id': '2036', 'actor_name': '张小斐', 'gender': '女', 'nationality': '中国'},
    {'actor_id': '2037', 'actor_name': '陈凯歌', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2038', 'actor_name': '徐克', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2039', 'actor_name': '易烊千玺', 'gender': '男', 'nationality': '中国'},
    {'actor_id': '2040', 'actor_name': '林诣彬', 'gender': '男', 'nationality': '美国'},
    {'actor_id': '2041', 'actor_name': '米歇尔·罗德里格兹', 'gender': '女', 'nationality': '美国'}]

movie_actor_relation = [{'id': '1', 'movie_id': '1001', 'actor_id': '2001', 'relation_type': '主演'},
                        {'id': '2', 'movie_id': '1001', 'actor_id': '2001', 'relation_type': '导演'},
                        {'id': '3', 'movie_id': '1002', 'actor_id': '2002', 'relation_type': '导演'},
                        {'id': '4', 'movie_id': '1003', 'actor_id': '2001', 'relation_type': '主演'},
                        {'id': '5', 'movie_id': '1003', 'actor_id': '2003', 'relation_type': '主演'},
                        {'id': '6', 'movie_id': '1003', 'actor_id': '2004', 'relation_type': '导演'},
                        {'id': '7', 'movie_id': '1004', 'actor_id': '2005', 'relation_type': '导演'},
                        {'id': '8', 'movie_id': '1004', 'actor_id': '2006', 'relation_type': '主演'},
                        {'id': '9', 'movie_id': '1004', 'actor_id': '2007', 'relation_type': '主演'},
                        {'id': '10', 'movie_id': '1005', 'actor_id': '2008', 'relation_type': '导演'},
                        {'id': '11', 'movie_id': '1005', 'actor_id': '2009', 'relation_type': '主演'},
                        {'id': '12', 'movie_id': '1005', 'actor_id': '2010', 'relation_type': '主演'},
                        {'id': '13', 'movie_id': '1006', 'actor_id': '2011', 'relation_type': '导演'},
                        {'id': '14', 'movie_id': '1006', 'actor_id': '2012', 'relation_type': '主演'},
                        {'id': '15', 'movie_id': '1006', 'actor_id': '2013', 'relation_type': '主演'},
                        {'id': '16', 'movie_id': '1007', 'actor_id': '2014', 'relation_type': '导演'},
                        {'id': '17', 'movie_id': '1007', 'actor_id': '2015', 'relation_type': '主演'},
                        {'id': '18', 'movie_id': '1008', 'actor_id': '2016', 'relation_type': '导演'},
                        {'id': '19', 'movie_id': '1008', 'actor_id': '2017', 'relation_type': '主演'},
                        {'id': '20', 'movie_id': '1009', 'actor_id': '2018', 'relation_type': '导演'},
                        {'id': '21', 'movie_id': '1009', 'actor_id': '2019', 'relation_type': '主演'},
                        {'id': '22', 'movie_id': '1009', 'actor_id': '2020', 'relation_type': '主演'},
                        {'id': '23', 'movie_id': '1010', 'actor_id': '2021', 'relation_type': '导演'},
                        {'id': '24', 'movie_id': '1010', 'actor_id': '2022', 'relation_type': '主演'},
                        {'id': '25', 'movie_id': '1011', 'actor_id': '2023', 'relation_type': '导演'},
                        {'id': '26', 'movie_id': '1011', 'actor_id': '2006', 'relation_type': '主演'},
                        {'id': '27', 'movie_id': '1011', 'actor_id': '2024', 'relation_type': '主演'},
                        {'id': '28', 'movie_id': '1012', 'actor_id': '2025', 'relation_type': '导演'},
                        {'id': '29', 'movie_id': '1012', 'actor_id': '2026', 'relation_type': '主演'},
                        {'id': '30', 'movie_id': '1012', 'actor_id': '2027', 'relation_type': '主演'},
                        {'id': '31', 'movie_id': '1012', 'actor_id': '2028', 'relation_type': '主演'},
                        {'id': '32', 'movie_id': '1013', 'actor_id': '2029', 'relation_type': '导演'},
                        {'id': '33', 'movie_id': '1013', 'actor_id': '2030', 'relation_type': '主演'},
                        {'id': '34', 'movie_id': '1013', 'actor_id': '2009', 'relation_type': '主演'},
                        {'id': '35', 'movie_id': '1013', 'actor_id': '2031', 'relation_type': '主演'},
                        {'id': '36', 'movie_id': '1015', 'actor_id': '2032', 'relation_type': '导演'},
                        {'id': '37', 'movie_id': '1015', 'actor_id': '2015', 'relation_type': '导演'},
                        {'id': '38', 'movie_id': '1015', 'actor_id': '2011', 'relation_type': '导演'},
                        {'id': '39', 'movie_id': '1015', 'actor_id': '2015', 'relation_type': '主演'},
                        {'id': '40', 'movie_id': '1015', 'actor_id': '2033', 'relation_type': '主演'},
                        {'id': '41', 'movie_id': '1015', 'actor_id': '2034', 'relation_type': '主演'},
                        {'id': '42', 'movie_id': '1016', 'actor_id': '2035', 'relation_type': '导演'},
                        {'id': '43', 'movie_id': '1016', 'actor_id': '2035', 'relation_type': '主演'},
                        {'id': '44', 'movie_id': '1016', 'actor_id': '2036', 'relation_type': '主演'},
                        {'id': '45', 'movie_id': '1016', 'actor_id': '2022', 'relation_type': '主演'},
                        {'id': '46', 'movie_id': '1017', 'actor_id': '2037', 'relation_type': '导演'},
                        {'id': '47', 'movie_id': '1017', 'actor_id': '2038', 'relation_type': '导演'},
                        {'id': '48', 'movie_id': '1017', 'actor_id': '2008', 'relation_type': '导演'},
                        {'id': '49', 'movie_id': '1017', 'actor_id': '2001', 'relation_type': '主演'},
                        {'id': '50', 'movie_id': '1017', 'actor_id': '2039', 'relation_type': '主演'},
                        {'id': '51', 'movie_id': '1018', 'actor_id': '2040', 'relation_type': '导演'},
                        {'id': '52', 'movie_id': '1018', 'actor_id': '2019', 'relation_type': '主演'},
                        {'id': '53', 'movie_id': '1018', 'actor_id': '2041', 'relation_type': '主演'}]


@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')
# 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息


@app.route('/initdb0')
def initdb0():
    #  1. 创建数据库
    db.drop_all()
    db.create_all()
    # 2. 创建表

    ##新增
    #将电影信息数据添加到数据库中。使用了一个循环来遍历movie_info_data中的每个元素，并根据每个元素创建一个MovieInfo对象，然后将其添加到数据库会话中。
    #在循环中，首先获取电影信息中的发布日期（release_date）。然后，使用datetime函数将发布日期的年份、月份和日期提取出来，并将其作为参数传递给datetime
    #函数来创建一个datetime对象。接下来，根据电影信息中的其他属性，例如电影ID、电影名称、国家、电影类型和年份，创建一个MovieInfo对象。
    #最后，通过db.session.add(movie)将movie对象添加到数据库会话中，以便在提交更改后将其保存到数据库中。
    #已有一个名为MovieInfo的数据库模型类（在models.py），并且已经正确地导入了相关的模块和库，例如db和datetime。
    for m in movie_info_data:
        release_date = m['release_date']

        movie = MovieInfo(movie_id=m['movie_id'],
                          movie_name=m['movie_name'],
                          release_date=datetime(int(release_date[0:4]), int(release_date[5: 7]), int(release_date[8:])),
                          country=m['country'],
                          movie_type=m['movie_type'],
                          year=m['year'],
                          )
        db.session.add(movie)

    for m in move_box_data:
        movie_box = MovieBox(movie_id=m['movie_id'],
                             box=m['box_office'])
        db.session.add(movie_box)

    for m in actor_info_data:
        actor_info = ActorInfo(actor_id=m['actor_id'],
                               actor_name=m['actor_name'],
                               gender=m['gender'],
                               country=m['nationality']
                               )
        db.session.add(actor_info)

    for m in movie_actor_relation:
        movie_actor_rela = MovieActorRelation(id=m['id'],
                                              movie_id=m['movie_id'],
                                              actor_id=m['actor_id'],
                                              relation_type=m['relation_type'])
        db.session.add(movie_actor_rela)

    db.session.commit()

    click.echo('Done.')
    # 3.创建用户
    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = "admin"
        user.set_password("admin")  # 设置密码
    else:
        click.echo('Creating user...')
        user = User(username="admin", name='admin')
        user.set_password("admin")  # 设置密码
        db.session.add(user)

    db.session.commit()  # 提交数据库会话
    click.echo('Done.')

    return redirect(url_for('index'))


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)  # 设置密码
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)  # 设置密码
        db.session.add(user)

    db.session.commit()  # 提交数据库会话
    click.echo('Done.')


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # # 新增
    for m in movie_info_data:
        release_date = m['release_date']

        movie = MovieInfo(movie_id=m['movie_id'],
                          movie_name=m['movie_name'],
                          release_date=datetime(int(release_date[0:4]), int(release_date[5: 7]), int(release_date[8:])),
                          country=m['country'],
                          movie_type=m['movie_type'],
                          year=m['year'],
                          )
        db.session.add(movie)

    for m in move_box_data:
        movie_box = MovieBox(movie_id=m['movie_id'],
                             box=m['box_office'])
        db.session.add(movie_box)

    for m in actor_info_data:
        actor_info = ActorInfo(actor_id=m['actor_id'],
                               actor_name=m['actor_name'],
                               gender=m['gender'],
                               country=m['nationality']
                               )
        db.session.add(actor_info)

    for m in movie_actor_relation:
        movie_actor_rela = MovieActorRelation(id=m['id'],
                                              movie_id=m['movie_id'],
                                              actor_id=m['actor_id'],
                                              relation_type=m['relation_type'])
        db.session.add(movie_actor_rela)

    db.session.commit()

    click.echo('Done.')
