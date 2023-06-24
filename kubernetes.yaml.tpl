apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: milleros-client
  name: milleros-client
  namespace: milleros-test
spec:
  replicas: 1
  selector:
    matchLabels:
      app: milleros-client
  template:
    metadata:
      labels:
        app: milleros-client
    spec:
      containers:
      - image: gcr.io/milleros/client:COMMIT_SHA
        name: client
        ports:
        - containerPort: 80 
---
apiVersion: v1
kind: Service
metadata:
  name: milleros-client
  namespace: milleros-test
spec:
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
  selector:
    app: milleros-client
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: milleros-test
  namespace: milleros-test
  annotations: 
    cert-manager.io/issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - test.milleros.com.ar
    secretName: milleros-production-tls
  rules:
  - host: test.milleros.com.ar
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: milleros-client
            port:
              number: 80
---
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: letsencrypt-staging
  namespace: milleros-test
spec:
  acme:
    # The ACME server URL
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    # Email address used for ACME registration
    email: infra@milleros.com.ar
    # Name of a secret used to store the ACME account private key
    privateKeySecretRef:
      name: letsencrypt-staging
    # Enable the HTTP-01 challenge provider
    solvers:
      - http01:
          ingress:
            ingressClassName: nginx
---
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: letsencrypt-prod
  namespace: milleros-test
spec:
  acme:
    # The ACME server URL
    server: https://acme-v02.api.letsencrypt.org/directory
    # Email address used for ACME registration
    email: infra@milleros.com.ar
    # Name of a secret used to store the ACME account private key
    privateKeySecretRef:
      name: letsencrypt-prod
    # Enable the HTTP-01 challenge provider
    solvers:
      - http01:
          ingress:
            ingressClassName: nginx
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: milleros-vars
  namespace: milleros-test
data:
  DJANGO_CONFIGURATION: Dev
  SQL_ENGINE: django.db.backends.postgresql
  SQL_DATABASE: trackmilesdb-test
  SQL_USER: postgres
  SQL_PASSWORD: postgres
  SQL_HOST: database-postgresql.default.svc.cluster.local
  SQL_PORT: '5432'
  DJANGO_ALLOWED_HOSTS: localhost;127.0.0.1;server;localhost;backend-trackmiles.ovh001.eynes.com.ar;[::1];test.milleros.com.ar;test.milleros.com.ar
  DJANGO_CORS_ALLOWED_ORIGINS: https://test.milleros.com.ar
  DJANGO_SECRET_KEY: foo
  DJANGO_CSRF_TRUSTED_ORIGINS: https://api.test.milleros.com.ar;https://test.milleros.com.ar
  DJANGO_SECRET_KEY: django-insecure-key
  DJANGO_CELERY_BROKER_URL: redis://redis:6379/0
  DJANGO_CELERY_RESULT_BACKEND: redis://redis:6379/0
  CELERY_BROKER_URL: redis://redis:6379/0
  CELERY_RESULT_BACKEND: redis://redis:6379/0
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: milleros-server
  name: milleros-server
  namespace: milleros-test
spec:
  replicas: 1
  selector:
    matchLabels:
      app: milleros-server
  template:
    metadata:
      labels:
        app: milleros-server
    spec:
      initContainers:
      - image: gcr.io/milleros/server:COMMIT_SHA
        name: init
        command: ["python3", "manage.py", "migrate"]
        envFrom:
        - configMapRef:
            name: milleros-vars
        env:
          - name: SQL_PASSWORD
            valueFrom:
              secretKeyRef:
                name: database-postgresql
                key: postgres-password
      containers:
      - image: gcr.io/milleros/server:COMMIT_SHA
        name: server
        envFrom:
        - configMapRef:
            name: milleros-vars
        env:
          - name: SQL_PASSWORD
            valueFrom:
              secretKeyRef:
                name: database-postgresql
                key: postgres-password
        command: ["gunicorn", "server.wsgi:application", "--bind", "0.0.0.0:8000"]
      - image: gcr.io/milleros/server:COMMIT_SHA
        name: celery
        envFrom:
        - configMapRef:
            name: milleros-vars
        env:
          - name: SQL_PASSWORD
            valueFrom:
              secretKeyRef:
                name: database-postgresql
                key: postgres-password
        command: ["celery", "-A", "server", "worker", "-l", "INFO", "-E"]
      - image: gcr.io/milleros/server:COMMIT_SHA
        name: celery-beats
        envFrom:
        - configMapRef:
            name: milleros-vars
        env:
          - name: SQL_PASSWORD
            valueFrom:
              secretKeyRef:
                name: database-postgresql
                key: postgres-password
        command: ["celery", "-A", "server", "beat", "--scheduler", "django_celery_beat.schedulers:DatabaseScheduler"]
      - image: gcr.io/milleros/server:COMMIT_SHA
        name: celery-flower
        envFrom:
        - configMapRef:
            name: milleros-vars
        env:
          - name: SQL_PASSWORD
            valueFrom:
              secretKeyRef:
                name: database-postgresql
                key: postgres-password
        command: ["celery", "-A", "server", "flower", "--address=0.0.0.0", "--port=5555"]
---
apiVersion: v1
kind: Service
metadata:
  name: milleros-server
  namespace: milleros-test
spec:
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
  selector:
    app: milleros-server
---
apiVersion: v1
kind: Service
metadata:
  name: milleros-server-flower
  namespace: milleros-test
spec:
  ports:
  - port: 5555
    targetPort: 5555
    protocol: TCP
  selector:
    app: milleros-server
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: milleros-backend
  namespace: milleros-test
  annotations: 
    cert-manager.io/issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - api.test.milleros.com.ar
    secretName: milleros-server-production-tls
  rules:
  - host: api.test.milleros.com.ar
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: milleros-server
            port:
              number: 80
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: milleros-backend-flower
  namespace: milleros-test
  annotations: 
    cert-manager.io/issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rewrite-target: "/"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - flower.test.milleros.com.ar
    secretName: milleros-server-flower-production-tls
  rules:
  - host: flower.test.milleros.com.ar
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: milleros-server-flower
            port:
              number: 5555
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: redis
  name: redis
  namespace: milleros-test
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - image: redis
        name: redis
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: redis
  name: redis
  namespace: milleros-test
spec:
  ports:
  - port: 6379
    protocol: TCP
    targetPort: 6379
  selector:
    app: redis
