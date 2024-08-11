# Zadanie 11

Úlohou zadania 11 bolo naprogramovať plánovač pre koprogramy založené na generátoroch. Koprogramy sú funkcie vracajúce generátorový iterátor, objekt
ktorý vieme iterovať pomocou metódy `next()`, prípadne do neho vieme posielať premenné metódou `send()`. Iterovanie vždy vykoná kód koprogramu po nasledujúci príkaz `yield`, pričom sa zachováva stav premenných medzi iteráciami.

Moja implementácia plánovača v triede `Scheduler` spočíva v jednoduchej FIFO fronte do ktorej sa postupne ukladajú koprogramy pomocou metódy `add_job()`. Plánovač sa spúšťa zavolaním metódy `start()`. Táto metóda spustí cyklus v ktorom sa z fronty vždy vyberie generátorový iterátor `task`, zavolá sa metóda `next(task)` a začne sa vykonávať koprogram po nasledujúci príkaz `yield`. Po prerušení vykonávania koprogramu sa generátorový iterátor `task` vráti naspäť do fronty. V prípade, že koprogram ukončí vykonávanie svojej úlohy, nastane výnimka `StopIteration` v metóde `next()`, čo spôsobí, že sa koprogram už nevloží naspäť do fronty a pokračuje vykonávanie ostatných koprogramov až pokým nebude fronta prázdna. 

Pre ukážku som implementoval 3 rôzne generátorové funkcie koprogramov, ktoré vykonávajú jednoduché úlohy.
- `coprogram1(n)` - Počíta a vypisuje čísla od 0 po `n`,
- `coprogram2(a, b)` - Vypisuje mocniny dvojky od `a` po `b`,
- `coprogram3(t)` - Vypisuje ubehnutý čas od spustenia funkcie po uplynutie času `t` (v sekundách).

Pre ľahšie sledovanie výpisov v reálnom čase som do každého koprogramu pridal časové oneskorenie `sleep(0.5)`.

V hlavnej `main()` funkcii programu vytvoríme plánovač a priradíme mu koprogram 1, vypisujúci čísla od 0 po 5, koprogram 2, ktorý vypisuje mocniny dvojky od 0 po 13 a koprogram 3, vypisújuci uplynulý čas od jeho spustenia po dobu 30 sekúnd.

Z výpisu môžeme vidieť, že koprogramy sa striedajú a vykonávajú postupne tak ako sme očakávali:

    Coprogram 1: starting
    Coprogram 1: 0
    Coprogram 2: starting
    Coprogram 2: 1
    Coprogram 3: starting
    Coprogram 3: 0.5003s elapsed
    Coprogram 1: 1
    Coprogram 2: 2
    Coprogram 3: 2.0049s elapsed
    Coprogram 1: 2
    Coprogram 2: 4
    Coprogram 3: 3.5085s elapsed
    Coprogram 1: 3
    Coprogram 2: 8
    Coprogram 3: 5.0144s elapsed
    Coprogram 1: 4
    Coprogram 2: 16
    Coprogram 3: 6.5175s elapsed
    Coprogram 1: 5
    Coprogram 2: 32
    Coprogram 3: 8.0216s elapsed
    Task completed.
    Coprogram 2: 64
    Coprogram 3: 9.0243s elapsed
    Coprogram 2: 128
    Coprogram 3: 10.0280s elapsed
    Coprogram 2: 256
    Coprogram 3: 11.0300s elapsed
    Coprogram 2: 512
    Coprogram 3: 12.0326s elapsed
    Coprogram 2: 1024
    Coprogram 3: 13.0349s elapsed
    Coprogram 2: 2048
    Coprogram 3: 14.0374s elapsed
    Coprogram 2: 4096
    Coprogram 3: 15.0401s elapsed
    Task completed.
    Coprogram 3: 15.5422s elapsed
    Coprogram 3: 16.0432s elapsed
    Coprogram 3: 16.5443s elapsed
    Coprogram 3: 17.0456s elapsed
    Coprogram 3: 17.5471s elapsed
    Coprogram 3: 18.0482s elapsed
    Coprogram 3: 18.5493s elapsed
    Coprogram 3: 19.0513s elapsed
    Coprogram 3: 19.5526s elapsed
    Coprogram 3: 20.0550s elapsed
    Coprogram 3: 20.5561s elapsed
    Coprogram 3: 21.0577s elapsed
    Coprogram 3: 21.5606s elapsed
    Coprogram 3: 22.0619s elapsed
    Coprogram 3: 22.5629s elapsed
    Coprogram 3: 23.0646s elapsed
    Coprogram 3: 23.5662s elapsed
    Coprogram 3: 24.0672s elapsed
    Coprogram 3: 24.5682s elapsed
    Coprogram 3: 25.0701s elapsed
    Coprogram 3: 25.5711s elapsed
    Coprogram 3: 26.0717s elapsed
    Coprogram 3: 26.5720s elapsed
    Coprogram 3: 27.0727s elapsed
    Coprogram 3: 27.5736s elapsed
    Coprogram 3: 28.0752s elapsed
    Coprogram 3: 28.5768s elapsed
    Coprogram 3: 29.0778s elapsed
    Coprogram 3: 29.5789s elapsed
    Coprogram 3: 30.0805s elapsed
    Task completed.
