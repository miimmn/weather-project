import hashlib
from models.dao.userDAO import userDAO


class userService:

    def __init__(self):
        self.dao = userDAO()

    # 회원가입
    def signup(self, data):

        insertData = []
        enc = hashlib.md5()

        originPwd = data['password']
        # md5 처리
        enc.update(str(originPwd).encode('utf-8'))
        encryptPwd = enc.hexdigest()

        insertData.append(data['email'])
        insertData.append(encryptPwd)
        insertData.append(data['name'])

        self.dao.insertUser(insertData)


    # 로그인
    def login(self, data) :
        inputEmail = data['email']
        inputPwd = data['pwd']

        # DB 비밀번호
        userInfo = self.dao.selectUserByEmail(inputEmail)

        # 가입된 이메일인 경우
        if type(userInfo) != type(None) :
            result = [userInfo[0], userInfo[2]]

            print("    DB   정보    :  ", userInfo)

            # 입력 비밀번호 암호화
            enc = hashlib.md5()
            enc.update(str(inputPwd).encode('utf-8'))
            inputPwd = enc.hexdigest()

            # 비밀번호 일치 : 사용자 데이터 반환 (이메일, 이름)
            if inputPwd == userInfo[1] :
                return result
            # 비밀번호 불일치
            else :
                return "FAIL"
        
        # 가입되지 않은 이메일인 경우
        else :
            return "NO EXIST"

        
        
