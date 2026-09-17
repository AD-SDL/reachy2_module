FROM ghcr.io/ad-sdl/madsci:latest

LABEL org.opencontainers.image.source=https://github.com/AD-SDL/reachy2_module
LABEL org.opencontainers.image.description="Drivers and REST API's for the reachy2 robot"
LABEL org.opencontainers.image.licenses=MIT

#########################################
# Module specific logic goes below here #
#########################################

RUN mkdir -p reachy2_module

COPY ./src reachy2_module/src
COPY ./README.md openarm_module/README.md
COPY ./pyproject.toml reachy2_module/pyproject.toml

RUN --mount=type=cache,target=/root/.cache \
    pip install -e ./reachy2_module

CMD ["python", "reachy2_module/src/openarm_rest_node.py"]

#########################################