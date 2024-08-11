# Zadanie 2

V zadaní 2 bolo potreba implementovať problém divochov, ktorí spolu každý deň obedujú, pričom majú kuchára, ktorý im vždy na požiadanie navarí a doplní jedlo do hrnca.

V prvom rade je potrebné zabezpečiť synchronizáciu medzi divochmi tak, aby sa najedli všetci spolu v jeden moment. Predtým je potrebné zabezpečiť, aby mal každý svoju porciu, ktoré si postupne naberajú z hrnca. Ak dôjde k vyprázdneniu hrnca, divoch ktorý si aktuálne naberá, zavolá kuchárovi, ktorý následne zabezpečí pridanie ďalších porcií do hrnca. Keď majú všetci divosi svoje jedlo, môžu začať obedovať. Po najedení sa znova rozídu a pokračujú vo svojich každodenných činnostiach až pokým sa na druhý deň zase nestretnú a cyklus sa opakuje.

V mojej implementácií je počet divochov daný premennou `N_DINER`, pričom každého divocha predstavuje samostatné vlákno vykonávajúce funkciu `diner()`. Rolu kuchára predstavuje ďalšie vlákno vykonávajúce funkciu `chef()`, pričom spolu s divochmi majú zdieľaný objekt `shared` triedy `Shared`. Kapacita hrnca vyjadrená maximálnym počtom porcií je definovaná premennou `POT_CAPACITY`.

V zdieľanom objekte sa nachádza okrem počítadla porcii v hrnci aj Mutex zámok hrnca `shared.pot` zabezpečujúci integritu jeho počítadla. Taktiež tam nájdeme dve jednoduché bariéry zabezpečujúce synchronizáciu divochov, a dva semafory, ktoré slúžia na signalizáciu. V prípade vyprázdnenia hrnca hladný divoch prvým semaforom `shared.chef` signalizuje kuchárovi, že treba navariť a keď kuchár navarí a doplní jedlo dá vedieť naspäť divochovi druhým semaforom `shared.chef_done`.

Jednoduchá bariéra je implementovaná jednoducho v triede `SimpleBarrier` s argumentom predstavujúcim počet vlákien ktoré majú byť synchronizované. Samotná bariéra pozostáva z počítadla a Mutex zámku, chrániaceho jeho integritu, a turniketu implementovaného pomocou semaforu. Každé vlákno po zavolaní metódy `wait()` inkrementuje počítadlo až pokým počítadlo nedosiahne daný počet vlákien, nastavený parametrom `max_threads` pri inicializácií bariéry. Následne sa otvorí turniket pre všetky vlákna a počítadlo sa vynuluje. Bariéra je tiež rozšírená o metódu `set_unlock_text()` ktorá ponúka možnosť nastavenia vypísania želaného výstupu pri otvorení bariéry.

Divosi vykonávajú kód funkcie `diner()`, kde najprv narazia na prvú bariéru, ktorá ich pustí ďalej len v prípade že všetci dorazia.

    shared.barrier.wait()

Následne si po jednom idú naberať porcie to je zabezpečené nasledovnou časťou kódu:

    shared.pot.lock()
    if shared.portions <= 0:
        shared.chef.signal()
        shared.chef_done.wait()
    shared.portions -= 1
    shared.pot.unlock()

Prístup k hrncu je zabezpečený zámkom `shared.pot` vďaka ktorému pristupuje k hrncu vždy len jeden divoch. V prípade vyprázdnenia hrnca to aktuálny divoch signalizuje kuchárovi pomocou semafora `shared.chef` a počká kým bude hrniec znova naplnený na semafore `shared.chef_done`.

Po tom čo si divosi naberú svoju porciu, počkajú na seba pri druhej bariére. Ak budú už všetci pripravený, môžu sa s chuťou pustiť do jedenia.

    shared.barrier2.wait()

Vlákno kuchára vykonávajúce funkciu `chef()` čaká na pokyn divocha semaforom `shared.chef`. Po signalizácií, teda inkrementovaní semafora na hodnotu 1, kuchár naspäť dekrementuje tento semafor a začne pripravovať jedlo. Všimnime si, že k počítadlu hrnca ktoré je pod zámkom divocha ktorý kuchára zavolal a musí na neho počkať, nemajú v tomto momente prístup žiadne iné vlákna. Kuchár tak môže veselo doplniť porcie do hrnca a s radosťou signalizovať divochovi jeho naplnenie semaforom `shared.chef_done`.

    shared.chef.wait()
    print("Chef is preparing food.")
    sleep(5)
    shared.portions += POT_CAPACITY
    shared.chef_done.signal()

Taktiež som do kódu pridal výpisy pomocou ktorých si vieme skontrolovať správnu postupnosť vykonávaných udalostí.

    Diner 3 came to lunch.
    Diner 5 came to lunch.
    Diner 4 came to lunch.
    Diner 0 came to lunch.
    Diner 1 came to lunch.
    Diner 2 came to lunch.
    Diner 6 came to lunch.
    All diners came to lunch.
    Diner 4 picked his portion.
    Diner 2 picked his portion.
    Diner 3 picked his portion.
    Diner 1 picked his portion.
    Diner 0 picked his portion.
    Diner 5 picked his portion.
    Diner 6 picked his portion.
    All diners have their portion. They proceed to eat.
    Diner 2 finished lunch.
    Diner 5 finished lunch.
    Diner 0 finished lunch.
    Diner 1 finished lunch.
    Diner 6 finished lunch.
    Diner 3 finished lunch.
    Diner 4 finished lunch.

Výpis jedného cyklu v prípade, že kuchár dopĺňa porcie:

    Diner 4 came to lunch.
    Diner 3 came to lunch.
    Diner 6 came to lunch.
    Diner 1 came to lunch.
    Diner 2 came to lunch.
    Diner 0 came to lunch.
    Diner 5 came to lunch.
    All diners came to lunch.
    Diner 3 picked his portion.
    Diner 6 picked his portion.
    Diner 1 picked his portion.
    Diner 0 realised the pot is empty. Calling chef.
    Chef is preparing food.
    Chef refilled the pot.
    Diner 0 picked his portion.
    Diner 4 picked his portion.
    Diner 2 picked his portion.
    Diner 5 picked his portion.
    All diners have their portion. They proceed to eat.
    Diner 6 finished lunch.
    Diner 5 finished lunch.
    Diner 2 finished lunch.
    Diner 1 finished lunch.
    Diner 0 finished lunch.
    Diner 3 finished lunch.
    Diner 4 finished lunch.
