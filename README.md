# starplot-hyperleda

<img src="hyperleda.jpg" />

HyperLeda catalog builder for [Starplot](https://github.com/steveberardi/starplot), which contains 983,261 galaxies (plotted above as pink markers).

1. `make install` to create virtual environment
2. `make build` to build catalog Parquet file
3. `make release` to create release (only run from GitHub action)

## Use this Catalog with Starplot

```python
hyperleda = Catalog(
    path="hyperleda.0.1.0.parquet",  # or specify your custom data path
    url="https://github.com/steveberardi/starplot-hyperleda/releases/download/v0.1.0/hyperleda.0.1.0.parquet",
)

m31 = DSO.get(m="31", catalog=hyperleda)

```

---

## Acknowledgements

Data for this catalog was obtained from:

- [HyperLeda - Catalog of galaxies : VII/237](https://cdsarc.cds.unistra.fr/viz-bin/cat/VII/237) (positions, geometry)
- [Automatic extraction for millions of galaxies](https://aas.aanda.org/articles/aas/abs/2000/16/ds1851/ds1851.html). G. Paturel, Y. Fang, R. Garnier, C. Petit and J. Rousseau; 2000, Astron. Astrophys. Suppl. Ser., 146, 19 (magnitudes in B band, via [HyperLeda database](http://leda.univ-lyon1.fr)) 

