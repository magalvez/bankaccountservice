"""API success responses"""

from flask import jsonify


class HTTPBase:
    """Base HTTP class"""

    def __init__(self, code):
        """HTTPBase constructor"""

        self.code = code
        self.payload = {}
        self.mimetype = "application/json"

    def get_response(self, payload, mimetype=None):
        """Return Response object"""

        if mimetype is not None:
            self.mimetype = mimetype

        return jsonify(payload)


class HttpSuccess(HTTPBase):
    """HTTP success class"""

    def __init__(self):
        """Return HTTP created response"""

        HTTPBase.__init__(self, 200)


class HttpCreated(HTTPBase):
    """HTTP created class"""

    def __init__(self):
        """Return HTTP created response"""

        HTTPBase.__init__(self, 201)


class HttpNoContent(HTTPBase):
    """HTTP no content class"""

    def __init__(self):
        """Return HTTP no content response"""

        HTTPBase.__init__(self, 204)
