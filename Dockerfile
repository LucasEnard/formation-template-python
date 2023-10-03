ARG IMAGE=intersystemsdc/iris-community:latest
FROM $IMAGE as builder

COPY . /irisdev/app

RUN pip3 install -r requirements.txt

# fix ld_library_path
ENV LD_LIBRARY_PATH=${ISC_PACKAGE_INSTALLDIR}/bin:/home/irisowner/irissys/:$LD_LIBRARY_PATH

COPY . /irisdev/app

RUN pip3 install -r requirements.txt
# load demo stuff
RUN iris start IRIS && \
    iris merge IRIS /irisdev/app/merge.cpf && \
    python3 /irisdev/app/iris_script.py && \
    iris stop IRIS quietly


FROM $IMAGE as final

ADD --chown=${ISC_PACKAGE_MGRUSER}:${ISC_PACKAGE_IRISGROUP} https://github.com/grongierisc/iris-docker-multi-stage-script/releases/latest/download/copy-data.py /irisdev/app/copy-data.py

RUN --mount=type=bind,source=/,target=/builder/root,from=builder \
    cp -f /builder/root/usr/irissys/iris.cpf /usr/irissys/iris.cpf && \
    python3 /irisdev/app/copy-data.py -c /usr/irissys/iris.cpf -d /builder/root/ 

ENV PYTHON_PATH=/usr/irissys/bin/irispython
ENV LD_LIBRARY_PATH=${ISC_PACKAGE_INSTALLDIR}/bin:/home/irisowner/irissys/:$LD_LIBRARY_PATH
ENV IRISUSERNAME "SuperUser"
ENV IRISPASSWORD "SYS"
ENV IRISNAMESPACE "IRISAPP"