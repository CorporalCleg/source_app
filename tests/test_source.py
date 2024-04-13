from fastapi.testclient import TestClient
from source.main import app
from tests.dummy import *
import pytest, unittest.mock

client = TestClient(app)


#test http commands
class TestRequests:

    def test_measure(self):
        response = client.get("/MEASURE")
        assert response.status_code == 200
        for i in range(4):
            assert response.json()[i] == {"state": 0, "current": 0.0,  "voltage": 0.0, "power": 0.0}
        

    def test_turn_on(self):
        response = client.get("/SOURCE/2?current=2&voltage=1")
        assert response.status_code == 200
        assert response.json()['action'] == f'turn on channel # {2}'

    def test_turn_off(self):
        response = client.get("/OUTPUT/2")
        assert response.status_code == 200
        assert response.json()['action'] == f'turn off channel # {2}'

#test tcp commands
class TestSending:

    
    @pytest.mark.parametrize(
        "channel, current, voltage",
        [
            (0, 1.4, 2),
            (1, 2.4, 2.13),
            (2, 5.3, 54.1),
            (3, 0.5, 1.0)
        ]
    )
    @unittest.mock.patch('socket.socket', StubSocket)
    @pytest.mark.asyncio
    async def test_turn_on(self, channel, current, voltage):
        await client.app.communicator.turn_on((channel, voltage, current))
        received_data = client.app.communicator.s.received_data
        assert received_data[0].decode() == f':SOURce{channel}:CURRent {current}\n' and \
        received_data[1].decode() == f':SOURce{channel}:VOLTage {voltage}\n' and \
        received_data[2].decode() == f':OUTPut{channel}:STATe ON\n'

    
    @pytest.mark.parametrize(
        "channel",
        [
            0,
            1,
            2,
            3
        ]
    )
    @unittest.mock.patch('socket.socket', StubSocket)
    @pytest.mark.asyncio
    async def test_turn_off(self, channel):
        await client.app.communicator.turn_off(channel)
        received_data = client.app.communicator.s.received_data
        assert received_data[0].decode() == f':OUTPut{channel}:STATe OFF\n' and \
        received_data[1].decode() == f':MEASure{channel}:ALL?\n'

    @pytest.mark.parametrize(
        "channel",
        [
            0,
            1,
            2,
            3
        ]
    )
    @unittest.mock.patch('socket.socket', StubSocket)
    def test_get_measurements(self, channel):
        client.app.communicator.get_data(channel)
        received_data = client.app.communicator.s.received_data
        assert received_data[0].decode() == f':MEASure{channel}:ALL?\n'

#test proceeding
class TestProceeding:
    @pytest.mark.parametrize(
        "channel",
        [
            0,
            1,
            2,
            3
        ]
    )
    @unittest.mock.patch('socket.socket', StubSocket)
    def test_get_measurements(self, channel):
        client.app.communicator.get_data(channel)
        assert client.app.communicator.telem[channel] == {"state": 0, "current": 3,  "voltage": 2, "power": 6}