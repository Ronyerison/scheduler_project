FROM odoo:16

USER root

# Atualizar e instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    gettext-base \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python
RUN pip install --upgrade pip
RUN pip install pypdf

# Copiar módulos personalizados
COPY ./odoo/addons /mnt/extra-addons/

# Copiar template de configuração
COPY ./railway-odoo.conf.template /etc/odoo/odoo.conf.template

# Copiar script de inicialização
COPY ./start-odoo.sh /start-odoo.sh
RUN chmod +x /start-odoo.sh

# Criar diretório para logs
RUN mkdir -p /var/log/odoo && chown odoo:odoo /var/log/odoo

USER odoo

# Expor porta
EXPOSE 8069

# Comando de inicialização padrão
CMD ["/start-odoo.sh"]
