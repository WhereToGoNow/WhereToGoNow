# WhereToGoNow

Main repository for CS408

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
