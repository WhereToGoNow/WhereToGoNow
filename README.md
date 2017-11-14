# WhereToGoNow

### About
Main repository

### Project structure
(Reference: [Flask - Organizing your project](http://exploreflask.com/en/latest/organizing.html))

- `scripts`: Useful scripts which is not directly used by the app (ex. crawler)
- `src`
  - `routerconntest`
    - `core`: Core modules (ex. router, evaluator)
    - `static`: Files that don't change (ex. js, css)
      - `data`
      - `libs`
      - `xxx.js`
      - `xxx.css`
    - `templates`: Template files for the pages (ex. html)
      - `xxx.html`
    - `controllers.py`
    - `models.py`
