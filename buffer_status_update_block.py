import requests
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties.expression import ExpressionProperty
from nio.metadata.properties.list import ListProperty
from nio.metadata.properties.string import StringProperty
from nio.metadata.properties.holder import PropertyHolder
from nio.common.block.base import Block


POST_URL = "https://api.bufferapp.com/1/updates/create.json"


class ProfileID(PropertyHolder):
    profile_id = StringProperty(default='[[BUFFER_PROFILE_ID]]',
                                title='Profile ID')


@Discoverable(DiscoverableType.block)
class BufferStatusUpdate(Block):

    text = ExpressionProperty(default='{{$text}}',
                              title='Status Update Text')
    profile_ids = ListProperty(ProfileID, default=[ProfileID()],
                               title='Profile IDs')
    access_token = StringProperty(default='[[BUFFER_ACCESS_TOKEN]]',
                                  title='Access Token')

    def process_signals(self, signals):
        for s in signals:
            try:
                text = self.text(s)
            except Exception as e:
                self._logger.error(
                    "Text evaluation failed: {0}: {1}".format(
                        type(e).__name__, str(e))
                )
                continue
            data = {'access_token': self.access_token,
                    'text': text,
                    'profile_ids[]': [pid.profile_id for pid in self.profile_ids]}
            self._status_update(data)

    def _status_update(self, payload):
        response = requests.post(POST_URL, data=payload)
        status = response.status_code
        if status != 200:
            self._logger.error(
                "Buffer Status Update to {} with text '{}' "
                "failed with status {}".format(
                    payload['profile_ids[]'],
                    payload['text'],
                    status
                )
            )
        else:
            self._logger.debug(
                "Buffer Status Update to {} with text '{}'".format(
                    payload['profile_ids[]'],
                    payload['text']
                )
            )
