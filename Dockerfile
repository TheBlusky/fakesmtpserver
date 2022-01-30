FROM python:3

# Prepare requirements
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Prepare running user
RUN mkdir /app
RUN useradd -ms /bin/bash python
RUN chown -R python:python /app
USER python
WORKDIR /app

# Configure app
ADD src/*.py /app
EXPOSE 5000
EXPOSE 2525
CMD python main.py
