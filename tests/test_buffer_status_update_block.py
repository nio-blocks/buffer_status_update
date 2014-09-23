from unittest.mock import patch, MagicMock
from ..buffer_status_update_block import BufferStatusUpdate
from nio.common.signal.base import Signal
from nio.util.support.block_test_case import NIOBlockTestCase


class TestBufferStatusUpdate(NIOBlockTestCase):

    @patch('buffer_status_update.buffer_status_update_block.'
           'BufferStatusUpdate._status_update')
    def test_process_signal(self, mock_post):
        signals = [Signal({'text': 'this is my status update'})]
        blk = BufferStatusUpdate()
        self.configure_block(blk, {})
        blk.start()
        blk.process_signals(signals)
        mock_post.assert_called_once_with(
            {'profile_ids[]': ['[[BUFFER_PROFILE_ID]]'],
             'text': signals[0].text,
             'access_token': blk.access_token}
        )
        blk.stop()

    @patch('buffer_status_update.buffer_status_update_block.'
           'BufferStatusUpdate._status_update')
    def test_process_multiple(self, mock_post):
        signals = [
            Signal({'text': 'this is my status update'}),
            Signal({'text': 'this is also my status update'})
        ]
        blk = BufferStatusUpdate()
        self.configure_block(blk, {})
        blk.start()
        blk.process_signals(signals)
        self.assertEqual(mock_post.call_count, len(signals))
        blk.stop()

    @patch('buffer_status_update.buffer_status_update_block.'
           'BufferStatusUpdate._status_update')
    def test_bad_config(self, mock_post):
        signals = [Signal({'text': 'this is my status update'})]
        blk = BufferStatusUpdate()
        self.configure_block(blk, {'text': '{{text+2}}'})
        blk._logger.error = MagicMock()
        blk.start()
        blk.process_signals(signals)
        self.assertEqual(blk._logger.error.call_count, 1)
        self.assertEqual(mock_post.call_count, 0)
        blk.stop()
