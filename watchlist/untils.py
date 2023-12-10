from watchlist.models import MovieInfo, MovieBox, MovieActorRelation, ActorInfo
from watchlist import db


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

    # 增加排名字段

    abccccccc = [
        {'movie_id': '1022', 'movie_name': '自定义2', 'release_date': '1986-11-22', 'country': '中国12',
         'type': '喜剧3', 'year': 1986, 'box': 80.02, 'actors': [
            {'actor_id': '2001', 'actor_name': '吴京', 'gender': '男', 'act_country': '中国',
             'relations': [{'id': '57', 'relation_type': '演员2'}]}]}

    ]
    for i in range(len(merged_data_list)):
        merged_data_list[i]["order_num"] = i + 1

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


def _convert_data_format_act_relation(actor_names, actor_id, relation_type,genders):
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
            'actor_name': actor_names[i],
            'relation_type': new_relation_type[i],
            'gender':genders[i]

        })
    return result
