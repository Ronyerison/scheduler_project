FROM odoo:16

USER root

# Atualiza e instala pacotes mínimos para Python
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Instala pypdf
RUN pip install --upgrade pip
RUN pip install pypdf

USER odoo

WORKDIR /mnt/scheduler_project