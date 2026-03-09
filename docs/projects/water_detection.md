# Detekcja powierzchni wody na zdjęciach satelitarnych

**Opis problemu badawczego:** Wyznaczanie zasięgu powierzchni wód (rzek, jezior, zbiorników, terenów podmokłych) na podstawie zdjęć satelitarnych jest kluczowe dla monitorowania zasobów wodnych, oceny ryzyka powodziowego i śledzenia zmian środowiskowych wywołanych zmianami klimatu. Celem projektu jest zbadanie i porównanie metod detekcji powierzchni wody - od klasycznych wskaźników spektralnych po techniki uczenia maszynowego - na podstawie wieloczasowych danych optycznych i/lub radarowych.

**Proponowane źródła danych:**

- Sentinel-2 (Copernicus Data Space Ecosystem / Microsoft Planetary Computer / Earth Search by Element 84)
- Sentinel-1 SAR (Copernicus Data Space Ecosystem)- do detekcji wody niezależnie od zachmurzenia
- [JRC Global Surface Water (Landsat)](https://global-surface-water.appspot.com/) - gotowy produkt referencyjny do walidacji
- [Dynamic World (Google / ESA)](https://dynamicworld.app/) - pixel-scale klasyfikacja terenu w czasie zbliżonym do rzeczywistego

**Dodatkowe informacje:**

- Spektralne wskaźniki wody: NDWI, MNDWI, AWEI - różnią się skutecznością w zależności od tła (obszary zurbanizowane, roślinność, cień)
- Do segmentacji semantycznej opartej na DL można skorzystać z datasetu [S1S2-Water](https://zenodo.org/records/11278238) (Sentinel-1 + Sentinel-2, binarne maski wody)
- Biblioteki: `rioxarray`, `stackstac`, `pystac-client`, `scikit-learn`, `segmentation-models-pytorch` (opcjonalnie)

**Proponowane techniki analizy danych:**

- Pobranie i wstępne przetwarzanie danych (korekcja atmosferyczna, maskowanie chmur)
- Obliczenie wskaźników spektralnych (NDWI, MNDWI, AWEI) i wyznaczenie optymalnego progu binaryzacji (np. Otsu)
 - Porównanie wskaźników - analiza wyników na różnych typach środowisk (tereny zurbanizowane, lasy, obszary wiejskie)
- Zastosowanie klasyfikatora ML (Random Forest, SVM) z cechami spektralnymi i przestrzennymi
- Segmentacja semantyczna z użyciem modelu U-Net na danych Sentinel-1/2
- Walidacja wyników względem JRC Global Surface Water lub Dynamic World
- Analiza zmienności zasięgu wody w czasie - wykrywanie zmian sezonowych lub ekstremalnych epizodów hydrologicznych (powodzie, susze)
