BufferStatusUpdate
==================

Create a new Buffer status update for each input signal. Uses the [/updates/create API](https://bufferapp.com/developers/api/updates#updatescreate).

Properties
----------
- **access_token**: Buffer API Access Token.
- **profile_ids**: An array of profile id's that the status update should be sent to. Invalid `profile_id's` will be silently ignored.
- **text**: The status update text.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
None

Commands
--------
None

Dependencies
------------
-   [requests](https://pypi.python.org/pypi/requests/)
