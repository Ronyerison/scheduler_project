FROM odoo:16

USER root

# Atualizar e instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    gettext-base \
    postgresql-client \
    nginx \
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

# Copiar config do nginx
COPY ./nginx.conf /etc/nginx/nginx.conf

# Criar diretório para logs e cache do nginx
RUN mkdir -p /var/log/odoo /var/lib/nginx /tmp/nginx \
    && chown -R odoo:odoo /var/log/odoo /var/lib/nginx /tmp/nginx

USER odoo

# Expor porta pública
EXPOSE 80

# Comando de inicialização padrão
CMD ["/start-odoo.sh"]
