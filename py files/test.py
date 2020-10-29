import logging
logging.basicConfig()
log = logging.getLogger()
fil=logging.FileHandler('log.txt')
log.addHandler(fil)
log.setLevel(logging.ERROR)

i=0
while True:
    log.error(i)
    i=i+1
