# Iskanje po zbirki dokumentov
Repozitorij vsebuje dokumente in programe, ki so potrebni za iskalnik po zbirki dokumentov, ki je nastajal v okviru projekta pri predmetu Matematično modeliranje (UL FRI - uni, 2. letnik). 

## Vsebina
Trenutno je v repozitoriju le branch main, ki vsebuje 10 dokumentov s tekstovno vsebino.

## Projekt
Izdelujemo iskalnik relevantnih dokumentov po ključnih besedah z uporabo metode **latentnega semantičnega indeksiranja** ali **LSI**. 

1. Iz zbirke dokumentov zgradite matriko $A$ povezav med besedami in dokumenti. Vsak dokument naj ima v matriki svojo stolpec, vsaka beseda pa svojo vrstico. Element aij naj bo frekvenca i-te besede v j-tem dokumentu. Ker uporabljava knjižnjico `NumPy` je v terminalu treba zagnati: `pip install numpy`
2. Matriko A razcepite z odrezanim SVD razcepom $A = U_{k}S_{k}V_{k}^{T}$, ki obdrži le k največjih singularnih vrednosti. Razmislite kaj predstavljajo stolpci matrike $U_{k}$ in matrike $V_{k}$. Odrezan SVD zmanjša t. i. ”overfitting” (preveliko prilagoditev modela podatkom, kar povzroči povečan vpliv šuma).
3. Iskani niz besed (poizvedbo) zapišite z vektorjem $q$. Iz poizvedbe $q$ generirajte vektor v prostoru dokumentov s formulo $q = q^{T}U_{k}S_{k}^{−1}$. Iskanim dokumentom ustrezajo stolpci $V_{k}$, ki so dovolj blizu vektorju $q$. Za razdaljo uporabite kosinus kota med dvema vektorjema in ne Evklidske razdalje med njima. Poizvedba naj vrne dokumente, za katere je kosinus večji od izbrane mejne vrednosti. Preskusite različne mejne vrednosti kosinusa, pri kateri izberemo dokument (0.9, 0.7, 0.6, ...).
