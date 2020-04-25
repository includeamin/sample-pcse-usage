from pcse.base_classes import ParameterProvider
from pcse.fileinput import CABOFileReader
from pcse.fileinput import YAMLAgroManagementReader
from pcse.util import WOFOST71SiteDataProvider
from pcse.db import NASAPowerWeatherDataProvider
from pcse.models import Wofost71_WLP_FD
import fire
import pandas as pd

base_dir = "./DATA"
out_dir = "./OUT"


class Wofost:
    """ sample wofost runner based on pcse """

    def run(self, crop, soil, agro, day, saved_name="output"):
        agromanagement = YAMLAgroManagementReader(f"{base_dir}/{agro}")
        sitedata = WOFOST71SiteDataProvider(WAV=100, CO2=360)
        soildata = CABOFileReader(f"{base_dir}/{soil}")
        cropdata = CABOFileReader(f"{base_dir}/{crop}")
        wdp = NASAPowerWeatherDataProvider(latitude=52, longitude=5)
        parameters = ParameterProvider(cropdata=cropdata, soildata=soildata,
                                       sitedata=sitedata)
        wofost = Wofost71_WLP_FD(parameters, wdp, agromanagement)
        if not day:
            wofost.run_till_terminate()
        else:
            wofost.run(day)

        model_out_put = wofost.get_output()
        df = pd.DataFrame(model_out_put)
        df.to_csv(f"{out_dir}/{saved_name}")

if __name__ == '__main__':
    fire.Fire(Wofost)
