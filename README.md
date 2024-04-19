# Test Task AmiFactory

## Setup Instructions

1. Clone the repository to your computer.
    ```shell
   git clone https://github.com/Sparix/AmiFactory_TestTask.git
   cd <project-directory>
2. Create a virtual environment by running `python -m venv venv`.
3. Activate the virtual environment:
    - On Windows: `venv\Scripts\activate`
    - On macOS and Linux: `source venv/bin/activate`
4. Install the required dependencies `pip install -r requirements.txt`.
5. Run migration `python manage.py migrate`
6. Download the initial data from the fixtures `python manage.py loaddata fixtures_db.json`
7. Run the Django server `python manage.py runserver`.

### Available links:

- Genres http://127.0.0.1:8000/api/v1/genres/
- Movies http://127.0.0.1:8000/api/v1/movies/
- Movie Detail http://127.0.0.1:8000/api/v1/movies/ <movie_id>/


## Technologies Used

- Django
- Python
