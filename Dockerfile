FROM ghcr.io/mo-rise/porla:v0.2.1

# Add custom binaries to the bin folder in the repository as required
COPY --chmod=555 ./bin/* /usr/local/bin/