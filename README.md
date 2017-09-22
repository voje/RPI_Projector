# Predstavitev .pdf preko RPI  

Kristjan Voje

# NAVODILA (slo)  
## PRIPRAVA STROJNE OPREME  

* priklopi IR sprejemnik  

Postavi raspberry pi tako, da so v zgornjem levem kotu. Pini si sledijo v zaporedju:  
  
p0 p2 p4 p6 p8 p10   
p1 p3 p5 p7 p9 p11   
  
* Postavi IR sprejemnik tako, da je valjasta izboklina obrnjena k tebi, pini pa gledajo navzgor.  

Pini si sledijo od leve proto desni: r0, r1, r2.   

Poveži pine:   
r0 -- p10  
r1 -- p1    
r2 -- p4   
  
* poveži RPI in projektor s HDMI  
* poveži RPI in projektor z LAN (testirano tudi preko Linxis routerja z DHCP)  
* riključi USB napajalni kabel  
* počakaj, da se sistem vzpostavi (cca 1 min - ne bo odziva na pritiske pilota)  

## POVEZAVA NA RPI (vzdrževanje)  
### Povezava preko routerja  
Če imamo na voljo router, priključimo RPI z ethernet kablom in se povežemo preko ssh povezave.
RPI ima fiksen ipv4: `192.168.1.142`. Tudi CASIO projektor ima fiksen ipv4: `192.168.1.143`.
```bash
$ssh pi@192.168.1.142
```
### Povezava direktno preko ethernet kabla  
Na laptopu dodaj povezavo preko kabla in se poveži na RPI preko zgornjega postopka.
Primer lokalne nastavitve: (potrebuješ statičen IP, saj tu ni DHCP serverja)
ip 				mask 			gateway
192.168.1.12	255.255.255.0	192.168.1.0

## KONFIGURACIJA NOVEGA PILOTA  
Konfiguracijske datoteke za pilote se nahajajo v `/etc/lirc/remote_configs/`.
Povezava na konfiguracijo pilota je nastavljena v `/etc/lirc/lircd.conf`.
V git repozitoriju je primer, kako mora zgledati direktorij `/etc/lirc`.

Izklopi lirc daemon, konfiguriraj, vklopi lirc daemon.
Konfiguriraj tipke, navedene v ./lirc/lircrc.

```bash
$cd /etc/lirc/remote_configs/  
$sudo /etc/init.d/lirc stop  
$sudo irrecord --device=/dev/lirc0 IME_PILOTA.conf
$sudo /etc/init.d/lirc start
```

Nato nastavi povezavo v `/etc/lirc/lircd.conf`. Datoteka naj vsebuje eno vrstico:
```bash
include "/etc/lirc/remote_configs/IME_PILOTA.conf"
```

Testiraj z uporabo:
```bash
#raw data
sudo mode2 -d /dev/lirc0
#lirc output (imena tipk, ki smo jih nastavili)
sudo irw
```

## NASTAVITVE V RASPBIAN:  
### DEPENDENCIES  
python2, lirc, xpdf
### IZKLOPI UGAŠANJE ZASLONA ALI SPANJE  
Tu se je treba poigrati z nastavitvami. Mismim, da sem za ugašanje zaslona moral naložiti xscreensaver, preko čigar menija sem izklopil ugašanje zaslona.
### POŽENI SKRIPTO OB ZAGONU  
V datoteki `/home/pi/.config/lxsession/LXDE-pi/autostart` dodaj vrstico:
```bash
@python /home/pi/git/RPI_Projector/python_script/main.py 2>error.log
```
Ne pozabi nastaviti pravic za python.py. (chmod +x)
### SAMODEJNO UPORABI HDMI  
V datoteki `/boot/config.txt` odkomentiraj vrstici:
```bash
hdmi_force_hotplug=1
hdmi_drive=2
```
### ZASUKAJ DISPLAY  
V datoteki `/boot/config.txt` dodaj eno od spodnjih vrstic:
```bash
display_rotate=0 Normal
display_rotate=1 90 degrees
display_rotate=2 180 degrees
display_rotate=3 270 degrees
display_rotate=0x10000 horizontal flip
display_rotate=0x20000 vertical flip
```

## FUNKCIONALNOSTI  
* Sistem se vzpostavi samodejno ob vklopi v el. omrežje. (vzpostavitev cca. 1 min)  
* Sistem zazna 1 USB (še vedno lahko v druge vhode priključimo druge naprave).
Usb naj vsebuje mapo `diapozitivi`, ta pa naj vsebuje .pdf datoteke. Ob priključitvi USB sistem samodejno uporabi diapozitive z USB. Ko USB odstranimo, se sistem vrne k privzeti mapi diapozitivi.
* S pilotom lahko iteriramo po datotekah po abecednem vrstnem redu. (pageup pagedown)
* Lahko vpišemo številko datoteke in s klikom na enter (trikotnik) prikažemo datoteko. Tu iščemo po številki, zapisani v imenu datoteke, bolj natančno prvi številki v imenu, če je teh več, in ne po zaporedni številki datoteke.
* Vse poizvedbe z uporabo tipke enter (trikotnik) se shranijo v notranji spomin. Notranji spomin ima nastavljeno velikosc (npr 5 datotek). Ko so vsa mesta zapolnjena, se ob zapisu nove datoteke najstarejši vnos izbriše. Po spominu lahko iteriramo z uporabo tipk volumeup, volumedown.
* V primeru, da smo se pri vnašanju številke zmotili, jo pobrišemo s tipko delete (rdeča, levo od enter).
* S pilotom preko RPI nadzorujemo projektor. S tipko quit (rdeča, zgoraj desno), projektor vključimo, s tipko back pa projektor izključimo (standby mode).
