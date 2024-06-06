# -----------------------------------------------------------------------------
# (C) 2024 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from uvicorn import run

if __name__ == '__main__':
    run('main:app', host='0.0.0.0', port=8000, reload=True)
