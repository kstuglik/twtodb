# TW to database

hashtags-getter

### W projekcie znajdują się foldery:
*  ```data```
   *  pliki JSON
*  ```list_first```
   *  informacje o last_id i first_id wykonanego przeszukiwania


#### Kolejność uruchamiania skryptów:
domyslne wywolanie:
```sh
python twitter2.py -1 -1 -1
```

pobieranie nowych od znanego id:
```sh
python twitter2.py -1 id -1
```

pobieranie wczesniejszych od znanego id:
```sh
python twitter2.py id -1 -1
```

### PREPARE MONGODB

```sh
docker pull mongo docker run -d -p 27017:27017 -v ~/data:/data/db mongo
```

Jeśli wystąpi komunikat, że dany port jest używany to trzeba go zmienić lub "zwolnić" i powtórzyć wcześniejsze komendy:
```sh
netstat -nlp | grep 27017 kill PID
```

Sprawdzenie czy docker chodzi:
```sh
docker ps
```

Jeśli mongo-client nie jest zainstalowany to:
```sh
sudo apt-get install mongodb-clients
```

Uruchomienie servera mongo:
```sh
mongo
```

jeśli jesteśmy zalogowani to działa