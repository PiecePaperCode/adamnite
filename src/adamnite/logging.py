import logging

name = 'adamnite'
formatter = logging.Formatter(
    fmt=' %(name)s :: %(levelname)-8s :: %(message)s'
)
logger = logging.getLogger(name)
logger.setLevel(logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
console.setFormatter(formatter)
logger.addHandler(console)
