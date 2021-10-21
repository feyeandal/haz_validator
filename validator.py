import os
import geopandas as gpd
import pandas as pd

def shapefile_validator():
    """
    Validates the shapefiles according to its geometries, attributes, and projections.
    """

    # Initialize empty dataframes
    geom_check = []
    attribute_check = []
    prj_check = []

    # Observed variants of hazard attributes
    haz_cols = ['Var', 'VAR', 'SS', 'GRIDCODE', 'LH']

    for shp in shp_files:
        # Gets the geometry of the shapefiles
        geometry = gpd.read_file(shp).geometry

        # Reads the shapefiles
        data = gpd.read_file(shp)

        # Checks if the shapefile contains a haz col given the different observed variants of haz columns
        for haz in haz_cols:
            if haz in data:
                attribute_check.append(True)
                break
        else:
            attribute_check.append(False)
        
        # Checks if shapefile has GCS projection (Correct = epsg:4326)
        prj = gpd.read_file(shp).crs
        if prj == 'epsg:4326':
            prj_check.append(True)
        else:
            prj_check.append(False)
        
        # Checks if the shapefile has empty geometries
        geom_series = gpd.GeoSeries(geometry)
        if geom_series.shape[0] > 0:
            geom_check.append(True)
        else:
            geom_check.append(False)

    validator = pd.DataFrame(data=zip(hazard_name, geom_check, attribute_check, prj_check),columns=['hazard name', 'contains geometry', 'correct attribute', 'GCS prj'])
    validator.to_csv('results_validation.csv', index=None, encoding="utf-8")
    print(validator)

if __name__ == '__main__':
    # Path to directories
    path_to_dir = os.path.dirname(os.path.abspath('__file__'))
    input_files = os.listdir(path_to_dir)

    # Gets only the .shp
    shp_files = [ file for file in input_files if file.endswith(".shp") ]

    # Extracts the hazard name (from the filename)
    hazard_name = [ shp.replace(".shp", "") for shp in shp_files ]

    shapefile_validator()