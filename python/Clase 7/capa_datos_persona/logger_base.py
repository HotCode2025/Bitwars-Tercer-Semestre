import logging as log

log.basicConfig(
    level=log.DEBUG,
    format='%(asctime)s:%(levelname)s [%(filename)s:%(lineno)s] %(message)s',
    datefmt='%I:%M:%S %p',
    handlers=[
        log.FileHandler('capa_datos.log'), # Archivo para guardar logs
        log.StreamHandler()
    ]
)

if __name__ == '__main__':

    # Mensaje por defecto
    log.basicConfig(level=log.DEBUG)

    log.debug("Mensaje a nivel DEBUG")
    log.info("Mensaje a nivel INFO")
    log.warning("Mensaje a nivel WARNING")
    log.error("Mensaje a nivel ERROR")
    log.critical("Mensaje a nivel CRITICAL")