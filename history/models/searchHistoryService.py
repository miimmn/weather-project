from history.models.searhHistoryDAO import searchHistoryDAO

class searchHistoryService:

    def __init__(self) :
        self.dao = searchHistoryDAO()

    # 검색 기록 가져오기
    def getSearchHistory(self, data) :
        history = self.dao.getSearchHistory(data)
        lists = []        
        for i in history :
            result = {}
            str1 = ""
            str1 += f'{i[2]} {i[3]} {i[4]} ({i[5]})'

            result['id'] = str(i[0])
            result['address'] = str1
            lists.append(result)
        return lists
    
    
    # 검색 기록 넣기
    def insertSearchHistory(self, data) :
        self.dao.insertSearchHistory(data)

    # 검색 기록 삭제
    def deleteSearchHistory(self, data) :
        self.dao.deleteSearchHistory(data)