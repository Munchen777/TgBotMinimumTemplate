from loguru import logger


my_logger = logger
my_logger.add('async_log.log', format='{time} {level} {message}', level='INFO',
               rotation='10 MB', colorize=True)
