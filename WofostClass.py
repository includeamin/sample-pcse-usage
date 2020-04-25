from pcse.base_classes import ParameterProvider
from pcse.fileinput import CABOFileReader
from pcse.fileinput import YAMLAgroManagementReader
from pcse.util import WOFOST71SiteDataProvider
from pcse.fileinput import CABOWeatherDataProvider
from pcse.models import Wofost71_WLP_FD
import fire
import pandas as pd
import typer
from pcse.base_classes import WeatherDataContainer

WeatherDataContainer.ranges = {"LAT": (-90., 90.),
                               "LON": (-180., 180.),
                               "ELEV": (-300, 6000),
                               "IRRAD": (0., 40e30),
                               "TMIN": (-50., 60.),
                               "TMAX": (-50., 60.),
                               "VAP": (0.06, 2000000.3),
                               "RAIN": (0, 25),
                               "E0": (0., 20000000.5),
                               "ES0": (0., 2000000.5),
                               "ET0": (0., 2000000.5),
                               "WIND": (0., 100.),
                               "SNOWDEPTH": (0., 250.),
                               "TEMP": (-50., 60.),
                               "TMINRA": (-50., 60.)}
base_dir = "./DATA"
out_dir = "./OUT"
app = typer.Typer()

""" sample wofost runner based on pcse """

"""
crop: crop file name in DATA directory
soil: soil file name in DATA directory
argo: argo file name in DATA directory
waether_filename and weathet_cabowe:  weather file name and path
day: number of day for running model
saved_name: name of csv output that will save in OUT directory
"""


@app.command(name="run")
def run(crop: str, soil: str, agro: str, day: int, weather_filename: str,
        saved_name="output"):
    # load argo from directory
    agromanagement = YAMLAgroManagementReader(f"{base_dir}/{agro}")
    sitedata = WOFOST71SiteDataProvider(WAV=100, CO2=360)
    # load soil from directory
    soildata = CABOFileReader(f"{base_dir}/{soil}")
    # load crop from directory
    cropdata = CABOFileReader(f"{base_dir}/{crop}")
    # load weather data from directory
    wdp = CABOWeatherDataProvider(fname=weather_filename, fpath=base_dir)
    # packaing parameters
    parameters = ParameterProvider(cropdata=cropdata, soildata=soildata,
                                   sitedata=sitedata)
    # create model
    wofost = Wofost71_WLP_FD(parameters, wdp, agromanagement)
    # run till [day]
    wofost.run(day)

    # save output az a csv in OUT directory
    model_out_put = wofost.get_output()
    df = pd.DataFrame(model_out_put)
    df.to_csv(f"{out_dir}/{saved_name}.csv")


if __name__ == '__main__':
    app()
