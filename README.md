# WhereToGoNow

Main repository for CS408

### TODO
- Evaluation 파트 완성 (Hit value 이용 preference 계산)
- InfoWindow 시간 입력: 'hours'보다는 hours + minutes
- Hashtag 리스트 더 좋은 걸로 바꾸기 (ex. Art, Ancient, ...)
- Route 렌더링했을 때 spot 번호 매기기: 알파벳보다는 숫자로
- Route 리스트: Start 및 end 표시, 색상 바꾸기
- Route 렌더링 후 spot 클릭했을 때: 이름뿐만 아니라 설명이나 리뷰 등 제공
  - 설명: Wikipedia API를 쓸 수는 있는데, 이름이 위키에 있는 것과 거의 일치하지
    않으면 잘 안 먹음
  - 리뷰: SpotInfoSearcher 수정해서 Google API 상에서 받아올 수 있음
  - 사진: Google API로 받아올 수는 있는데, url이 아니라 photo id를 주고
    별도의 API로 이미지 자체를 받아와야 함 (시간만 충분하면 가능)
- (우리가 추천한 경로뿐만 아니라 최단경로도 제공)

### Requirement
- Python 2.X

### Dependency
- [flask](http://flask.pocoo.org/)
- [flask-login](https://github.com/maxcountryman/flask-login)

### Project structure
(Reference: [Flask - Organizing your project](http://exploreflask.com/en/latest/organizing.html))

- `scripts`: Useful scripts which is not directly used by the app (ex. crawler)
- `src`
  - `wheretogonow`
    - `core`: Core modules (ex. router, evaluator)
    - `static`: Files that don't change (ex. js, css)
      - `data`
      - `libs`
      - `xxx.js`
      - `xxx.css`
    - `templates`: Template files for the pages (ex. html)
      - `xxx.html`
    - `controllers.py`: Handle the requests / responses
    - `models.py`: Connect the core and the controller
