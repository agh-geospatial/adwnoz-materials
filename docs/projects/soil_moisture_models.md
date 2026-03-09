# Porównanie przestrzennych modeli wilgotności gleby

**Opis problemu badawczego:** Wilgotność gleby jest kluczową zmienną hydrologiczną wpływającą na plony rolnicze, bilans wodny, ryzyko pożarów i zmiany klimatyczne. Dostępnych jest wiele produktów przestrzennych wilgotności gleby, różniących się rozdzielczością, metodologią i pokryciem czasowym - od modeli reanaliz klimatycznych, przez produkty satelitarne, po modele hydrodynamiczne. Celem projektu jest porównanie wybranych produktów wilgotności gleby pod kątem zgodności przestrzennej, czasowej i statystycznej, najlepiej z uwzględnieniem walidacji na danych naziemnych.

**Proponowane źródła danych:**

- [ERA5-Land (Copernicus Climate Data Store)](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land) - reananaliza, rozdzielczość ~9 km, dane od 1950 r.
- [SMAP L4 Surface and Rootzone Soil Moisture (NASA)](https://nsidc.org/data/spl4smgp) - najwyższa dokładność w klasie produktów globalnych, od 2015 r., ~9 km
- [SMAP/Sentinel-1 (NASA)](https://nsidc.org/data/spl2smap_s) - produkt fuzji aktywno-pasywnej, rozdzielczość 1-3 km
- [ESA CCI Soil Moisture](https://esa-soilmoisture-cci.org/) - wieloletnia fuzja produktów satelitarnych, od 1978 r., ~25 km
- [ISMN (International Soil Moisture Network)](https://ismn.earth/) - baza naziemnych pomiarów wilgotności do walidacji

**Dodatkowe informacje:**

- API do pobierania ERA5-Land: [Copernicus CDS API](https://cds.climate.copernicus.eu/how-to-api)
- Do wczytywania danych SMAP (HDF5) przydatny jest pakiet `h5py` lub `xarray` z silnikiem `h5netcdf`
- Biblioteki: `xarray`, `rioxarray`, `pandas`, `scipy`, `matplotlib`, `cartopy`

**Proponowane techniki analizy danych:**

- Pobranie i harmonizacja danych (reprojekcja na wspólną siatkę, ujednolicenie jednostek i rozdzielczości czasowej)
- Eksploracyjna analiza danych - rozkłady wartości, sezonowość, mapy przestrzenne
- Porównanie statystyczne produktów: korelacja Pearsona, RMSE, bias względem danych naziemnych (ISMN) lub wzajemnie
- Analiza przestrzenna różnic - mapy odchyleń między modelami, identyfikacja regionów o największych rozbieżnościach
- Analiza sezonowości i trendów długoterminowych (np. dla ERA5-Land)
- Walidacja na wybranym obszarze (np. Polska lub obszar śródziemnomorski) względem danych ISMN
- Fuzja produktów metodą ważonej kombinacji (ensemble) i ocena uzyskanej zgodności
