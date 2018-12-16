## Raspberry pi projekcija

### Priprava
* Raspberry in projektorj povežemo s HDMI kablom in Ethernet kablom.
* Če projektor to omogoča, nastavimo IP projektorja na `192.168.1.143` ter vključimo PjLink protokol. Nastavitev bo potrebna za kontrolna ukaza vklop in izklop. V primeru, da PjLink protokol ni mogoč, lahko odstranimo Ethernet kabel. Projektor bo treba vključiti in izključiti ročno.
* V Raspberry vstavimo USB ključek s slikami za prikaz.
* USB naj vsebuje mapo `/diapozitivi`, v kateri so datoteke, ki jih bomo predvajali.  
* Datoteke lahko oštevilčimo tako, da ime datoteke vsebuje številko. Na primer: `datoteka_11_test.pdf`.
* Podprt je format .pdf ter popularni slikovni formati (.jpg, .png, ...).
* Raspberry priključimo na vir energije in počakamo slabo minuto, da se sistem vzpostavi.
* Program ob vzpostavitvi poišče USB ključek in prebere datoteke.
* Branje ključka lahko sprožimo ročno z ukazom `0001 Enter`.

### Uporaba pilota
* S telefonom ali računalnikom se povežemo na omrežje: `SSID: malina, geslo: malina18`.
* Če se omrežje `malina` ne prikaže, raspberry ponovno zaženemo (izključimo in vključimo napajalni kabel).
* Pilot najdemo na naslovu `192.168.2.1:5001/remote`.
* Na voljo so številčnica in ukazne tipke.
* Z uporabo številčnice lahko dostopamo do oštevilčenih datotek: vpišemo številko in pritisnemo `Enter`.
* Zgoraj desno se prikaže ime datoteke, ki se trenutno predvaja.
* Prikazane oštevilčene datoteke se shranjujejo v spomin, po katerem se lahko sprehajamo s puščicama `levo` in `desno`.
* S puščicama `gor` in `dol` se sprehajamo po vseh datotekah. Seznam je zgrajen tako, da so na začetku oštevilčene datoteke, sledijo pa vse ostale datoteke.
* Tipka `Sleep` prikaže povsem črno datoteko in s tem simulira zatemnjeni zaslon. Zaslon prižgemo nazaj s tipko `On`.
* Tipka `Off` ugasne projektor. S tipko `On` projektor prižgemo in nadaljujemo kjer smo ostali. *

### Priprava projektorja ViewSonic
Za podrobnejši opis glej navodila za uporabo projektorja (datoteka `viewsonic_pj1158.pdf`). Spodaj so ključni koraki: 

* IP projektorja nastavimo na `192.168.1.143`. 
* Če je mogoče, nastavimo preko menija s pilotom. Sicer se moramo povezati na spletni vmesnik projektorja (lahko priključimo RPI, se s telefonom ali računalnikom povežemo na omrežje ter v iskalno vrstico brskalnika vtipkamo IP naslov projektorja.)
* V nastavitvah vkjlučmo `Control port (Port: 23)`.
* Izključimo avtentikacijo za ta port (nekje mora biti kljukica za `Authentication`). 
* Vkjlučimo tudi `Control port (Port: 9715)`.
* Izključimo avtentikacijo za ta port (nekje mora biti kljukica za `Authentication`). 
* Kliknemo gumb `Apply`,  da shranimo nastavitve. 
* Povežemo se na polot in preizkusimo funkcije `On` in `Off`. Funkcije so v testnem stanju: vsak gumb projektorjev pošlje več ukazov s časovnim zamikom z upanjem, da bo eden pravilen. Če se po pol minute ne zgodi nič, lahko sklepamo, da ukazi ne delujejo. 

