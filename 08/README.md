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

| Dĺžka pola | Čas trvania sérioveho insertion sortu (ms) |                   | Čas trvania paralelného sample sortu (ms) * |                 |
|:----------:|:------------------------------------------:|:-----------------:|:-----------------------------------------:|:---------------:|
|        100 |                                       0.37 |      (10) 310.62 |                                           |                |
|      1 000 |                                      34.83 |      (10) 337.24 |                               (50) 315.61 |   (100) 401.70 |
|      5 000 |                                     934.64 |      (10) 366.62 |                               (50) 357.85 |   (100) 393.75 |
|     10 000 |                                   3 771.05 |      (10) 445.08 |                               (50) 463.96 |   (100) 477.19 |
|    100 000 |                                          - |     (10) 8_428.18 |                              (50) 1_300.15 |  (100) 1_571.02 |
|  1 000 000 |                                          - | (1000) 505_312.56 |                            (500) 46_266.34 | (100) 19_349.61 |

\* Počet bucketov v zátvorke

Z výsledkov môžeme pozorovať jednoznačnú výhodu paralelného algoritmu pri veľkých poliach. Môžme taktiež pozorovať zvýšený čas spracovania pri väčšom množstve bucketov, keďže časť algoritmu kde prebieha výber vzoriek a roztriedenie do bucketov je v mojej implementácií spracovaná sériovo.
