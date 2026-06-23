# Gunicorn configuration for memory-constrained environments
bind = "0.0.0.0:5000"

# Use 1-2 workers maximum for 512MB memory constraint
workers = 1

# Preload app before forking workers (loads models once, shared by all workers)
preload_app = True

# Worker class
worker_class = "sync"

# Timeout
timeout = 60

# Access log
accesslog = "-"

# Error log
errorlog = "-"

# Log level
loglevel = "info"

# Max requests to prevent memory creep
max_requests = 1000
max_requests_jitter = 50
