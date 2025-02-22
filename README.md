# Ravintolat
Sovelluksessa näkyy sovellukseen lisätyt ravintolat, joista voi etsiä tietoa ja lukea arvioita. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.
 * Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen. TOTEUTETTU
 * Käyttäjä näkee ravintolat kartalla ja voi painaa ravintolasta, jolloin siitä näytetään lisää tietoa (kuvaus, kategoriat, sijainti ja arviot).TOTEUTETTU
 * Kirjautunut käyttäjä voi antaa arvion (tähdet ja kommentti) ravintolasta ja kaikki käyttäjät voivat lukea muiden antamia arvioita.TOTEUTETTU
 * Ylläpitäjä voi lisätä ja poistaa ravintoloita sekä määrittää ravintolasta näytettävät tiedot. TOTEUTETTU
 * Käyttäjä voi etsiä kaikki ravintolat, joiden kuvauksessa on annettu sana.TOTEUTETTU
 * Käyttäjä näkee myös listan, jossa ravintolat on järjestetty parhaimmasta huonoimpaan arvioiden mukaisesti.TOTEUTETTU
 * Ylläpitäjä voi tarvittaessa poistaa käyttäjän antaman arvion. TOTEUTETTU
 * Ylläpitäjä voi luoda ryhmiä, joihin ravintoloita voi luokitella. Ravintola voi kuulua yhteen tai useampaan ryhmään.TOTEUTTETTU
 * Ylläpitäjä voi tarvittaessa poistaa ryhmiä. TOTEUTETTU



## Ohjeet sovelluksen käynnistämiseen paikallisesti:

1. Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon.
2. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:  
``  
DATABASE_URL=tietokannan-paikallinen-osoite  
``  
``  
SECRET_KEY=salainen-avain  
``

4. Aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet virtuaaliympäristöön komennoilla:  
``  
$ python3 -m venv venv
``  
``  
$ source venv/bin/activate  
``  
``  
$ pip install -r ./requirements.txt  
``  
6. Määritä tietokannan skeema komennolla:  
``
$ psql < schema.sql
``
7. Luo sovellukseen admin-käyttäjä:
``
$ psql < seed.sql
``
8. Käynnistä sovellus komennolla:  
``
$ flask run
``

Admin-käyttäjän tiedot 

* tunnus: Admin
* salasana: password

