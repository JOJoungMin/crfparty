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
    return "Hello, Flask!"

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

if __name__ == '__main__':  
   app.run('0.0.0.0', port=5000, debug=True)



if __name__ == '__main__':
    app.run(debug=True)
