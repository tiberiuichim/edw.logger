Installation
============

::

    [instance]
    ...
    eggs =
        ...
        edw.logger
    zcml =
        ...
        edw.logger


Introduction
============

This package creates a new `edw.logger` log facility that logs to
INFO and ERROR the following events:

    * Login (not available for default Zope ACL)
    * Viewed pages
    * Added/Created content
    * Copied/Moved/Deleted content
    * ZODB commits
    * Raised errors
