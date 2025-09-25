#!/bin/bash
set -e

# Substituir variáveis de ambiente no arquivo de configuração
envsubst < /etc/odoo/odoo.conf.template > /etc/odoo/odoo.conf

# Mostrar variáveis de ambiente no log (para debug)
echo "========================================"
echo "🔧 Variáveis de ambiente para Odoo"
echo "PGHOST=$PGHOST"
echo "PGPORT=$PGPORT"
echo "ODOO_DB_NAME=$ODOO_DB_NAME"
echo "ODOO_DB_USER=$ODOO_DB_USER"
# Não exibir senha inteira por segurança, apenas tamanho
if [ -n "$ODOO_DB_PASSWORD" ]; then
  echo "ODOO_DB_PASSWORD=*** (tamanho: ${#ODOO_DB_PASSWORD})"
else
  echo "ODOO_DB_PASSWORD= (vazio)"
fi
echo "========================================"

echo "Aguardando PostgreSQL..."
until pg_isready -h "$PGHOST" -p "$PGPORT" -U "$ODOO_DB_USER"; do
  sleep 2
done
echo "PostgreSQL disponível!"

# Verificar se o banco já foi inicializado
echo "Verificando se o banco já foi inicializado..."
if psql "postgresql://$ODOO_DB_USER:$ODOO_DB_PASSWORD@$PGHOST:$PGPORT/$ODOO_DB_NAME" \
   -c "\dt" | grep -q "ir_module_module"; then
  echo "✅ Banco já inicializado. Subindo Odoo normalmente..."
  exec odoo -c /etc/odoo/odoo.conf --without-demo=all "$@"
else
  echo "⚡ Banco vazio. Inicializando com módulo base..."
  exec odoo -c /etc/odoo/odoo.conf -i base --without-demo=all "$@"
fi
