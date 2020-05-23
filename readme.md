# TW to database

hashtags-getter

### W projekcie znajdują się foldery i pliki:
*  ```data```
   *  pliki JSON
*  ```last_first.json```
   *  informacje o last_id i first_id ostatnio wykonanego przeszukiwania


#### Kolejność uruchamiania skryptów:
domyslne wywolanie:
```sh
    1) python test.py <start_id> <end_id> <time> <output_prefix> <query>
==> 2) python test.py
```


W trakcie działania programu pobierane są pliki i zapisywane są informcje o last_id i first_id. Wewnątrz programu jest lista składająca się z interesujących nas tagów.


### PREPARE MONGODB (DOCKER SHOULD BE AVAILABLE)

Jeśli mongo-client nie jest zainstalowany to:
```sh
sudo apt-get install mongodb-clients 
```

Instalacja dockera: https://docs.docker.com/install/


```sh
docker pull mongo
```


### RUN MONGODB (EVERYTIME)
Uruchomienie dockera w CLI poprzez wywołanie polecenia:
```sh
docker run -d -p 27017:27017 -v ~/data:/data/db mongo
```

~/data - to katalog, który musi istnieć

Uruchomienie mongodb w CLI (POLECENIE WYKONYWANE ZA KAŻDYM RAZEM):
```sh
mongo
```

Jeśli wystąpi komunikat, że dany port jest używany to trzeba go zmienić lub "zwolnić" i powtórzyć wcześniejsze komendy:
```sh
netstat -nlp | grep 27017 
kill PID
```

Sprawdzenie czy docker działa:
```sh
docker ps
```


Jeżeli wkurza Cie docker i najprostrze wydaje sie jego ponowne zainstalowanie to:
```sh
https://docs.docker.com/engine/install/ubuntu/

```