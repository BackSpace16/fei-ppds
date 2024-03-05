# Zadanie 3

Toto zadanie predstavuje problém synchronizácie vlákien predstavujúcich pasažierov s vláknom predstavujúci vláčik húsenkovej dráhy. 

Vláčik má obmedzenú kapacitu `CAPACITY` a môže vykonať jazdu iba ak je naplnený, teda ak nastúpi počet pasažierov rovný konštante `CAPACITY`. 

Pasažieri môžu nastupovať iba ak je vláčik pripravený, teda po zavolaní funkcie `load()`, podobne môže vystúpiť až po zastavení a zavolaní funkcie `unload()`. Taktiež je potrebné zabezpečiť aby vláčik počkal na nastúpenie a vystúpenie všetkých pasažierov. Celkový počet pasažierov je definovaný konštantou `N_PASSENGERS`.

Moja implementácia obsahuje jedno vlákno vláčika vykonavajúce funkciu `train()` a vlákna pasažierov vykonávajúce funkciu `passenger()`, pričom zdielajú spoločný objekt `shared` triedy `Shared`, kde zdielajú objekty pre synchronizáciu nástupu a výstupu.

Vlákno vláčika najprv vykoná funkciu `load()` a signalizuje pasažierom počtu `CAPACITY` pomocou semafora `shared.board_queue`. Následne počká na semafor `shared.boarded` a vyrazí na dráhu vykonávajúc funkciu `run()`. Po úspešnom dokončení jazdy zavolá funkciu `unload()`, signalizuje pasažierom pomocou semafora `shared.unboard_queue` a počká pokým všetci nevystúpia na semafore `shared.unboarded`.


Vlákno vláčika:
```python
load()
shared.board_queue.signal(CAPACITY)
shared.boarded.wait()
run()
unload()
shared.unboard_queue.signal(CAPACITY)
shared.unboarded.wait()
```

Pasažieri čakajú na semafore `shared.board_queue` pokým im vláčik signalizuje, že môžu nastúpiť. Následne vykonajú funkciu `board()` a počkajú až budú všetci nastúpený pri bariére `shared.board_barrier`. Po otvorení bariéry sa vláčiku signalizuje pomocou semafóra `shared.boarded`. Vystupovanie prebieha analogicky.

Bariéra je implementovaná podobne ako v [zadaní 2](https://github.com/BackSpace16/Vizvary-111488-PPDS2024/tree/02) avšak s pridanou možnosťou signalizácie semafora po otvorení bariéry. Semafor ktorý chceme signalizovať po otvorení bariéry vieme poslať ako argument do metódy `barrier.wait(semaphore)`.

Vlákno pasažiera:
```python
shared.board_queue.wait()
board()
shared.board_barrier.wait(shared.boarded)

shared.unboard_queue.wait()
unboard()
shared.unboard_barrier.wait(shared.unboarded)
```

Pri takejto implementácií problému môže dôjsť k vyhladovaniu niektorých vlákien, ktoré sa jednoducho nedostanú do vláčika, keďže ich vždy predbehne iné vlákno. Riešením by bolo implementovanie FIFO fronty v semafore `shared.board_queue`, ktorá by zabezpečila poradie pre čakajúce vlákna, čo by znemožnilo vláknam predbiehať sa.

Výpisy z konzoly:

    Train is empty, ready for boarding.
    Passenger 16 boarded.
    Passenger 14 boarded.
    Passenger 4 boarded.
    Passenger 12 boarded.
    Passenger 8 boarded.
    Passenger 3 boarded.
    Passenger 7 boarded.
    Passenger 13 boarded.
    Train is full, departing.
    Train arrived.
    Train is ready for unloading.
    Passenger 16 unboarded.
    Passenger 4 unboarded.
    Passenger 3 unboarded.
    Passenger 8 unboarded.
    Passenger 7 unboarded.
    Passenger 13 unboarded.
    Passenger 14 unboarded.
    Passenger 12 unboarded.
    Train is empty, ready for boarding.