# base image to be used
FROM python:3.8.3
ENV PYTHONUNBUFFERED 1
RUN pip3 install  Django==3.0.6
RUN pip3 install numpy matplotlib
RUN pip3 install opencv-python
RUN pip3 install pillow
RUN pip3 install pytesseract
RUN apt-get update \
    && apt-get install tesseract-ocr -y \
    python3 \
    python3-pip
COPY . /code/
WORKDIR /code
EXPOSE 8000
CMD /code/script.sh