# Cyfrowa wersja map glebowych

**Opis problemu badawczego:** Tradycyjne mapy glebowe, tworzone w oparciu o terenowe badania profili glebowych i ręczną kartografię, stanowią cenne, ale często przestarzałe lub trudno dostępne zasoby wiedzy o glebach. Nowoczesne globalne produkty cyfrowego kartowania gleb (np. SoilGrids) generują informacje o właściwościach gleb w sposób automatyczny, na podstawie uczenia maszynowego i teledetekcji. Celem projektu jest porównanie i analiza przestrzenna wybranych właściwości gleb z różnych źródeł - tradycyjnych i cyfrowych - z ewentualnym uwzględnieniem walidacji statystycznej i oceny dokładności przestrzennej.

**Proponowane źródła danych:**

- [SoilGrids 2.0 (ISRIC)](https://soilgrids.org/) - globalny produkt ML, rozdzielczość 250 m, dostęp przez WCS lub REST API; właściwości: pH, zawartość materii organicznej, frakcje granulometryczne (piasek, pył, ił), gęstość objętościowa, CEC
- [European Soil Data Centre (ESDAC)](https://esdac.jrc.ec.europa.eu/) - mapy glebowe dla obszaru Europy (ESDAC Topsoil Survey, LUCAS Soil)
- [LUCAS Topsoil (Eurostat/JRC)](https://esdac.jrc.ec.europa.eu/content/lucas-2018-topsoil-survey) - dane punktowe z terenowych badań gleb UE, dostępne jako CSV
- [Baza danych glebowo-kartograficzna Polski](https://www.gios.gov.pl/) lub dane z Generalnej Dyrekcji Ochrony Środowiska - krajowe dane glebowe (o ile dostępne)

**Dodatkowe informacje:**

- SoilGrids udostępnia dane przez Web Coverage Service (WCS); przykładowe skrypty Python z użyciem `OWSLib` dostępne są w [dokumentacji SoilGrids](https://docs.isric.org/globaldata/soilgrids/wcs.html)
- Dane LUCAS Soil to punktowe obserwacje - wymagają geokodowania i analizy przestrzennej
- Biblioteki: `owslib`, `rioxarray`, `geopandas`, `scipy`, `sklearn` (do interpolacji i walidacji)

**Proponowane techniki analizy danych:**

- Pobranie danych z SoilGrids dla wybranego obszaru (np. Polska lub wybrany region) i wybranej właściwości gleby
- Eksploracyjna analiza danych - rozkłady przestrzenne, histogramy, korelacje między warstwami
- Porównanie SoilGrids z danymi punktowymi LUCAS: obliczenie błędu RMSE, MAE, korelacji
- Przestrzenna analiza różnic - identyfikacja obszarów, gdzie model odbiega od pomiarów terenowych
- ?Interpolacja przestrzenna właściwości gleby z danych punktowych LUCAS (np. kriging, IDW) i porównanie z SoilGrids?
- ?Analiza niepewności prognoz SoilGrids (dostępne kwantyle 5. i 95.) w powiązaniu z typem pokrycia terenu lub nachyleniem?
- Wizualizacja map przestrzennych właściwości gleb i ich zmienności
