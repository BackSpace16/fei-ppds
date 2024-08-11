# Semestrálne zadanie

Úlohou semestrálneho zadania bolo vytvoriť paralelný algoritmus, ktorý nájde najkratšie cesty medzi všetkými vrcholmi v orientovanom grafe s ohodnotenými hranami. 

V mojej implementácii som použil dijkstrov algoritmus ktorý hľadá najkratšie cesty z jedného vrcholu do všetkých ostatných vrcholov. Keďže úlohou bolo nájsť najkratšiu cestu medzi všetkými vrcholmi, musíme tento algoritmus spustiť pre každý vrchol. Ako vstup som používal maticu susednosti, kde počet riadkov a stĺpcov predstavuje počet vrcholov a každý riadok matice predstavuje váhy ciest z jedného vrcholu do ostatných, pričom ak medzi vrcholmi hrana neexistuje, na danej pozícií je hodnota nekonečno. Výstupom je matica najkratších vzdialeností medzi vrcholmi, podobná vstupnej matici, s tým rozdielom že hodnoty predstavujú najkratšie vzdialenosti a nie priame hrany medzi vrcholmi.

Pri meraniach som ako vstup používal matice vygenerované funkciou `generate_adj_matrix()` ktorú som vytvoril v súbore `sz.py`. Táto funkcia vygeneruje maticu susednosti s `n_vertices` vrcholmi a s hranami ohodnotenými v rozmedzí daným parametrami `min_weight` a `max_weight`. Početnosť hrán vo výslednom grafe je daná percentuálne parametrom `edge_density`, pričom `0` znamená, že graf bude obsahovať vždy len jednu hranu z a do každého vrcholu, hodnota `100` vygeneruje kompletný graf. Maticu susednosti je možné aj načítať zo súboru použitím funkcie `load_adj_matrix()`. Pri meraniach som však túto funkciu nepoužil, všetky grafy boli generované funkciou `generate_adj_matrix()`.

Dijkstrov algoritmus pre jeden vrchol je implementovaný vo funkcii `dijkstra()`, ktorej vstupmi sú matica susednosti a index vrcholu. Pre vytvorenie matice dĺžok najkratších ciest medzi všetkými vrcholmi slúži funkcia `all_dijkstra()` ktorej vstupmi sú matica susednosti a funkcia pre výpočet týchto dĺžok z jedného vrcholu. Výsledná matica tak vznikne kombináciou výstupov z dijkstrového algoritmu pre každý vrchol v grafe.

Pre overenie výsledku implementovaného algoritmu a porovnanie matíc som použil už implementovaný dijkstrov algoritmus z knižnice `NetworkX`. Vstupom funkcie `single_source_dijkstra_path_length()` je objekt grafu, ktroý sa vytvára z matice susednosti vo funkcii `adjacency_matrix_to_nxgraph()`. Funkciu `dijkstra_nxgraph()` som následne použil ako vstup do funkcie `all_dijkstra()`, pričom porovnaním výsledných matíc som zistil, že použitie funkcie `dijkstra()` vracia rovnaký správny výsledok.

Pre paralelizáciu dijkstrovho algoritmu som použil `MPI` z knižnice `mpi4py` v súbore `sz_par.py`. Hlavnou myšlienkou paralelizácie je rozdelenie vykonávania dijkstrovho algoritmu pre jednotlivé vrcholy medzi `n_proc` procesov. V prípade `n_proc` >= `N_NODES` sa vrcholy rozdelia po jednom medzi procesy, pričom počet procesov rovný počtu vrcholov vykonáva dijkstrov algoritmus a zvyšné procesy nevykonávajú nič. Vo väčšine prípadoch však počet vrcholov `N_NODES` výrazne prevyšuje počet procesov. Vtedy sa indexy vrcholov rovnomerne rozdelia medzi všetky procesy v poli `indices` a v prípade zvyšku sa aj tieto zvyšky po jednom rozdelia medzi procesy v poli `indices_tail`. Príslušné časti polí `indices` a `indices_tail` sa následne rozpošlú medzi procesy pomocou MPI funkcie `scatter()`. Dijkstrov algoritmus pre jeden vrchol potrebuje pre svoju funkciu maticu susednosti celého grafu, takže aj túto musíme rozposlať všetkým procesom pomocou funkcie `bcast()`. Následne prebehne paralelný výpočet najkratších dĺžok v každom procese a výsledky sa zozbierajú pomocou funkcie `gather()`. Nakoniec sa všetky časti spoja a výsledkom je matica s dĺžkami, ktorú som opäť porovnal so sériovým algoritmom, pričom výsledky boli vždy rovnaké.

Merania boli vykonávané vždy s `1, 2, 3, 4, 6, 8, 12 a 16` počtom procesov na procesore `Intel Core i5-12500H`. Nastavované parametre grafu predstavovali počet vrcholov grafu `N_NODES`, hustota hrán v grafe `EDGE_DENSITY` a počet opakovaní `N_ATTEMPTS` na ktorých bol meraný čas. V nasledujúcej tabuľke môžeme vidieť prehľad parametrov v jednotlivých meraniach z ktorých výsledky sú zapísané v súboroch `csv` s názvami kde čísla predstavujú postupne parametre `N_NODES`, `EDGE_DENSITY` a `N_ATTEMPTS` pre dané meranie. Stĺpce `Time_P`, kde `P` je počet procesov, predstavujú časové údaje z meraní, pričom posledné riadky na konci predstavujú priemer, medián a časovú odchýlku z daného stĺpca.

|Počet vrcholov|Podiel hrán (%)*|Počet pokusov|
|-|-|-|
|50|0|500|
|100|0, 33, 66, 100|100|
|250|0|50|
|500|0|10|
|1000|0|5|

**0 - jedna hrana z/do každého vrcholu, 100 - úplný graf*

Na výsledky meraní sa môžeme pozrieť v nasledujúcich grafoch.

Každé meranie prebiehalo s rôznym počtom pokusov, v nasledujúcom grafe vidíme meranie času vykonania algoritmu na 500 rôznych grafov s 50 vrcholmi.

![Graf 1](https://github.com/BackSpace16/Vizvary-111488-PPDS2024/blob/sz/graphs/attempts.png?raw=true)

V nasledujúcich grafoch sa pozrieme na súhrnné hodnoty času predstavujúce medián zo všetkých pokusov daného merania pre rôzny počet procesov. V prvom grafe vidíme merania s grafom s 100 vrcholmi a môžeme vidieť porovnanie nastavení s rôznym počtom hrán kde vidíme, že spracovanie riedkych grafov s menším počtom hrán bolo rýchlejšie ako grafy s väčšou hustotou hrán. V druhom grafe vidíme porovnanie s meraniami menšieho grafu s 50 vrcholmi a väčšieho grafu s 250 vrcholmi.

<p align="center">
    <img src="https://github.com/BackSpace16/Vizvary-111488-PPDS2024/blob/sz/graphs/100.png?raw=true" width=45%>
    <img src="https://github.com/BackSpace16/Vizvary-111488-PPDS2024/blob/sz/graphs/50_100_250.png?raw=true" width=45%>
</p>

V ďalších grafoch vidíme porovnanie meraní malých grafov s 50 a 100 vrcholmi a súhrnný graf všetkých meraní riedkych grafov.

<p align="center">
    <img src="https://github.com/BackSpace16/Vizvary-111488-PPDS2024/blob/sz/graphs/small.png?raw=true" width=45%>
    <img src="https://github.com/BackSpace16/Vizvary-111488-PPDS2024/blob/sz/graphs/all.png?raw=true" width=45%>
</p>

Vidíme, že zo zvyšujúcim sa počtom procesov sa čas vykonania algoritmu skracuje, čo bolo našim cieľom paralelizácie.

### Zdroje:
https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/
https://en.wikipedia.org/wiki/Parallel_all-pairs_shortest_path_algorithm
https://networkx.org/documentation/stable/tutorial.html
https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.single_source_dijkstra_path_length
https://github.com/BackSpace16/Vizvary-111488-PPDS2024/tree/07
