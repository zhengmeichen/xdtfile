from logging import getLogger, handlers, Formatter


def logger(name,
           level='INFO',
           format='[%(levelname)s:%(asctime)s:%(filename)s-%(funcName)s@%(lineno)s] %(message)s',
           datefmt='%Y-%b-%d %H:%M:%S'):
  logger = getLogger(name)
  hdlr = handlers.TimedRotatingFileHandler('log/%s.log' % name, when='d', interval=1, backupCount=10, encoding='utf8')
  fmt = Formatter(format, datefmt)
  hdlr.setFormatter(fmt)
  logger.addHandler(hdlr)
  logger.setLevel(level)
  return logger

  # %(name)s            Name of the logger (logging channel)
  # %(levelno)s         Numeric logging level for the message (DEBUG, INFO,
  #                     WARNING, ERROR, CRITICAL)
  # %(levelname)s       Text logging level for the message ("DEBUG", "INFO",
  #                     "WARNING", "ERROR", "CRITICAL")
  # %(pathname)s        Full pathname of the source file where the logging
  #                     call was issued (if available)
  # %(filename)s        Filename portion of pathname
  # %(module)s          Module (name portion of filename)
  # %(lineno)d          Source line number where the logging call was issued
  #                     (if available)
  # %(funcName)s        Function name
  # %(created)f         Time when the LogRecord was created (time.time()
  #                     return value)
  # %(asctime)s         Textual time when the LogRecord was created
  # %(msecs)d           Millisecond portion of the creation time
  # %(relativeCreated)d Time in milliseconds when the LogRecord was created,
  #                     relative to the time the logging module was loaded
  #                     (typically at application startup time)
  # %(thread)d          Thread ID (if available)
  # %(threadName)s      Thread name (if available)
  # %(process)d         Process ID (if available)
  # %(message)s         The result of record.getMessage(), computed just as
  #                     the record is emitted
