import logging
import json
from datetime import datetime

from zExceptions.ExceptionFormatter import format_exception
from AccessControl.SecurityManagement import getSecurityManager

from edw.logger.util import get_ip


logger = logging.getLogger("edw.logger")


def error_logger(self, info):
    strtype = str(getattr(info[0], '__name__', info[0]))
    if strtype in self._ignored_exceptions:
        return

    if not isinstance(info[2], basestring):
        tb_text = ''.join(
            format_exception(*info, **{'as_html': 0}))
    else:
        tb_text = info[2]

    url = None
    username = None
    request = getattr(self, 'REQUEST', None)
    if request:
        user = getSecurityManager().getUser()
        url = request.get("URL", None)
        username = user.getUserName()

    data = {
        "IP": get_ip(request),
        "User": username,
        "Date": datetime.now().isoformat(),
        "Type": "Error",
        "URL": url,
        "ErrorType": strtype,
        "Traceback": tb_text,
    }

    logger.info(json.dumps(data))


def error_wrapper(meth):
    """Log errors"""

    def extract(self, *args, **kwargs):
        error_logger(self, *args, **kwargs)
        return meth(self, *args, **kwargs)

    return extract


from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
SiteErrorLog.orig_raising = SiteErrorLog.raising
SiteErrorLog.raising = error_wrapper(SiteErrorLog.raising)
