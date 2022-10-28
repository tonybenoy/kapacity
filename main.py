import asyncio
import csv
import logging
import os
from typing import Dict, List

import pandas as pd
import plotly.express as px
import typer
from dash import Dash, Input, Output, dcc, html
from httpx import AsyncClient, BasicAuth

from constants import BASE_URL, PASSWORD, USERNAME

logging.basicConfig(level=logging.INFO)
app = typer.Typer()
dash_app = Dash(__name__)
df_global = {}


async def get_data(filename: str) -> Dict[str, List[Dict]]:
    url = BASE_URL + "/json"
    async with AsyncClient(auth=BasicAuth(USERNAME, PASSWORD)) as client:
        response = await client.get(url, params={"filename": filename})
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Error: {response.status_code}")
            return {}


def clean_data(data: List[Dict]) -> List[Dict]:
    clean_data_list = []
    for row in data:
        cleaned_row = {
            "time_stamp": row.get("time_stamp", None),
            "supply_temp": row["Supply temp °C"]
            if isinstance(row.get("Supply temp °C", None), float)
            else None,
            "outdoor_temp": row["Outdoor temperature °C"]
            if isinstance(row.get("Outdoor temperature °C", None), float)
            else None,
            "power_kw": row["Power-sum kW"]
            if isinstance(row.get("Power-sum kW", None), float)
            else None,
        }
        if validate_data(cleaned_row):
            clean_data_list.append(cleaned_row)
    return clean_data_list


def validate_data(dataDict):
    if all(dataDict.values()):
        return True
    else:
        logging.error(f"Error (Missing value): {dataDict}")
        return False


def write_to_csv(data: List[Dict], filename: str, path: str) -> None:
    if not os.path.exists(path):
        os.mkdir(path)

    try:
        with open(f"{path}/{filename}", "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    except IOError:
        logging.error("I/O error")


async def applet(filename: str, path: str, plot: bool, csv: bool):
    data = await get_data(filename=filename)
    if not data:
        logging.error("No data received")
        return
    cleaned_data = clean_data(data["data"])
    if csv:
        write_to_csv(cleaned_data, f"{filename}.csv", path=path)
    if plot:
        df = pd.DataFrame(cleaned_data)
        df_global.update({filename: df})


@dash_app.callback(Output("time-series-chart", "figure"), Input("file", "value"))
def display_time_series(file):
    df = df_global[file]
    fig = px.line(df, x="time_stamp", y=df.columns)
    return fig


@app.command()
def main(
    files: List[str] = typer.Argument(...),
    path: str = typer.Option("./out"),
    csv: bool = typer.Option(True),
    plot: bool = typer.Option(True),
):
    if not plot and not csv:
        logging.error("Please select atleast one option")
        typer.Exit(1)
    if plot:
        dash_app.layout = html.Div(
            [
                html.H4("Kapacity"),
                dcc.Graph(id="time-series-chart"),
                html.P("Select File:"),
                dcc.Dropdown(
                    id="file",
                    options=files,
                    value=files[0],
                    clearable=False,
                ),
            ]
        )
    for file in files:
        if ".json" in file:
            file = file.split(".json")[0]
        asyncio.run(applet(filename=file, path=path, plot=plot, csv=csv))
    if plot:
        dash_app.run_server(debug=True)


if __name__ == "__main__":
    app()
