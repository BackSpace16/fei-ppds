# Zadanie 7

V siedmom zadaní bolo za úlohu upraviť program paralelného násobenia matíc pomocou MPI tak, aby sme umožnili vykonávať násobenie ľubovolnému počtu pracovných uzlov s použitím kolektívnej komunikácie.

Implementácia zadania sa nachádza v súbore `07_parsg.py` ktorý som upravil z pôvodného `cv.mat_parsg.py`. Po spustení programu proces s rankom definovaným konštantou `MASTER` inicializuje matice požadovaných veľkostí a rozdelí riadky matice `A` rovnomerne pre všetky procesy. V prípade, že počet riadkov nie je delitelný počtom procesov, zvyšné riadky oddelí od matice `A` do matice `A_tail` a tie po jednom rozdelí procesom.

Pre potrebu rozdelenia zvyšných riadkov som použil kolektívnej komunikácie `scatter` a `gather` pričom bolo nutné vytvoriť nový komunikátor `comm_tail` keďže počet procesov počítajúcich zvyšné riadky je menší ako počet všetkých procesov. Proces počítania prebieha rovnako ako v pôvodnej verzií s tým, že niektoré procesy počítajú ešte navyše tie zvyšné riadky po tom ako vypočítajú svoju časť matice `C`. Na konci proces s rankom `MASTER` skombinuje matice `C` a `C_tail` dohromady a vypíše výsledok.

V prípade väčšieho počtu procesov ako riadkov matice sa matica rozdelí každému procesu po jednom riadku pričom zvyšné procesy nevykonávajú žiadnu činnosť.

Ďalšiou časťou zadania bolo experimentovať s rôznymi hodnotami a porovnať jednotlivé metódy komunikácie. Do súborov `07_par.py`, predstavujúceho P2P komunikáciu pomocou metód `send` a `recv` a `07_parsg.py` s kolektívnou komunikáciou metódami `scatter` a `gather` som pridal meranie času vykonávania výpočtu v procese s rankom `MASTER`. Meranie pomocou metódy `MPI.Wtime()` začína po inicializácií a vytvorení matíc avšak ešte pred rozdelením a odoslaním zvyšným procesom. Meranie sa končí po skompletizovaní výslednej matice `C`.

Pre potreby zberu a analýzy meraní pri rôznych parametroch som doplnil zapisovanie nameraných časov do súborov `csv` v priečinku `data`. Meranie sa samozrejme opakuje `N_ATTEMPTS` krát a na konci každého behu programu sa vypočíta priemer, medián a smerodajná odchýlka, ktoré sa taktiež zapíšu na koniec csv súboru.

Merania som vykonával násobením štvorcových matíc veľkosti `48x48`, `96x96`, `192x192` a `432x432` prvkov, s vždy `1, 2, 3, 4, 6, 8, 12 a 16` počtom procesov. Ďalej som skúšal matice s veľa riadkov / málo stĺpcov a naopak s výsledkom veľkosti `48x432` a `432x48`.

Merania menších matíc som opakoval 500-krát, pri matici veľkosti `192x192` 100-krát a pri veľkých maticiach s 432 riadkami/stĺpcami 25-krát.

Taktiež prebehli merania vždy obidvoch metód komunikácie `par` pre P2P a `parsg` pre kolektívne metódy.

Výsledky sú zapísané v csv súboroch s názvom:
```N_ATTEMPTS_times_C[rozmer matice]_metóda.csv```

V nasledujúcom grafe sa môžme pozrieť na výsledky meraní násobenia matiíc `48x48` paralelne s rôznym počtom procesov s P2P metódou komunikácie.

![Graf 1](https://github.com/BackSpace16/Vizvary-111488-PPDS2024/blob/07/graphs/C[48,48]_par.png?raw=true)

V ďalších grafoch môžeme pozorovať priemery výsledkov meraní pre štvorcové matice s rôznym počtom procesov pre obidve metódy.

<img src="https://github.com/BackSpace16/Vizvary-111488-PPDS2024/blob/07/graphs/allsquare.png?raw=true" width=50% height=50%>
<img src="https://github.com/BackSpace16/Vizvary-111488-PPDS2024/blob/07/graphs/smallsquare.png?raw=true" width=50% height=50%>

Nasledujúci graf porovnáva neštvorcové matice s výsledkom `48x432` a `432x48` a matice `48x48`.

<img src="https://github.com/BackSpace16/Vizvary-111488-PPDS2024/blob/07/graphs/notsquare.png?raw=true" width=50% height=50%>

Posledné 2 grafy ukazujú porovnanie metód komunikácie pri násobení najmenších meraných matíc `48x48` a najväčších meraných `432x432`, kde môžeme pozorovať lepšie výsledky P2P komunikácie pri násobení malých matíc.

<img src="https://github.com/BackSpace16/Vizvary-111488-PPDS2024/blob/07/graphs/C[48,48].png?raw=true" width=50% height=50%>
<img src="https://github.com/BackSpace16/Vizvary-111488-PPDS2024/blob/07/graphs/C[432,432].png?raw=true" width=50% height=50%>

Nakoniec môžem konštatovať, že rýchlosť obidvoch metód komunikácie je vo väčšine prípadoch veľmi podobná, môžeme však pozorovať o trošku lepšie výsledky pri použití kolektívnej komunikácie. Môžeme si však všimnúť, že metóda P2P komunikácie je o trošku rýchlejšia pri násobení najmenších meraných matíc `48x48`.