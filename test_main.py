import pytest

from main import applet, clean_data, validate_data

sample_resp = {
    "data": [
        {
            "device_id": "11111",
            "units_on": 2,
            "dhw_tank_temp": -5351.717145515211,
            "dhw_start_temp": 510,
            "dhw_stop_temp": 550,
            "time_stamp": "2022-10-19T19:05:00+00:00",
            "Set point °C": "error",
            "Supply temp °C": "error",
            "Outdoor temperature °C": 4.235353479481707,
            "Power-sum kW": 10.687525334984365,
            "heat_value": 43.79768744250489,
        },
        {
            "device_id": "11111",
            "dhw_tank_temp": 53.02592624959721,
            "dhw_start_temp": 510,
            "dhw_stop_temp": 550,
            "time_stamp": "2022-10-19T19:00:00+00:00",
            "Set point °C": 35.79999923706055,
            "Supply temp °C": 32.33535419810902,
            "Outdoor temperature °C": 4.064646402994792,
            "Power-sum kW": 3.8331649639088696,
            "heat_value": 9.919311055704682,
        },
    ]
}


@pytest.mark.asyncio
async def test_applet(mocker):
    mocker.patch("main.get_data", return_value=sample_resp)
    filename = "data"
    path = "./out_test"
    plot = True
    csv = True
    resp = await applet(filename, path, plot, csv)
    assert resp is None


def test_clean_data():
    data = sample_resp["data"]
    resp = clean_data(data)
    assert len(resp) == 1


def test_validate_data():
    data = sample_resp["data"][0]
    for key, value in data.items():
        if value == "error":
            data[key] = None
    resp = validate_data(data)
    assert resp is False


def test_validate_data_valid():
    data = sample_resp["data"][1]
    for key, value in data.items():
        if value == "error":
            data[key] = None
    resp = validate_data(data)
    assert resp is True
