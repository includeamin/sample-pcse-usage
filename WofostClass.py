from pcse.base_classes import ParameterProvider
from pcse.fileinput import CABOFileReader
from pcse.fileinput import YAMLAgroManagementReader
from pcse.util import WOFOST71SiteDataProvider
from pcse.db import NASAPowerWeatherDataProvider
from pcse.fileinput import CABOWeatherDataProvider
from pcse.models import Wofost71_WLP_FD
import fire
import pandas as pd

base_dir = "./DATA"
out_dir = "./OUT"


class Wofost:
    """ sample wofost runner based on pcse """

    """
    crop: crop file name in DATA directory
    soil: soil file name in DATA directory
    argo: argo file name in DATA directory
    waether_filename and weathet_cabowe:  weather file name and path
    day: number of day for running model
    saved_name: name of csv output that will save in OUT directory
    """

    def run(self, crop, soil, agro, weather_filename, weather_cabowe, day, saved_name="output"):
        # load argo from directory
        agromanagement = YAMLAgroManagementReader(f"{base_dir}/{agro}")
        sitedata = WOFOST71SiteDataProvider(WAV=100, CO2=360)
        # load soil from directory
        soildata = CABOFileReader(f"{base_dir}/{soil}")
        # load crop from directory
        cropdata = CABOFileReader(f"{base_dir}/{crop}")
        # load weather data from directory
        wdp = CABOWeatherDataProvider(fname=weather_filename, fpath=weather_cabowe)
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
        df.to_csv(f"{out_dir}/{saved_name}")


if __name__ == '__main__':
    fire.Fire(Wofost)
