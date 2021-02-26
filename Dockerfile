FROM python:3.8.5

RUN mkdir -p /home/arctic/Test/uuu/
WORKDIR /home/arctic/Test/uuu/
COPY . /home/arctic/Test/uuu/
RUN pip3 install --no-cache-dir -r requirements.txt
ARG CONST_VAR="Minsk,BY"
ARG CONST_VIR="now"
ENV arg=${CONST_VAR} time=$CONST_VIR
CMD ["sh","-c","python ./print.py $arg $time"]
