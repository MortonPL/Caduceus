## Szybki start

Wymagania: Python >= 3.6.8

`./testenv.sh` - tworzy przykładowe środowisko do testów

`python caduceus.py testenv/X testenv/Y1 testenv/Y2` - przykładowe użycie programu do ww. środowiska

## Użycie

`python caduceus.py -h` wyświetla pomoc dla programu.

`usage: caduceus.py [-h] [-m [MODES]] [-c [CONFIG]] [-a] target directories [directories ...]`

* `-m [MODES]` lub `--modes [MODES]` - lista akcji (rozdzielonych przecinkiem) do wykonania. Domyślna wartość to *wszystkie* akcje w podanej kolejności:
  * `empty` - wykryj i usuń pliki puste
  * `temp` - wykryj i usuń pliki tymczasowe
  * `dupes` - wykryj pary plików o tej samej zawartości i usuń nowszy
  * `badnames` - wykryj pliki o nazwach z "nielegalnymi" znakami i popraw je
  * `samenames` - wykryj pary plików o tych samych nazwach i usuń starszy
  * `flags` - wykryj pliki o niestandardowych prawach dostępu i skoryguj je
  * `movable` - wykryj pliki, których nie ma w `target` i przenieś je

* `-c [CONFIG]` lub `--config CONFIG` - ścieżka do pliku konfiguracyjnego. Domyślna wartość to plik `caduceus.conf` w tym samym katalogu, co plik `caduceus.py`.

* `-a` lub `-all` - program nie będzie pytał użytkownika o potwierdzenie akcji.

* `target` - ścieżka do katalogu, który chcemy uporządkować. Parametr obowiązkowy.

* `directories` - lista ścieżek (oddzielonych spacją), które będziemy brać pod uwagę. Paramter obowiązkowy.

## Konfiguracja

Domyślna zawartość pliku `caduceus.conf`:

```
[Globals]
DefaultFilePermissions= rw-r--r--
IllegalCharacters= : , ; * ? $ # ' | \ "
IllegalCharacterReplacement= _
TemporaryFileExtensions= *~ *.tmp
```

Wszystkie opcje muszą się znajdować w sekcji \[Globals\].

* `DefaultFilePermissions` - ciąg znaków określający domyślne prawa dostępu do wszystkich plików

* `IllegalCharacters` - lista znaków oddzielonych spacją, które będą "nielegalne" w nazwie pliku

* `IllegalCharacterReplacement` - znak, na który zmienione zostaną znaki "nielegalne"

* `TemporaryFileExtensions` - lista wzorców nazw plików oddzielonych spacją, które zostaną uznane za tymczasowe. Znak \* oznacza dowolny ciąg znaków (w tym pusty).

## Działanie

Po uruchomieniu programu z zadanymi argumentami, program będzie po kolei wykonywał akcje. Dla każdego znalezionego pliku z dostępną akcją, użytkownik zostanie zapytany o potwierdzenie, np. `[...] is empty. Remove? ([Y]es/[a]ll/[n]o/[s]kip)`.

* `y` (domyślnie) - akceptuje wykonanie tej akcji dla tego pliku

* `a` - akceptuje wykonanie tej akcji dla wszystkich plików (np. usuń wszystkie puste)

* `n` - pomija wykonanie tej akcji dla tego pliku

* `s` - pomija wykonanie tej akcji dla wszystkich plików

Program kończy działanie, gdy dla wszystkich akcji zostaną zaakceptowane (lub pominięte) wszystkie problematyczne pliki.

## Przykład

Skrypt `testenv.sh` tworzy przykładowe środowisko do testowania działania z następującym drzewem plików:

```
testenv
|---X
|   |---- a - zawiera "A"
|   |---- b - zawiera "B"
|   |---- z - zawiera "A" (duplikat testenv/X/a, nietypowe flagi)
|
|---Y1
|   |---- .tmp - zawiera "" (pusty, tymczasowy, nie ma w X)
|   |---- a - zawiera "A" (duplikat testenv/X/a, duplikat testenv/X/z, taka sama nazwa co testenv/X/a)
|   |---- c; - zawiera "C" (nielegalna nazwa, nietypowe flagi, nie ma w X)
|
|---Y2
|   |---- a - zawiera "aa" (taka sama nazwa co testenv/X/a, taka sama nazwa co testenv/Y1/a)
|   |---- b - zawiera "" (pusty, duplikat testenv/Y1/.tmp, taka sama nazwa co testenv/X/b)
|   |---- d - zawiera "D" (nietypowe flagi, nie ma w X)
```

Wywołanie programu `python caduceus.py testenv/X testenv/Y1 testenv/Y2` wykona wszystkie akcje z katalogiem-celem `testenv/X` i dodatkowymi `testenv/Y1` i `testenv/Y2`, pytając użytkownika o potwierdzenie. W przypadku zaakceptowania wszystkiego, wynik działania programu będzie następujący:

```
testenv
|---X
|   |---- a - zawiera "A"
|   |---- b - zawiera "B"
|   |---- c_ - zawiera "C" 
|   |---- d - zawiera "D"
|
|---Y1
|---Y2
```
