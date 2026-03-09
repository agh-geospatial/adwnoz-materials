# Zunifikowany dostęp do nachylenia terenu

**Opis problemu badawczego:** Nachylenie terenu (slope) jest jedną z podstawowych pochodnych cyfrowych modeli wysokości (DEM), niezbędną w analizach hydrologicznych, geomorfologicznych, rolniczych i środowiskowych. Dostępnych jest wiele globalnych źródeł danych wysokościowych (Copernicus DEM, SRTM, ALOS World 3D), które różnią się rozdzielczością przestrzenną, metodologią pomiaru i pokryciem. Wyznaczone na ich podstawie wartości nachylenia mogą istotnie się różnić. Celem projektu jest stworzenie zunifikowanego narzędzia lub pipeline'u umożliwiającego pobieranie danych DEM z różnych źródeł, obliczanie nachylenia terenu i systematyczne porównanie uzyskanych wyników na wybranym obszarze testowym.

**Proponowane źródła danych:**

- [Copernicus DEM GLO-30 / GLO-90](https://registry.opendata.aws/copernicus-dem/) - 30 m i 90 m, globalne, AWS S3 (STAC)
- [SRTM 30m / 90m](https://github.com/bopen/elevation) - klasyczny produkt NASA/USGS, dostępny przez pakiet `elevation`
- [ALOS World 3D-30m (AW3D30)](https://www.eorc.jaxa.jp/ALOS/en/dataset/aw3d30/aw3d30_e.htm) - produkt JAXA, rozdzielczość 30 m
- [EU-DEM v1.1](https://www.eea.europa.eu/data-and-maps/data/copernicus-land-monitoring-service-eu-dem) - DEM dla obszaru Europy, 25 m

**Dodatkowe informacje:**

- Biblioteki do obliczania nachylenia i pochodnych DEM: [`richdem`](https://richdem.readthedocs.io/) (Horn 1981), [`xarray-spatial`](https://xarray-spatial.readthedocs.io/) (integracja z xarray, Numba)
- Dostęp do danych STAC (Copernicus DEM): `pystac-client`, `stackstac` lub `odc-stac`
- Pakiet `elevation` pozwala na proste pobranie SRTM 30m/90m dla dowolnego bounding box
- Warto wybrać obszar testowy zróżnicowany rzeźbą terenu (np. Tatry, Karpaty, obszar nizinny) dla lepszej ekspozycji różnic

**Proponowane techniki analizy danych:**

- Pobranie danych DEM z co najmniej dwóch źródeł dla wspólnego obszaru zainteresowań (AOI)
- Reprojekcja i resampling do wspólnej siatki przestrzennej umożliwiającej bezpośrednie porównanie
- Obliczenie nachylenia terenu dla każdego DEM tą samą metodą (np. Horn 1981 przez `richdem`)
- Statystyczna analiza porównawcza - histogramy, korelacja, RMSE, rozkład różnic
- Przestrzenna analiza różnic - mapy odchyleń między produktami, identyfikacja obszarów o największych rozbieżnościach
- Interpretacja różnic w kontekście charakterystyki źródłowych danych (metoda akwizycji, rok pomiaru, rozdzielczość)
- Badanie wpływu wyboru DEM na wyniki praktycznej analizy (np. wyznaczanie zlewni, analizę ekspozycji zboczy)
