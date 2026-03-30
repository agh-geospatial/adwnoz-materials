"""
ERA5 - pobieranie danych godzinowych dla wybranych lokalizacji punktowych
========================================================================

NAJSZYBSZA METODA: dataset `reanalysis-era5-single-levels-timeseries`
- przechowywany w formacie zoptymalizowanym pod time-series (nie gridowym!)
- automatycznie wybiera najbliższy punkt siatki (0.25° x 0.25°)
- dla wielu lokalizacji: równoległe requesty (ThreadPoolExecutor)

Wymagania:
    conda install earthkit-data -c conda-forge
    conda install cdsapi -c conda-forge

Konfiguracja CDS API (~/.cdsapirc lub %USERPROFILE%\.cdsapirc):
    url: https://cds.climate.copernicus.eu/api
    key: <twój_personal_access_token>
    (token dostępny po rejestracji na: https://cds.climate.copernicus.eu)
"""

import earthkit.data
import xarray as xr
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# KONFIGURACJA
# ---------------------------------------------------------------------------

LOCATIONS = {
    "krakow":   {"latitude": 50.06, "longitude": 19.94},
    "warszawa": {"latitude": 52.23, "longitude": 21.01},
    "gdansk":   {"latitude": 54.35, "longitude": 18.65},
}

VARIABLES = [
    "2m_temperature",
    "total_precipitation",
    "10m_u_component_of_wind",
    "10m_v_component_of_wind",
]

# ERA5 zaczyna się w 1940-01-01 i kończy ~5 dni przed dzisiejszą datą
# (tyle czasu potrzeba na przetworzenie najnowszych danych przez ECMWF)
ERA5_START = "1940-01-01"
ERA5_END   = (date.today() - timedelta(days=5)).strftime("%Y-%m-%d")
DATE_RANGE = [ERA5_START, ERA5_END]

OUTPUT_DIR = Path("era5_output")
OUTPUT_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# FUNKCJA POBIERANIA - jedna lokalizacja
# ---------------------------------------------------------------------------

def download_location(name: str, coords: dict) -> xr.Dataset:
    """
    Pobiera cały zakres czasowy ERA5 dla jednego punktu.
    Dataset timeseries jest zoptymalizowany do tego celu - znacznie szybszy
    niż standardowy 'reanalysis-era5-single-levels' z parametrem area.
    """
    print(f"[{name}] Rozpoczynam pobieranie ({coords['latitude']}°N, {coords['longitude']}°E)...")

    request = {
        "variable": VARIABLES,
        "date": DATE_RANGE,
        "location": coords,        # automatycznie trafia na najbliższy punkt siatki
        "data_format": "netcdf",
    }

    ds = (
        earthkit.data
        .from_source("cds", "reanalysis-era5-single-levels-timeseries", request)
        .to_xarray()
    )

    out_path = OUTPUT_DIR / f"era5_{name}.nc"
    ds.to_netcdf(out_path)
    print(f"[{name}] Zapisano -> {out_path}  ({len(ds.valid_time)} kroków czasowych)")

    return ds


# ---------------------------------------------------------------------------
# POBIERANIE RÓWNOLEGŁE - wszystkie lokalizacje jednocześnie
# ---------------------------------------------------------------------------

def download_all_parallel(max_workers: int = 4) -> dict[str, xr.Dataset]:
    """
    Wysyła równoległe requesty do CDS dla każdej lokalizacji.
    CDS pozwala na kilka jednoczesnych zadań - max_workers=4 jest bezpieczne.
    """
    results = {}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(download_location, name, coords): name
            for name, coords in LOCATIONS.items()
        }

        for future in as_completed(futures):
            name = futures[future]
            try:
                results[name] = future.result()
            except Exception as e:
                print(f"[{name}] BŁĄD: {e}")

    return results


# ---------------------------------------------------------------------------
# PRZYKŁAD - analiza po pobraniu
# ---------------------------------------------------------------------------

def quick_stats(datasets: dict[str, xr.Dataset]) -> pd.DataFrame:
    """Prosta statystyka temperatury dla wszystkich lokalizacji."""
    rows = []
    for name, ds in datasets.items():
        if "t2m" in ds:
            t_celsius = ds["t2m"] - 273.15
            rows.append({
                "lokalizacja": name,
                "lat_nearest": float(ds["latitude"].values),
                "lon_nearest": float(ds["longitude"].values),
                "T_mean_C":    round(float(t_celsius.mean()), 2),
                "T_min_C":     round(float(t_celsius.min()), 2),
                "T_max_C":     round(float(t_celsius.max()), 2),
                "n_hours":     len(ds["valid_time"]),
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("ERA5 point download - metoda: reanalysis-era5-single-levels-timeseries")
    print(f"Lokalizacje: {list(LOCATIONS.keys())}")
    print(f"Zmienne:     {VARIABLES}")
    print(f"Zakres:      {DATE_RANGE[0]}  ->  {DATE_RANGE[1]}")
    print("-" * 60)

    datasets = download_all_parallel(max_workers=len(LOCATIONS))

    if datasets:
        stats = quick_stats(datasets)
        print("\nStatystyki temperatury:")
        print(stats.to_string(index=False))

    for ds in datasets.values():
        ds.close()
