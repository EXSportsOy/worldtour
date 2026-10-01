# EXS World Tourin oikeudellisten sivujen ylläpito

Päivitetty 1.10.2026. Varsinaiset tekstit ovat `fi/`- ja `en/`-hakemistojen HTML-sisältöpalat. `legal_content.py` tuottaa navigoinnin ja sisällysluettelon, ja `build.py` kokoaa sivut. `{{prefix}}` korvataan dokumentin kielen mukaisella polulla. Älä muokkaa generoituja HTML-sivuja käsin.

Asiakirjat: käyttöehdot, tietosuojaseloste, tilin/tietojen poistaminen, ostot ja hyvitykset, World Rank -säännöt sekä evästeet. Suomen- ja englanninkieliset tekstit ovat erilliset, joten muutokset on tehtävä molempiin. Muissa sivuston kielissä näytetään selkeästi merkitty englanninkielinen versio.

## Tila

Käyttöehdot, ostoehdot, World Rank -säännöt ja tietosuojaseloste ovat tarkistettavia luonnoksia. Poisto-ohje ja evästetiedot kuvaavat nykyistä sivustoa/testiä. Luonnoksen päivämäärä ei ole ehtojen takautuva voimaantulopäivä. Päätä käyttöönotto ja versionhallinta erikseen, kun sisältö ja pelin toteutus vastaavat toisiaan.

Vahvistetut lähtötiedot: EXSports Oy; yritystiedot https://www.exsports.fi/legal/imprint.html ; info@exsports.fi; testin13vuoden ikäraja; täysversion PEGI3-tavoite; testitiedot enintään90päivää testijakson päättymisestä. Aiemman testiruudun lyhyempää säilytyslupausta ei pidennetä takautuvasti. Automaattinen poistopainike on suunnitelma.

## Ennen lopullisten tekstien käyttöönottoa

1. Korjaa testianalytiikan hyväksyntä ja peruuttaminen niin, että valittu käsittelyperuste toteutuu aidosti. Pelkkä käyttöehdon tai verkkosivun muuttaminen ei korjaa toiminnallisuutta.
2. Vahvista pilvipalvelujen alueet, tietojenkäsittelysopimukset, siirtoperusteet, käyttöoikeudet ja varmuuskopioiden poistuminen. Supabase on nykyinen vastaanottaja; Firebase on tuleva muutos.
3. Toteuta ja tarkista yksilöitävien testitietojen määräaikainen poisto, tukipyyntöjen kohdistaminen ja lopulliset muiden tietoryhmien säilytysajat.
4. Toteuta tilin ja siihen liittyvien tietojen poisto pelissä ja ulkoinen pyyntöreitti ennen tilien avaamista. Tarkista Google Play Data safety ja tietosuojalinkit todellista buildia vasten.
5. Vahvista lasten kohdeyleisö, lopullinen sisältöluokitus, verkkotilien ikäkäytäntö ja mahdollinen huoltajan suostumus maittain. Sisältöluokitus ei ratkaise näitä yksin.
6. Tarkista ostotuotteet, käyttöoikeuksien palautus ja oston yhteydessä annettavat tiedot ennen maksullisen julkaisun avaamista. Julkaisupäivää, uutta rataa tai viikkokisaa ei ole tässä luvattu.
7. Päivitä palvelukohtaiset ehdot ennen World Rankin tai palkintokilpailun avaamista. Arvioi yleisölle jaettavaan käyttäjäsisältöön soveltuvat DSA-velvoitteet erikseen.
8. Poista luonnosmerkinnät vasta tarkastuksen ja tarvittavien toteutusmuutosten jälkeen. Säilytä aiemmat käytössä olleet ehdot päivättyinä, kerro muutoksista asianmukaisesti ja päivitä molemmat kielet.

## Tarkistukset

```text
python build.py
python tools/check.py
python tools/check_legal.py
```

Tarkistukset kattavat paikalliset linkit ja asiakirjojen rakenteen. Ne eivät vahvista juridista pätevyyttä, pilven asetuksia, toimivaa sähköpostipalvelua tai vielä puuttuvia pelitoimintoja. Pääsivuston yritystietolinkkiä ei ole sisällytetty peliehtojen yleiseksi vastuunrajoitukseksi.

## Lähteet (tarkistettu 1.10.2026)

- Yritystiedot: https://www.exsports.fi/legal/imprint.html (luettu selaimessa).
- KKV, digitaaliset sisällöt: https://www.kkv.fi/kuluttaja-asiat/digitaaliset-sisallot-ja-palvelut/
- KKV, peruuttamisoikeus: https://www.kkv.fi/kuluttaja-asiat/verkkokauppa/peruuttamisoikeus-verkkokaupassa/
- Euroopan komissio, rekisteröidyn tiedot ja oikeudet: https://commission.europa.eu/law/law-topic/data-protection/information-individuals_en
- Euroopan komissio, käsittelyperusteet: https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/legal-grounds-processing-data_en
- Euroopan komissio, pyyntöjen käsittely: https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/dealing-requests-individuals_en
- EDPB, suostumusohje05/2020: https://www.edpb.europa.eu/sites/default/files/files/file1/edpb_guidelines_202005_consent_en.pdf
- Google Play, käyttäjätiedot: https://support.google.com/googleplay/android-developer/answer/10144311
- Google Play, tilinpoisto: https://support.google.com/googleplay/android-developer/answer/13327111
- Google Play, Families: https://support.google.com/googleplay/android-developer/answer/9893335
- GitHub Pages, tiedonkeruu: https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages#data-collection
- GitHub, tietosuoja: https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement
- Supabase, tietojenkäsittelyehdot: https://supabase.com/legal/dpa
- Traficom, evästeet: https://www.kyberturvallisuuskeskus.fi/fi/toimintamme/saantely-ja-valvonta/evasteet
- EU:n suljetun ODR-palvelun korvaava ohje: https://consumer-redress.ec.europa.eu/site-relocation_en
