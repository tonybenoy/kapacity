# Kapacity
A CLI tool to get API response from kapacity endpoint and generate CSV and graphs based on the response.

## Installation
The dependencies are managed by [Poetry](https://python-poetry.org/). To install the dependencies, run the following command:
```bash
poetry install
```

## Usage
To get the possible options, run the following command:
```bash
poetry run main.py --help
```
The CLI tool takes in file names as a required argument and path as optional argument. The path defaults out directory to the current directory. The file names are the names of the files passed to the API. The CLI tool generates a CSV file and a graph for each file. The CSV file and the graph contains the data from the API response after removing incorrect values.

The graph is available [here](http://localhost:8050/)

## Testing
To run the tests, run the following command:
```bash
poetry run pytest
```
