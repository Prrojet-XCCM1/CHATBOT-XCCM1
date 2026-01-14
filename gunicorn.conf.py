import multiprocessing

# Nombre de workers
workers = multiprocessing.cpu_count() * 2 + 1

# Configuration des workers
worker_class = 'sync'  # Pour Flask standard
threads = 2

# Timeouts
timeout = 120
keepalive = 5

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Pour le plan gratuit de Render
bind = f"0.0.0.0:{os.environ.get('PORT', 5000)}"