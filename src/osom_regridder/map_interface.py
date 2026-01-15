"""
A module that exposes an interface to create and read from a precomputed grid
map in the form of a SQLite file.

Functions:
  initialize_grid: Creates an initialized Sqlite DB.
  close: Closes connection to the DB.
  save_distances: Saves computed distances into initialized DB.
  load_grid: Loads a grid file for quering.
  get_distances: Returns the distances for a point from a grid file.
"""

import numpy as np
import sqlite3

CREATE_GRID_SCHEMA = """BEGIN;

CREATE TABLE IF NOT EXISTS "distances" (
	"output_x" INTEGER NOT NULL,
	"output_y" INTEGER NOT NULL,
	"model_x" INTEGER NOT NULL,
	"model_y" INTEGER NOT NULL,
	"distance" REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS "sizes" (
    "x" INTEGER NOT NULL,
    "y" INTEGER NOT NULL,
    "width" REAL NOT NULL,
    "height" REAL NOT NULL,
    "size" REAL NOT NULL
);

COMMIT;
"""

INSERT_DISTANCE_VALUE_TEMPLATE = 'INSERT INTO "distances" VALUES(?, ?, ?, ?, ?)'
INSERT_SIZE_VALUE_TEMPLATE = 'INSERT INTO "sizes" VALUES(?, ?, ?, ?, ?)'
GET_DISTANCES_TEMPlATE = 'SELECT "model_x", "model_y", "distance" FROM "distances" WHERE "output_x" = ? AND "output_y" = ?'
GET_SIZE_TEMPlATE = 'SELECT "size" FROM "sizes" WHERE "x" = ? AND "y" = ?'


def initialize_grid(
    grid_file_name: str,
):
    connection = sqlite3.connect(grid_file_name)
    cursor = connection.cursor()
    cursor.executescript(CREATE_GRID_SCHEMA)
    return connection


def save_distances(
    connection: sqlite3.Connection, output_x: int, output_y: int, distances: np.ndarray
):
    """
    distances is an array for ONE OUTPUT GRID INDEX
    """
    cursor = connection.cursor()
    rows = []
    for i in range(len(distances)):
        model_x, model_y, distance = distances[i]
        rows.append(
            (
                output_x,
                output_y,
                model_x,
                model_y,
                distance,
            )
        )
    result = cursor.executemany(INSERT_DISTANCE_VALUE_TEMPLATE, rows)
    connection.commit()

def save_sizes(
    connection: sqlite3.Connection, sizes: list[tuple[int, int, int, int, int]]
):
    """
    distances is an array for ONE OUTPUT GRID INDEX
    """
    cursor = connection.cursor()
    result = cursor.executemany(INSERT_SIZE_VALUE_TEMPLATE, sizes)
    connection.commit()


def load_grid(grid_file_name: str):
    connection = sqlite3.connect(grid_file_name)
    cursor = connection.cursor()
    return connection


def get_distances(connection: sqlite3.Connection, output_x: int, output_y: int):
    cursor = connection.cursor()
    cursor.execute(GET_DISTANCES_TEMPlATE, (output_x, output_y))
    distances = cursor.fetchall()
    return distances


def close(connection: sqlite3.Connection):
    connection.close()


if __name__ == "__main__":
    pass
