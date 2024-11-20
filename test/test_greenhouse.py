from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock

from mock import GPIO
from mock.seesaw import Seesaw
from src.greenhouse import Greenhouse, GreenhouseError

class TestGreenhouse(TestCase):

    @patch.object(Seesaw, "moisture_read")
    def test_measure_soil_moisture_valid_range(self, mock_moisture_sensor: Mock):
        mock_moisture_sensor.return_value = 300
        gn = Greenhouse()
        m = gn.measure_soil_moisture()
        self.assertEqual(300, m)

    @patch.object(Seesaw, "moisture_read")
    def test_measure_soil_moisture_valid_range(self, mock_moisture_sensor: Mock):
        mock_moisture_sensor.return_value = 299
        gn = Greenhouse()
        self.assertRaises(GreenhouseError, gn.measure_soil_moisture)

    @patch.object(Seesaw, "moisture_read")
    def test_measure_soil_moisture_valid_range(self, mock_moisture_sensor: Mock):
        mock_moisture_sensor.return_value = 501
        gn = Greenhouse()
        self.assertRaises(GreenhouseError, gn.measure_soil_moisture)

    @patch.object(GPIO, "output")
    def test_turn_on_sprinkler(self, mock_sprinkler: Mock):
        gn = Greenhouse()
        gn.turn_on_sprinkler()
        mock_sprinkler.assert_called_once_with(gn.SPRINKLER_PIN, True)
        self.assertTrue(gn.sprinkler_on)

    @patch.object(GPIO, "output")
    def test_turn_off_sprinkler(self, mock_sprinkler: Mock):
        gn = Greenhouse()
        gn.turn_off_sprinkler()
        mock_sprinkler.assert_called_once_with(gn.SPRINKLER_PIN, False)
        self.assertFalse(gn.sprinkler_on)

    @patch.object(Seesaw, "moisture_read")
    @patch.object(GPIO, "output")
    def test_manage_sprinkler_should_be_turned_on_when_below_375(self, mock_sprinkler: Mock, mock_moisture_sensor: Mock):
        mock_moisture_sensor.return_value = 374
        gn = Greenhouse()
        gn.manage_sprinkler()
        mock_sprinkler.assert_called_once_with(gn.SPRINKLER_PIN, True)
        self.assertTrue(gn.sprinkler_on)

    @patch.object(Seesaw, "moisture_read")
    @patch.object(GPIO, "output")
    def test_manage_sprinkler_should_be_turned_on_when_above_425(self, mock_sprinkler: Mock, mock_moisture_sensor: Mock):
        mock_moisture_sensor.return_value = 426
        gn = Greenhouse()
        gn.manage_sprinkler()
        mock_sprinkler.assert_called_once_with(gn.SPRINKLER_PIN, False)
        self.assertFalse(gn.sprinkler_on)



