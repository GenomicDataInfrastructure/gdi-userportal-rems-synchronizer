# SPDX-FileCopyrightText: 2024 PNED G.I.E.
#
# SPDX-License-Identifier: Apache-2.0

FROM registry.access.redhat.com/ubi9/python-312-minimal:9.6-1751461507
USER 0

WORKDIR /app

# Update system packages to fix security vulnerabilities
RUN microdnf update -y && microdnf clean all

COPY src/ /app
COPY data/ /app/data/
COPY requirements.txt /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.2.33/supercronic-linux-amd64 \
    SUPERCRONIC=supercronic-linux-amd64

RUN curl -fsSLO "$SUPERCRONIC_URL" \
    && chmod +x "$SUPERCRONIC" \
    && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
    && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic

RUN chown -R 1001:1001 ./

USER 1001

CMD ["/usr/local/bin/supercronic", "-debug", "/app/crontab"]
