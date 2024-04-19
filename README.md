# Test Task AmiFactory

## Setup Instructions

1. Clone the repository to your computer.
    ```shell
   git clone https://github.com/Sparix/AmiFactory_TestTask.git
   cd <project-directory>

### Instructions without Docker

1. Create a virtual environment by running `python -m venv venv`.
2. Activate the virtual environment:
    - On Windows: `venv\Scripts\activate`
    - On macOS and Linux: `source venv/bin/activate`
3. Install the required dependencies `pip install -r requirements.txt`.
4. Run migration `python manage.py migrate`
5. Download the initial data from the fixtures `python manage.py loaddata fixtures_db.json`
6. Run the Django server `python manage.py runserver`.

### Instructions with Docker

1. Run dockerfile using this `docker run -p 8000:8000 test_task_app`


### Available links:

- Genres http://127.0.0.1:8000/api/v1/genres/
- Movies http://127.0.0.1:8000/api/v1/movies/
- Movie Detail http://127.0.0.1:8000/api/v1/movies/ <movie_id>/
- Media Files http://127.0.0.1:8000/media/ poster or bg_picture / img_name


## Technologies Used

- Django
- Python
