FROM odoo:16

USER root

# Atualizar e instalar dependências
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    gettext-base \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python
RUN pip install --upgrade pip
RUN pip install pypdf

# Copiar módulos personalizados
COPY ./odoo/addons /mnt/extra-addons/

# Copiar template de configuração
COPY ./railway-odoo.conf.template /etc/odoo/odoo.conf.template

# Criar script de inicialização
RUN cat <<'EOF' > /start-odoo.sh
#!/bin/bash
set -e

# Aguardar banco estar disponível
echo "Aguardando PostgreSQL..."
while ! pg_isready -h "${PGHOST}" -p "${PGPORT}" -U "${ODOO_DB_USER}" >/dev/null 2>&1; do
    sleep 2
done
echo "PostgreSQL disponível!"

# Substituir variáveis de ambiente no arquivo de configuração
envsubst < /etc/odoo/odoo.conf.template > /etc/odoo/odoo.conf

# Iniciar Odoo
exec odoo -c /etc/odoo/odoo.conf --without-demo=all "$@"
EOF

RUN chmod +x /start-odoo.sh

# Criar diretório para logs
RUN mkdir -p /var/log/odoo && chown odoo:odoo /var/log/odoo

USER odoo

# Expor porta
EXPOSE 8069

# Comando de inicialização
CMD ["/start-odoo.sh"]
