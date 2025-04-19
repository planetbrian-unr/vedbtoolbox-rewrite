# written by brian, a "quick" dockerfile used for containerized deployment
# not quite fully functional; seems to be a thing with proxies

# slim is not used!
FROM python:bookworm

# add everything here into the docker image
WORKDIR /app
COPY requirements.txt .
COPY LICENSE .
COPY flaskr ./toolbox

# install necessary stuff not in image & the application's pip requirements
RUN <<EOF
    apt update
    apt install -y libgl1
    pip install --no-cache-dir -r requirements.txt
EOF

# open port 8000, which is the default of gunicorn. runs it
EXPOSE 8000
CMD ["gunicorn", "-w", "4", "toolbox:create_app(test_config=None)"]
