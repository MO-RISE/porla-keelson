FROM ghcr.io/mo-rise/porla-zenoh:v0.2.0

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Add custom binaries to the bin folder in the repository as required
COPY --chmod=555 ./bin/* /usr/local/bin/