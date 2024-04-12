# Zadanie 8

Úlohou bolo implementovať paralelnú verziu triediaceho algoritmu samplesort s využitím architektúry CUDA v pythone implementovanej knižnicou `Numba`.

Samotný algoritmus samplesort vykonáva triedenie v nasledujúcich krokoch:
1. Rozdelenie poľa `data` na `N_BUCKETS` častí a zoradenie týchto častí paralelne vo funkcií `sort_evenly()`
2. Z každej časti vybrať `N_BUCKET - 1` počet hodnôt do poľa `samples`
3. Zoradiť pole `samples`
4. Z poľa `samples` vybrať `N_BUCKET - 1` počet hodnôt do poľa `splitters` predstavujúcich hraničné hodnoty bucketov
5. Roztriediť hodnoty z poľa `data` do bucketov `buckets` podľa `splitters`
6. Zoradiť buckety paralelne vo funkcií `sort_splitters()` pomocou insertion sortu a vrátiť zoradené pole `data`

<a href="http://users.atw.hu/parallelcomp/ch09lev1sec5.html">Zdroj</a>


## Porovnanie sérioveho a paralelného algoritmu

Nakoniec som urobil porovnanie paralelného samplesortu v súbore `08.py` a sériového insertion sortu v súbore `08_ser.py` s rôznou dľžkou poľa `ARRAY_LENGTH` s hodnotami vždy v rozsahu 0-99. Pre meranie času som použil funkciu `cuda.event_elapsed_time()` a rozdiel časov udalostí `cuda.event()` vždy na začiatku a konci vykonávania algoritmu. Výsledky porovnania sú nasledovné:

tabuľka
1000000           19349.61 (100)
100000            8428.28 (10) 1300.15 (50) 1571.02 (100)
10000    3771.05  445.08(10) 463.96 (50)   477.19(100)
5000     934.64   366.62(10)   357.85 (50)   393.75 (100)
1000     34.83    337.24 (10)   315.61 (50)   401.70 (100)
100      0.37     310.62 (10)
C U D A