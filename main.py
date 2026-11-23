import geopandas as gpd
import shapely
from shapely import geometry
import simplekml

gdf = gpd.read_file("data/cb_2018_us_county_500k/cb_2018_us_county_500k.kml")

void_counties = [
    # [state fips, county fips]
    ["27", "053"],
    ["27", "093"],
]

void_circles = [
    # [lat, lon, radius_km]
    [45.655329, -95.218591, 20],
    [44.237812, -95.447679, 10],
    [44.375776, -95.454775, 10],
    [45.82520598723697, -94.75449860800727, 22],

]

void_circles = [[y, x, r] for x, y, r in void_circles]

counties = {
    statefp: group.set_index("COUNTYFP")["geometry"].to_dict()
    for statefp, group in gdf.groupby("STATEFP")
}

polygons = []

for statefp, countyfp in void_counties:
    county_poly = counties[statefp][countyfp]
    polygons.append(county_poly)


for lat, lon, radius_km in void_circles:
    circle = geometry.Point(lat, lon)

    gdf_circles = gpd.GeoDataFrame(
        {"Name": ["x"], "Description": ["x"]}, geometry=[circle], crs="EPSG:4326"
    )

    utm_crs = gdf_circles.estimate_utm_crs()
    gdf_projected = gdf_circles.to_crs(utm_crs)
    gdf_projected["geometry"] = gdf_projected.geometry.buffer(
        1000 * radius_km, quad_segs=64
    )
    gdf_circle = gdf_projected.to_crs("EPSG:4326")
    polygons.extend(gdf_circle.geometry)

polygons = [
    shapely.MultiPolygon([p]) if isinstance(p, shapely.Polygon) else p for p in polygons
]

composite = shapely.union_all(polygons)

gdf_out = gpd.GeoDataFrame(
    {"Name": ["comp"], "Description": ["comp"]}, geometry=[composite], crs="EPSG:4326"
)

gdf_out["OGR_STYLE"] = "BRUSH(fc:#F0F0F0)"
gdf_out.to_file("out.kml", driver="LIBKML")
