# -*- coding: utf-8 -*-
# Copyright SweetCase Project, Re_Coma(Ha Jeong Hyun). All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#      http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .label.requestdata_label import *

class RequestData:
    """
        클라이언트로부터 요청받은 데이터를 "가공한" 클래스 데이터
        userKey : Int
        genre : Int
        timeSignature : Int
        noteSize : Int
    """
    def __init__(self, myIP, genre, timeSignature, noteSize):
        """
            클라이언트로부터 받는 데이터를 변환한 다음 삽압하는 순서이므로
            맞지 않을 경우 ValueError 반환
        """
        try:
            # IP
            if isinstance(myIP, str) is False:
                raise ValueError("user key must be string")
            self.ip = myIP

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