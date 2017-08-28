from unittest.mock import patch, MagicMock

from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase

from ..buffer_status_update_block import BufferStatusUpdate


class TestBufferStatusUpdate(NIOBlockTestCase):

    @patch.object(BufferStatusUpdate, '_status_update')
    def test_process_signal(self, mock_post):
        signals = [Signal({'text': 'this is my status update'})]
        blk = BufferStatusUpdate()
        self.configure_block(blk, {})
        blk.start()
        blk.process_signals(signals)
        mock_post.assert_called_once_with(
            {'profile_ids[]': ['[[BUFFER_PROFILE_ID]]'],
             'text': signals[0].text,
             'access_token': blk.access_token()}
        )
        blk.stop()

    @patch.object(BufferStatusUpdate, '_status_update')
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

    @patch.object(BufferStatusUpdate, '_status_update')
    def test_bad_config(self, mock_post):
        signals = [Signal({'text': 'this is my status update'})]
        blk = BufferStatusUpdate()
        self.configure_block(blk, {'text': '{{text+2}}'})
        blk.logger.error = MagicMock()
        blk.start()
        blk.process_signals(signals)
        self.assertEqual(blk.logger.error.call_count, 1)
        self.assertEqual(mock_post.call_count, 0)
        blk.stop()
