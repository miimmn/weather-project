import hashlib
from user.models.userDAO import userDAO
from config import getLogger



class userService:

    def __init__(self):
        self.dao = userDAO()
        self.logger = getLogger()
        
    # 회원가입
    def signup(self, data):

        # 이미 가입된 이메일인지 확인
        findUser = self.dao.selectUserByEmail(data)

        if not findUser :
            self.dao.insertUser(data)
        else :
            return "ALREADY EXIST"


    # 로그인
    def login(self, data) :
        # inputEmail = data['email']
        inputPwd = data['pwd']

        # DB 비밀번호
        userInfo = self.dao.selectUserByEmail(data)

        # 가입된 이메일인 경우
        if userInfo != '' :
            result = [userInfo[0], userInfo[2]]

            # print("    DB   정보    :  ", userInfo)
            self.logger.info(' ---------DB 정보--------' + str(userInfo))

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

        
        
