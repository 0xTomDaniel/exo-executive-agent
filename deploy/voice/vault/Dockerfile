FROM debian:bookworm-slim

ARG CODEX_UID=1001
ARG CODEX_VERSION=0.153.1
ARG INSTALLER_SHA256=ba92dd27e5c06f0d3bbc58bfa4b9cfb6599cd2742fbb1f92a2765e6c07dedb5a
ARG NITRIDE_COMMIT=f3addd283300b37fbed73e65513af9101c921d22
ARG NITRIDE_SHA256=18d9cddddaa411886a4d0bfe26a6de45b3c9c84825988eee9c4d44cdf9890363

COPY --from=node:22.23.2-bookworm-slim /usr/local/bin/node /usr/local/bin/node

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash ca-certificates curl git procps python3 ripgrep tar util-linux \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid ${CODEX_UID} --shell /bin/bash codex

RUN curl -fsSL "https://codeload.github.com/0xTomDaniel/nitride-cli/tar.gz/${NITRIDE_COMMIT}" -o /tmp/nitride.tar.gz \
    && echo "${NITRIDE_SHA256}  /tmp/nitride.tar.gz" | sha256sum -c - \
    && mkdir /opt/nitride \
    && tar -xzf /tmp/nitride.tar.gz -C /opt/nitride --strip-components=3 "nitride-cli-${NITRIDE_COMMIT}/skills/nitride" \
    && rm /tmp/nitride.tar.gz \
    && chmod +x /opt/nitride/scripts/nitride.mjs \
    && ln -s /opt/nitride/scripts/nitride.mjs /usr/local/bin/nitride \
    && node --version && nitride --version

USER codex
ENV HOME=/home/codex
ENV PATH=/home/codex/.local/bin:${PATH}
WORKDIR /workspace

RUN curl -fsSL https://chatgpt.com/codex/install.sh -o /tmp/codex-install.sh \
    && echo "${INSTALLER_SHA256}  /tmp/codex-install.sh" | sha256sum -c - \
    && sh /tmp/codex-install.sh --release "${CODEX_VERSION}" \
    && rm /tmp/codex-install.sh \
    && codex --version

USER root
RUN mkdir -p /opt/codex-seed \
    && cp -a /home/codex/.codex/. /opt/codex-seed/ \
    && chown -R codex:codex /opt/codex-seed
USER codex

COPY --chmod=0755 --chown=codex:codex entrypoint.sh /usr/local/bin/exo-codex-entrypoint
ENTRYPOINT ["/usr/local/bin/exo-codex-entrypoint"]
