python -m venv .venv
source .venv/bin/activate          # Windows は .venv\Scripts\activate
pip install -r requirements.txt    # あれば
python manage.py migrate
python manage.py runserver
