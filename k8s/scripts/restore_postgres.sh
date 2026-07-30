#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "❌ Usage: $0 <backup_file.sql>"
    exit 1
fi

BACKUP_FILE=$1

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Backup file $BACKUP_FILE does not exist!"
    exit 1
fi

echo "🚀 Initiating PostgreSQL Restore to Kubernetes..."

POD_NAME=$(kubectl get pods -n kairos -l app=postgres -o jsonpath="{.items[0].metadata.name}")

if [ -z "$POD_NAME" ]; then
    echo "❌ No PostgreSQL pod found in the 'kairos' namespace."
    exit 1
fi

echo "📦 Found Database Pod: $POD_NAME"
echo "⚠️ WARNING: This will overwrite existing data!"
read -p "Are you sure you want to proceed? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "⏳ Restoring database..."
    kubectl exec -i -n kairos $POD_NAME -- psql -U postgres < $BACKUP_FILE
    echo "✅ Restore completed successfully."
else
    echo "Aborted."
fi
