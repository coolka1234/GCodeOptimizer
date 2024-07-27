from local_logging import logger
def read_nc_file(file_path):
    if not file_path.endswith('.nc'):
        logger.error("The file is not a .nc file")
        raise ValueError("The file is not a .nc file")
    logger.debug(f"Reading file {file_path}")
    counter=1
    with open(file_path, 'r', encoding='cp1250') as file:
        for line in file:
            logger.debug(f"Line {counter}: {line}")
            counter+=1
            yield line