from flask import Flask, jsonify, request,render_template
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
client = MongoClient('localhost', 27017)
db = client.party


# 코딩 시작
app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login' , methods=['POST'])
def login_post():

    data = request.get_json()

    user_id = data.get('user_id')
    user_password = data.get('user_password')

    login_data = db.userdata.find_one({
        'user_id': user_id,
        'user_password': user_password  # 비밀번호도 조건에 추가
    })
    print(login_data['user_name'])
  

    if login_data:
       print(login_data)
       return jsonify({'result': 'success'})
    else:
         return jsonify({'result': 'false'})


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():

    data = request.get_json()

   
    user_name = data.get('user_name') 

    user_id  = data.get('user_id')
    user_cord = data.get('user_cord')
    user_password = data.get('user_password')
    print(type(user_cord))
    doc = {
        'user_name': user_name,
        'user_id': user_id,
        'user_cord': user_cord,
        'user_password': user_password,
    }

    db.userdata.insert_one(doc)
   

    return render_template('register.html')

@app.route('/index')
def index():
    return render_template('index.html')  # 로그인 후 index.html로 이동



# @app.route('/postPtdata', methods=['POST'])
# def post_data():
#    data = request.get_json()  
  
#    title_give =data.get('title_give') 
#    category_give = data.get('category_give')
#    content_give = data.get('content_give')
#    date_give = data.get('date_give')
#    partparticipants_give = data.get('partparticipants_give')
#    partymaneserName = data.get('name_give')
#    partymaneserCord_give = data.get('partyCord_give')

   
#    doc = {
#      'title_give': title_give,
#      'category_give': category_give,
#      'content_give': content_give,
#      'date_give': date_give,
#      'partparticipants_give': partparticipants_give,
#      'partymaneserName_name' : partymaneserName,
#      'partymanaser_cord': partymaneserCord_give,
#      'userArr': [],
#      'userCord': [],
#    }

#    db.party.insert_one(doc)
#    return jsonify({'result': 'succese'})


@app.route('/postPtdata', methods=['POST'])
def post_data():
    data = request.get_json()  

    title_give = data.get('title_give') 
    category_give = data.get('category_give')
    content_give = data.get('content_give')
    date_give = data.get('date_give')
    partparticipants_give = data.get('partparticipants_give')
    partymaneserName = data.get('name_give')
    partymaneserCord_give = data.get('partyCord_give')

    doc = {
        'title_give': title_give,
        'category_give': category_give,
        'content_give': content_give,
        'date_give': date_give,
        'partparticipants_give': partparticipants_give,
        'partymaneserName_name': partymaneserName,
        'partymanaser_cord': partymaneserCord_give,
    }

    # party 컬렉션에서 단 하나의 문서를 찾아서 userArr 배열에 doc을 추가
    db.party.update_one(
        {},  # 조건: 모든 문서에 대해
        {'$setOnInsert': {'userArr': []}},  # userArr 배열이 없으면 생성
        upsert=True  # 문서가 없으면 새로 생성
    )

    # userArr 배열에 doc 추가
    db.party.update_one(
        {},  # 조건: 모든 문서에 대해
        {'$push': {'userArr': doc}}  # userArr 배열에 doc 추가
    )

    return jsonify({'result': 'success'})

@app.route('/joinParty', methods=['POST'])
def join_party():
   data = request.get_json()  

   partymanaser_cord = data.get('partyCord_give')
   user_arr = data.get('party_member')
   userCord_arr = data.get('partymember_cord')


   result = db.party.update_one(
        {' partymanaser_cord':partymanaser_cord},  
        {'$push': {'userArr': user_arr,
                  'userCord' : userCord_arr} }  # 배열에 새로운 할 일을 추가
    )
   
    
   if result.modified_count > 0:
        return jsonify({'result': 'success'})
   else:
        return jsonify({'result': 'fail', 'message': '문서를 찾을 수 없습니다.'})
      

# @app.route('/lodingdata')
# def load_data():
#     result = list(db.party.find({}, {'_id': 0}))
#     print(len(result))
#     data_list = []
#     if result:
#        for data in result:
#            print(data)
#            data_list.append({
#                'Arr_give': data.get('title_give'),
#                'category_give': data.get('category_give'),
#                "content_give" : data.get('content_give'),
#                "date_give" : data.get('date_give'),
#                "partparticipants_give" : data.get('partparticipants_give'),
#         })
#        return jsonify(data_list), 200
#     else:
#        return jsonify([]), 200    


@app.route('/lodingdata')
def load_data():
    result = list(db.party.find({}, {'_id': 0}))
    print(len(result))
    data_list = []
    if result:
       for data in result:
            data_list.append(data)
       print(data_list)
       return jsonify(data_list), 200
    else:
       return jsonify([]), 200    



# @app.route('/lodingdata')
# def load_data():
#  result = list(db.party.find({}))
#  print(len(result))
#  data_list = []
#  index = 제공받은_인덱스  # 미리 제공받은 인덱스 값

#  if result:
#     for data in result:
#         data_list.append({
#             'title_give': data.get('title_give'),
#             'category_give': data.get('category_give'),
#             "content_give": data.get('content_give'),
#             "date_give": data.get('date_give'),
#             "partparticipants_give": data.get('partparticipants_give'),
#         })
    
#     # 인덱스가 유효한지 확인
#     if 0 <= index < len(data_list):
#         # 인덱스에 해당하는 데이터 출력
#         print(data_list[index])
#         return jsonify(data_list[index]), 200
#     else:
#         return jsonify({"error": "Invalid index"}), 400
# else:
#     return jsonify([]), 200


@app.route('/deleteParty', methods=['POST'])
def delete_Party():

    data = request.get_json()
    party_code = data.get('partyCord_give')

    delete_data = db.party.find_one({'partymanaser_cord': party_code})
      
    if delete_data:
        result = db.party.delete_one({'partymanaser_cord': party_code}) 

        if result.deleted_count > 0:  
   
            return jsonify({'result': 'true'})
        else:
            return jsonify({'result': 'false', 'message': '삭제실패'}), 400  # 수정된 내용이 없을 경우
    else:
        return jsonify({'result': 'false', 'message': '해당 파티티는 db에 존재하지 않는다'}), 404

if __name__ == '__main__':  
   app.run('0.0.0.0', port=5000, debug=True)



if __name__ == '__main__':
    app.run(debug=True)
