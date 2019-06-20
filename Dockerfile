FROM docker.repository.cloudera.com/cdsw/engine:8
  ADD ./requirements.txt requirements.txt
  RUN pip3 install -r requirements.txt
  RUN python3 -m spacy download en
