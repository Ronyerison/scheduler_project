FROM odoo:16

USER root

# Atualizar e instalar dependências
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Instalar pypdf (sua dependência)
RUN pip install --upgrade pip
RUN pip install pypdf

# Copiar módulos personalizados
COPY ./odoo/addons /mnt/extra-addons/

# Copiar configuração para Railway
COPY ./railway-odoo.conf /etc/odoo/odoo.conf

# Criar diretório para logs
RUN mkdir -p /var/log/odoo && chown odoo:odoo /var/log/odoo

USER odoo

# Expor porta
EXPOSE 8069

# Comando de inicialização
CMD ["odoo", "-c", "/etc/odoo/odoo.conf"]