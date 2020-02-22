FROM python:3.7.6-buster
# most models need GCC

RUN mkdir -p /app/src \
    && chown -R nobody:nogroup /app

# user: https://medium.com/@mccode/processes-in-containers-should-not-run-as-root-2feae3f0df3b
USER nobody

COPY requirements.txt /app/requirements.txt
RUN cd /app/ \
    && python -m venv /app/env \
    && /app/env/bin/pip install -r requirements.txt
ENV PATH /app/env/bin:$PATH

WORKDIR /app/src
COPY data /app/data
COPY src /app/src

EXPOSE 8080

ENTRYPOINT ["python", "src/api.py"]
