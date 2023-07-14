# How to get the backup of the database?

## Activate the environ
$ kubectx gke_milleros_us-west1-c_milleros
$ kubens default

## Extract backup
1. Get the password of the database
export POSTGRES_PASSWORD=$(kubectl get secret --namespace default database-postgresql -o jsonpath="{.data.postgres-password}" | base64 -d)
2. List the databases
kubectl run database-postgresql-client --rm --tty -i --restart='Never' --namespace default --image docker.io/bitnami/postgresql:15.3.0-debian-11-r7 --env="PGPASSWORD=$POSTGRES_PASSWORD" \
      --rm --command -- psql -l --host database-postgresql -U postgres -d postgres -p 5432
3. Get the backup in plain SQL
kubectl run database-postgresql-client --rm --tty -i --restart='Never' --namespace default --image docker.io/bitnami/postgresql:15.3.0-debian-11-r7 --env="PGPASSWORD=$POSTGRES_PASSWORD" \
      --rm --command -- pg_dump --host database-postgresql -U postgres -d trackmilesdb-test -p 5432 > backup.sql
4. Remove the last line of the backup
