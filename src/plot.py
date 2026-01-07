from starplot import MapPlot, Robinson, Mollweide, _, DSO
from starplot.styles import PlotStyle, extensions
from starplot.data import Catalog

from settings import BUILD_FILE_PATH

hyperleda = Catalog(path=BUILD_FILE_PATH)

import timeit

n = 1
def get():
    results = DSO.find(where=[_.magnitude < 18], catalog=hyperleda)
    # results = DSO.find(where=[_.m ==31], catalog=hyperleda)
    # print(len(results))
    """
    Row group size = 100 -> 2.36 sec / 66ms to find andromeda by M
    """

    # andromeda = DSO.get(ngc="224", catalog=hyperleda)


execution_time = timeit.timeit(stmt=get, number=n)
print(execution_time/n)
exit()

p = MapPlot(
    projection=Mollweide(),
    style=PlotStyle().extend(
        extensions.BLUE_NIGHT,
        extensions.MAP,
    ),
    resolution=6000,
    scale=0.3,
)

p.dsos(
    catalog=hyperleda,
    where=[_.magnitude < 18],
    where_labels=[False],
    true_size=False,
)

p.milky_way()

p.export("hyperleda.png", padding=1, transparent=True)
