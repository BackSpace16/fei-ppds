# Zadanie 12

Úlohou tohto zadania bolo vytvoriť program umožňujúci asynchrónne sťahovanie viacerých súborov s vizuálnym zobrazením priebehu sťahovania.

V hlavnom koprograme `main()` sa pre každý sťahovaný súbor vytvorí koprogram `dwnld_file()`. Tieto koprogramy sú uložené v poli `tasks` a navzájom si odovzdávajú riadenie pomocou volania `await asyncio.gather(*tasks)`.

Koprogram `dwnld_file()` tvorí asynchrónne odoslanie HTTP GET požiadaviek na príslušnú URL adresu. Následne prebieha asynchrónne čítanie odpovede a zapisovanie do súboru po 1KiB častiach, počas ktorého prebieha aj aktualizovanie ukazovateľa priebehu sťahovania.

Pre prácu s HTTP požiadavkami som použil knižnicu `aiohttp`, pre vizuálne zobrazenie priebehu sťahovania knižnicu `tqdm`.

Príklad zobrazenia priebehu sťahovania viacerých súborov:
```
2024-04.Paralelne_vypocty_1.pdf:   9%|███▎                               | 161k/1.72M [00:02<00:22, 67.7kiB/s]
2024-02.mutex%20multiplex%20randezvouse%20bariera.pdf:  13%|█▊            | 136k/1.06M [00:01<00:06, 137kiB/s]
2024-08.cuda.pdf:   2%|▊                                                  | 136k/8.31M [00:01<00:57, 141kiB/s]
2024-05.1.Paralelne_vypocty_2.pdf:  27%|█████████▎                        | 103k/376k [00:02<00:05, 48.2kiB/s]
2024-03.zrychlenie_pk_rw_fajciari.pdf:  12%|███▌                           | 103k/895k [00:01<00:07, 106kiB/s]
2024-05.2.Paralelne_vypocty_2.pdf:   4%|█▍                              | 49.9k/1.14M [00:01<00:23, 46.3kiB/s]
2024-12.async2.pdf:  24%|███████████▋                                    | 82.7k/339k [00:00<00:02, 95.2kiB/s]
2024-11.async.pdf:  32%|████████████████▍                                  | 132k/410k [00:01<00:01, 161kiB/s]
2024-01.uvod_do_paralelnych_a_distribuovanych_vypoctov.pdf:  11%|▉       | 49.9k/449k [00:01<00:15, 25.1kiB/s]
2024-06.Paralelne_vypocty_3.pdf:   6%|█▉                                | 66.3k/1.18M [00:01<00:31, 35.5kiB/s] 
```