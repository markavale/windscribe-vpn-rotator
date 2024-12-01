import pytest
from unittest.mock import patch, MagicMock
from src.windscribe import Windscribe
from src.windscribe_singleton import WindscribeSingleton
import subprocess

@pytest.fixture
def mock_subprocess():
    with patch('subprocess.Popen') as mock_popen, \
         patch('subprocess.run') as mock_run:
        # Configure mock for Popen
        process_mock = MagicMock()
        process_mock.returncode = 0
        process_mock.communicate.return_value = ('Success', None)
        mock_popen.return_value = process_mock
        
        # Configure mock for run
        run_mock = MagicMock()
        run_mock.stdout = b'Connect state: Connected\nIP: 1.2.3.4'
        run_mock.returncode = 0
        mock_run.return_value = run_mock
        
        yield {
            'popen': mock_popen,
            'run': mock_run,
            'process': process_mock
        }

class TestWindscribe:
    @pytest.fixture
    def windscribe(self):
        return Windscribe('test_user', 'test_pass')

    def test_login(self, windscribe, mock_subprocess):
        """Test that login method calls subprocess with correct arguments"""
        assert mock_subprocess['popen'].called
        mock_subprocess['popen'].assert_called_with(
            ['windscribe-cli', 'login'],
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    def test_connect(self, windscribe, mock_subprocess):
        """Test connect method with default parameters"""
        windscribe.connect()
        mock_subprocess['run'].assert_called_with(
            'windscribe-cli connect',
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    def test_disconnect(self, windscribe, mock_subprocess):
        """Test disconnect method"""
        windscribe.disconnect()
        mock_subprocess['run'].assert_called_with(
            'windscribe-cli disconnect',
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

class TestWindscribeSingleton:
    @pytest.fixture
    def windscribe_singleton(self):
        return WindscribeSingleton()

    def test_singleton_pattern(self):
        """Test that WindscribeSingleton follows singleton pattern"""
        instance1 = WindscribeSingleton()
        instance2 = WindscribeSingleton()
        assert instance1 is instance2

    def test_get_status(self, windscribe_singleton, mock_subprocess):
        """Test get_status method parses output correctly"""
        mock_subprocess['run'].return_value.stdout = b'Connect state: Connected\nIP: 1.2.3.4'
        status = windscribe_singleton.get_status()
        assert status == {
            'Connect state': 'Connected',
            'IP': '1.2.3.4'
        }

    def test_parse_status(self, windscribe_singleton):
        """Test parse_status method"""
        test_output = b'Connect state: Connected\nIP: 1.2.3.4\nLocation: US East'
        parsed = windscribe_singleton.parse_status(test_output)
        assert parsed == {
            'Connect state': 'Connected',
            'IP': '1.2.3.4',
            'Location': 'US East'
        }

    @patch('time.sleep')  # Mock sleep to speed up tests
    def test_connect(self, mock_sleep, windscribe_singleton, mock_subprocess):
        """Test connect method"""
        windscribe_singleton.connect()
        assert mock_subprocess['run'].called 