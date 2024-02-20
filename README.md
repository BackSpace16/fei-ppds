# Zadanie 1

Program vytvorí 2 vlákna s menami Jano a Fero, ktoré vykonávajú úlohy definované vo funkcií `tasks()`. Úlohou bolo zabezpečiť serializáciu vykonávania úlohy jedenia implementovanej funkciou `eating()`, tak aby druhé vlákno vykonalo túto úlohu až keď ju dokončí prvé vlákno.

To aby prvé vlákno vykonalo úlohu vždy pred druhým vláknom je zabezpečené pomocou semafóra `call` inicializovaného na hodnotu `0` v zdielanom objekte `shared` triedy `Shared`.

Prvé vlákno po dokončení úlohy inkrementuje tento semafór `shared.call` zavolaním funkcie `call()` čím sa hodnota semafóra zväčší na hodnotu `1`.

Ďalšie vlákno musí pred vykonaním úlohy počkať na prvé vlákno, to je zabezpečené príkazom `wait()` semafóra `shared.call` vo funkcií `recieve_call()`.

V prípade, že prvé vlákno dokončí úlohu skôr ako sa k nej dostane druhé vlákno, inkrementuje semafór na hodnotu `1` čo dovolí vykonávanie funkcie druhým vláknom.

V prípade, že je druhé vlákno rýchlejšie ako prvé, semafór inicializovaný na hodnotu `0` preruší jeho ďalšie vykonávanie až pokým prvé vlákno nezväčší hodnotu semafóra na `1`.

Výpis v prípade, že druhý proces musí počkať na dokončenie úlohy prvého procesu:

    Jano fell asleep. He will be sleeping 5s.
    Fero fell asleep. He will be sleeping 5s.
    Jano woke up.
    Fero woke up.
    Fero started doing his morning hygiene. He will be done in 1s.
    Jano started doing his morning hygiene. He will be done in 1s.
    Fero finished his morning hygiene.
    Fero waiting for a call.
    Jano finished his morning hygiene.
    Jano started eating. He will be done in 2s.
    Jano finished eating.
    Jano is calling.
    Fero recieved call.
    Fero started eating. He will be done in 2s.
    Fero finished eating.

Výpis v prípade, že prvý proces dosiahne bod serializácie skôr ako druhý proces:

    Jano fell asleep. He will be sleeping 3s.
    Fero fell asleep. He will be sleeping 6s.
    Jano woke up.
    Jano started doing his morning hygiene. He will be done in 1s.
    Jano finished his morning hygiene.
    Jano started eating. He will be done in 2s.
    Fero woke up.
    Fero started doing his morning hygiene. He will be done in 1s.
    Jano finished eating.
    Jano is calling.
    Fero finished his morning hygiene.
    Fero waiting for a call.
    Fero recieved call.
    Fero started eating. He will be done in 1s.
    Fero finished eating.