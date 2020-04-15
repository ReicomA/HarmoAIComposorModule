from .label.requestdata_label import *

class RequestData:
    """
        클라이언트로부터 요청받은 데이터를 "가공한" 클래스 데이터
        userKey : Int
        genre : Int
        timeSignature : Int
        noteSize : Int
    """
    def __init__(self, userKey, genre, timeSignature, noteSize):
        """
            클라이언트로부터 받는 데이터를 변환한 다음 삽압하는 순서이므로
            맞지 않을 경우 ValueError 반환
        """
        try:
            # userkey는 integer여야 한다.
            if isinstance(userKey, int) is False:
                raise ValueError("user key must be integer")
            self.userKey = userKey

            self.genre = changeGenreToInteger(genre)
            self.timeSignature = changeSignatureToInteger(timeSignature)
            # NoteSize
            # 노트크기제한은 Config의 데이터로 밖에서 처리 필요
            if isinstance(noteSize, int) is False:
                raise ValueError("note size must be integer")
            if noteSize > 0:
                self.noteSize = noteSize
        except ValueError as e:
            raise e