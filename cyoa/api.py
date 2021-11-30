import attr

@attr.s
class SendMailRequest(object):
    to: str = attr.ib()
    recommendation: str = attr.ib()
    source: str = attr.ib()

@attr.s
class SendMailResponse(object):
    success: bool = attr.ib()
    error_message: str = attr.ib()