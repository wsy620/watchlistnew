import os
import sys
from datetime import datetime

import click
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'dataMovices.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

# 需要设置 SECRET_KEY。不然会报错
app.config['SESSION_TYPE'] = "filesystem"
app.config['SECRET_KEY'] = os.urandom(24)

# 在扩展类实例化前加载配置
db = SQLAlchemy(app)
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


# 1. 创建数据库
@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')
# 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息


# 2. 数据库结构
class MovieInfo(db.Model):
    __tablename__ = 'movie_info'
    movie_id = db.Column(db.String(10), primary_key=True)
    movie_name = db.Column(db.String(20), nullable=False)
    release_date = db.Column(db.DateTime)
    country = db.Column(db.String(20))
    movie_type = db.Column('type', db.String(10))
    year = db.Column(db.Integer, CheckConstraint('year>=1000 and year<=2100'))

    def to_json(self):
        return {
            'movie_id': self.movie_id,
            'movie_name': self.movie_name,
            'release_date': str(self.release_date),
            'country': self.country,
            'type': self.movie_type,
            'year': self.year
        }


class MovieBox(db.Model):
    __tablename__ = 'movie_box'
    movie_id = db.Column(db.String(10), primary_key=True)
    box = db.Column(db.Float)

    def to_json(self):
        return {
            'movie_id': self.movie_id,
            'box': self.box
        }


class ActorInfo(db.Model):
    __tablename__ = 'actor_info'
    actor_id = db.Column(db.String(10), primary_key=True)
    actor_name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(2), nullable=False)
    country = db.Column(db.String(20))

    def to_json(self):
        return {
            'actor_id': self.actor_id,
            'actor_name': self.actor_name,
            'gender': self.gender,
            'act_country': self.country
        }


class MovieActorRelation(db.Model):
    __tablename__ = 'movie_actor_relation'
    id = db.Column(db.String(10), primary_key=True)
    movie_id = db.Column(db.String(10), db.ForeignKey('movie_info.movie_id'))
    actor_id = db.Column(db.String(10), db.ForeignKey('actor_info.actor_id'))
    relation_type = db.Column(db.String(20))

    def to_json(self):
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'actor_id': self.actor_id,
            'relation_type': self.relation_type
        }


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


# @app.context_processor
# def inject_user():
#     user = User.query.first()
#     return dict(user=user)
def merge_data(data_list):
    merged_data = {}
    for data in data_list:
        movie_id = data['movie_id']
        if movie_id not in merged_data:
            merged_data[movie_id] = {
                'movie_id': movie_id,
                'movie_name': data['movie_name'],
                'release_date': data['release_date'][:10],
                'country': data['country'],
                'type': data['type'],
                'year': data['year'],
                'box': data['box'],
                'actors': []
            }
        actor_data = next((item for item in merged_data[movie_id]['actors'] if item['actor_id'] == data['actor_id']),
                          None)
        if actor_data is None:
            actor_data = {
                'actor_id': data['actor_id'],
                'actor_name': data['actor_name'],
                'gender': data['gender'],
                'act_country': data['act_country'],
                'relations': [{
                    'id': data['id'],
                    'relation_type': data['relation_type']
                }]
            }
            merged_data[movie_id]['actors'].append(actor_data)
        else:
            actor_data['relations'].append({
                'id': data['id'],
                'relation_type': data['relation_type']
            })

    merged_data_list = list(merged_data.values())
    for data in merged_data_list:
        for actor_data in data['actors']:
            actor_data.pop('id', None)

    return merged_data_list


def query_all_data():
    result = db.session.query(
        MovieInfo, MovieBox, ActorInfo, MovieActorRelation
    ).filter(
        MovieInfo.movie_id == MovieBox.movie_id,
        MovieInfo.movie_id == MovieActorRelation.movie_id,
        ActorInfo.actor_id == MovieActorRelation.actor_id
    ).order_by(MovieBox.box.desc()).all()

    # 处理结果
    combined_data = []
    for movie_info, movie_box, actor_info, movie_actor_relation in result:
        movie_data = movie_info.to_json()
        movie_data['box'] = movie_box.box
        actor_data = actor_info.to_json()
        relation_data = movie_actor_relation.to_json()
        combined_data.append({**movie_data, **actor_data, **relation_data})

    # 打印结果
    new_combined_data = merge_data(combined_data)
    return new_combined_data


def convert_data_format_act_relation(actor_id, relation_type):
    result = []

    new_relation_type = []
    temp = []
    for j in relation_type:
        if j != "|":
            temp.append(j)
        else:
            new_relation_type.append(temp)
            temp = []

    new_actor_id = []
    temp = []
    for j in actor_id:
        if j != "|":
            temp.append(j)
        else:
            new_actor_id.append(temp)
            temp = []

    for i in range(len(new_actor_id)):
        result.append({
            'actor_id': new_actor_id[i],
            'relation_type': new_relation_type[i]
        })
    return result


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
        actor_id = request.form.get('actor_id')
        relation = request.form.get('relation')
        box = request.form.get('box')

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

        # 3. 插入收视率和 电影关系表
        movie_box = MovieBox(movie_id=movie_id,
                             box=box)
        db.session.add(movie_box)

        # 4. 插入 演员和电影关系表
        # actor_id
        # actor = ActorInfo.query.filter(ActorInfo.actor_name == actor_name).first()
        # print(actor)
        movice_act_relas = MovieActorRelation.query.all()
        last_movice_act_rela_id = str(int(movice_act_relas[-1].id) + 1)
        movie_actor_rela = MovieActorRelation(id=last_movice_act_rela_id,
                                              movie_id=movie_id,
                                              actor_id=actor_id,
                                              relation_type=relation)
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

        print(search_type)
        # 多表联查并按照box从高到低排序
        new_combined_data = query_all_data()
        res = []
        # print(new_combined_data[0])
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
def edit(movie_id):
    movie = MovieInfo.query.get_or_404(movie_id)  # 根据 movie_id 获取电影信息，如果不存在则返回 404 错误
    if request.method == 'POST':
        # 获取表单数据
        movie_name = request.form.get('movie_name')
        release_date = request.form.get('release_date')
        country = request.form.get('country')
        movie_type = request.form.get('movie_type')
        year = request.form.get('year')
        actor_name = request.form.get('actor_name')
        relation_type = request.form.getlist("relation_type[]")
        box = request.form.get('box')
        actor_id = request.form.getlist('actor_id[]')
        act_relation = convert_data_format_act_relation(actor_id=actor_id, relation_type=relation_type)

        # 验证数据
        if not movie_name or not year or len(year) > 4 or len(movie_name) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))

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

        # # 更新收视率
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
def detail_info(movie_id):
    movie = MovieInfo.query.get_or_404(movie_id)
    new_combined_data = query_all_data()
    target = {}
    for i in new_combined_data:
        if i["movie_id"] == str(movie_id):
            target = i
    return render_template('detail.html', combined_data=target)  # 传入被编辑的电影记录


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
def delete(movie_id):
    # 1. 删除电影表
    movie = MovieInfo.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    #  2. 删除收视率表
    movie_box = MovieBox.query.get_or_404(movie_id)
    db.session.delete(movie_box)

    #  3. 删除演员和 电影关系表
    move_box_datas = MovieActorRelation.query.filter(MovieActorRelation.movie_id == movie_id)
    for move_box_data in move_box_datas:
        db.session.delete(move_box_data)

    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页
