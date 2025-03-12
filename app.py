from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from pymongo import MongoClient
import jwt
import datetime
from functools import wraps
import json
SECRET_KEY = "your_secret_key"  # JWT 서명에 사용할 비밀키


client = MongoClient('localhost', 27017)
db = client.party



# 코딩 시작c
app = Flask(__name__)
CORS(app)

def token_required(f):
    @wraps(f)  # ✅ 여기가 올바르게 들여쓰기 되어야 함
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'result': 'false', 'message': '토큰이 없습니다.'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = db.userdata.find_one({'user_id': data['user_id']})
            if not current_user:
                return jsonify({'result': 'false', 'message': '사용자를 찾을 수 없습니다.'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'result': 'false', 'message': '토큰이 만료되었습니다.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'result': 'false', 'message': '유효하지 않은 토큰입니다.'}), 401

        return f(current_user, *args, **kwargs)

    return decorated  # ✅ `decorated` 반환 시에도 들여쓰기 유지

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    
    data = request.get_json()

    user_id = data.get('user_id')
    user_password = data.get('user_password')

    login_data = db.userdata.find_one({
        'user_id': user_id,
        'user_password': user_password  # 비밀번호도 조건에 추가
    })

    if login_data:
        # JWT 토큰 생성
        token = jwt.encode({
            'user_id': user_id,
            'user_name': login_data['user_name'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, SECRET_KEY, algorithm="HS256")
        
        # 터미널에 토큰 정보 출력
        print("\n===== JWT 토큰 정보 =====")
        print(f"사용자 ID: {user_id}")
        print(f"사용자 이름: {login_data['user_name']}")
        print(f"생성된 토큰: {token}")
        
        
        doc = {
            'user_name': login_data['user_name'],
            'user_cord': login_data['user_cord'],
        }

        # 토큰 디코딩 정보도 출력
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            print(f"디코딩된 페이로드: {decoded}")
            print(f"만료 시간: {datetime.datetime.fromtimestamp(decoded['exp'])}")
        except Exception as e:
            print(f"디코딩 오류: {e}")
        
        print("========================\n")
        
        # 클라이언트에 토큰 반환
        return jsonify({'result': 'success', 'token': token, "userdata": json.dumps(doc)})
    else:
        print(f"\n로그인 실패: {user_id}")
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
    
     return render_template('index.html') 


@app.route('/postPtdata', methods=['POST'])
def post_data():
   data = request.get_json()  
  
   title_give =data.get('title_give') 
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
     'partymaneserName_name' : partymaneserName,
     'partymanaser_cord': partymaneserCord_give,
     'userArr': [],
     'userCord': [],
   }

   db.party.insert_one(doc)
   return jsonify({'result': 'succese'})



@app.route('/joinParty', methods=['POST'])
def join_party():
   data = request.get_json()  

   partymanaser_cord = data.get('partyCord_give')
   print(partymanaser_cord)
   user_arr = data.get('party_member')
   userCord_arr = data.get('partymember_cord')
   print(type(user_arr))
   print(userCord_arr)
#  
   result = db.party.update_one(
    {'partymanaser_cord': partymanaser_cord},  
    {'$push': {'userArr': user_arr, 'userCord': userCord_arr}}
)


   if result.modified_count > 0:
        return jsonify({'result': 'success'})
   else:
        return jsonify({'result': 'fail', 'message': '문서를 찾을 수 없습니다.'})
      

@app.route('/lodingdata')
def load_data():
    result = list(db.party.find({}))
    data_list = []
    if result:
       for data in result:
           data_list.append({
               'title_give': data.get('title_give'),
               'category_give': data.get('category_give'),
               "content_give" : data.get('content_give'),
               "date_give" : data.get('date_give'),
               "partparticipants_give" : data.get('partparticipants_give'),
               "partymaneserName": data.get('partymaneserName_name'),
               "partymanaser_cord": data.get('partymanaser_cord'),
               "userArr": data.get('userCord'),
        })
       return jsonify(data_list), 200
    else:
       return jsonify([]), 200    

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


@app.route('/quitParty', methods=['POST'])
def delete_data():
   data = request.get_json()  
   partyCode = data.get('partyCode')
   index_give = data.get('index')
   

   document = db.party.find_one({'partymanaser_cord': partyCode})

   if document and 'userCord' in document:
    party_list = document['userCord']

    if 0 <= index_give <= len(party_list):
        new_party_list = party_list[:index_give] + party_list[index_give + 1:]

        # userArr 삭제 로직 추가
        if 'userArr' in document:
            user_arr = document['userArr']

            if 0 <= index_give <= len(user_arr):
                new_user_arr = user_arr[:index_give] + user_arr[index_give + 1:]
            else:
                return jsonify({'result': 'fail', 'msg': '유효하지 않은 인덱스입니다.'})

            # userArr 업데이트
            db.party.update_one(
                {'partymanaser_cord': partyCode},
                {'$set': {'userCord': new_party_list, 'userArr': new_user_arr}}
            )
        else:
            # userArr가 없을 경우
            db.party.update_one(
                {'partymanaser_cord': partyCode},
                {'$set': {'userCord': new_party_list}}
            )

        return jsonify({'result': 'success', 'msg': '값이 삭제되었습니다.'})
    else:
        return jsonify({'result': 'fail', 'msg': '유효하지 않은 인덱스입니다.'})
   else:
        return jsonify({'result': 'fail', 'msg': '문서가 존재하지 않거나 userCord가 없습니다.'})
   


if __name__ == '__main__':  
   app.run('0.0.0.0', port=5000, debug=True)


