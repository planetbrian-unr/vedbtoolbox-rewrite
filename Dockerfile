# slim is not used!
FROM python:bookworm

# add everything here into the docker image
WORKDIR /app
COPY requirements.txt .
COPY LICENSE .
COPY toolbox ./toolbox

# install necessary stuff not in image & the application's pip requirements
RUN apt update && apt install -y libgl1
RUN pip install --no-cache-dir -r requirements.txt

# open port 8000, which is the default of gunicorn. runs it
EXPOSE 8000
CMD ["gunicorn", "-w", "4", "flaskr:create_app(test_config=None)"]