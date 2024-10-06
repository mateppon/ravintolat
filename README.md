# Ravintolat
Sovelluksessa näkyy tietyn alueen ravintolat, joista voi etsiä tietoa ja lukea arvioita. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.
 * Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen. TOTEUTETTU
 * Käyttäjä näkee ravintolat kartalla ja voi painaa ravintolasta, jolloin siitä näytetään lisää tietoa (kuten kuvaus ja aukioloajat).
 * Käyttäjä voi antaa arvion (tähdet ja kommentti) ravintolasta ja lukea muiden antamia arvioita.
 * Ylläpitäjä voi lisätä ja poistaa ravintoloita sekä määrittää ravintolasta näytettävät tiedot. TOTEUTETTU OSITTAIN - Tällä hetkellä kaikki käyttäjät voivat täyttää ravintolan lisäämiseen tarkoitetun lomakkeen. Toistaiseksi ravintolan tiedot eivät tallennu tietokantaan. 
 * Käyttäjä voi etsiä kaikki ravintolat, joiden kuvauksessa on annettu sana.
 * Käyttäjä näkee myös listan, jossa ravintolat on järjestetty parhaimmasta huonoimpaan arvioiden mukaisesti.
 * Ylläpitäjä voi tarvittaessa poistaa käyttäjän antaman arvion.
 * Ylläpitäjä voi luoda ryhmiä, joihin ravintoloita voi luokitella. Ravintola voi kuulua yhteen tai useampaan ryhmään.



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
7. Käynnistä sovellus komennolla:  
``
$ flask run
``
