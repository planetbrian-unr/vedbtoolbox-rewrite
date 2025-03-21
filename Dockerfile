# slim is not used!
FROM python:bookworm

# add everything here into the docker image
WORKDIR /app
COPY . .

# install necessary stuff not found in image, as well as the application's pip requirements
RUN apt update && apt install -y libgl1
RUN pip install --no-cache-dir -r requirements.txt

# open port 8000, which is the default of gunicorn
EXPOSE 8000
CMD ["gunicorn", "-w", "4", "flaskr:create_app(test_config=None)"]