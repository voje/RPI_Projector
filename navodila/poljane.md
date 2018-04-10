## Raspberry pi projekcija

### Priprava
* V Raspberry vstavimo usb ključek s slikami za prikaz.
* Datoteke lahko oštevilčimo tako, da ime datoteke vsebuje številko.
* USB naj vsebuje mapo `/diapozitivi`, v kateri so datoteke, ki jih bomo predvajali.  
* Podprt je format .pdf ter popularni slikovni formati (.jpg, .png).
* Raspberry priključimo na vir energije in počakamo do 1 minuto, da se sistem vzpostavi.
* Branje ključka lahko sprožimo ročno z ukazom `0001 Enter`.

### Uporaba pilota
* S telefonom ali računalnikom se povežemo na omrežje: `SSID: malina, geslo: malina18`.
* Pilot najdemo na naslovu `192.168.2.1:5003/remote`.
* Na voljo je številčnica in ukazne tipke.
* Z uporabo številčnice lahko dostopamo do oštevilčenih datotek: vpišemo številko in pritisnemo `Enter`.
* Prikazane oštevilčene datoteke se shranjujejo v spomin, po katerem se lahko sprehajamo s puščicama levo in desno.
* S puščicama gor in dol se sprehajamo po vseh datotekah. Seznam je zgrajen tako, da so na začetku oštevilčene datoteke, sledijo pa vse ostale datoteke.
* Tipka `Sleep` prikaže povsem črno datoteko in s tem simulira zatemnjeni zaslon. Zaslon prižgemo nazaj s tipko `On`.
* Tipka `Off` ugasne projektor. S tipko `On` projektor prižgemo in nadaljujemo kjer smo ostali.

### Opomba
Tipki `On` in `Off` sta odvisni od podpore projektorja. Nekateri projektorji ne podpirajo tehnologije za upravljanje preko omrežja. V tem primeru je treba projektor zagnati in ugasniti ročno. Zatemnitev se lahko simulira z uporabo tipk `Sleep` in `On`.

