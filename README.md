# worldtour.exsports.fi

EXS World Tour -pelin sivusto: esittely, ohje ja maailmanlista. Staattinen sivusto, joka julkaistaan Firebase Hostingiin.

## Rakenne

- `build.py` tuottaa HTML-sivut. Muokkaa sivujen sisältöä tässä tiedostossa, älä `index.html`-tiedostoissa, ja aja `python build.py`.
- `assets/css/tokens.css` ja `assets/css/bundle.css` tulevat pelin suunnittelujärjestelmästä (EXS World Tour, Viimeinen valo -teema). `assets/css/site.css` on sivuston oma asettelu.
- `assets/fonts/` Barlow-fontit woff2-muodossa (SIL Open Font License).
- `tools/check.py` tarkistaa sisäiset linkit; GitHub Actions ajaa sen ennen julkaisua.
- `lista/` ja `s/` näyttävät nyt esimerkkidataa. Oikea data tulee Firebase-rajapinnasta, kun World Rankin tekninen kokeilu on valmis (pelirepo: `Docs/plans/2026-10-01-sivusto-ja-world-rank.md`).

## Julkaisu Firebase Hostingiin

Sivusto julkaistaan pelin Firebase-projektin `exs-worldtour` oletussivustolle `exs-worldtour` (kohde `worldtour` tiedostoissa `firebase.json` ja `.firebaserc`). Samassa projektissa ovat pelin Auth, Firestore, telemetrian Realtime Database ja tuleva tilipalvelu `exs-accounts` (Cloud Run, `europe-west1`); niiden asetukset ovat pelirepon `firebase/`-hakemistossa. Tästä reposta julkaistaan vain Hosting.

Firebase Hosting -sivustolla on yksi julkaisu kerrallaan, joten vain tämä repo julkaisee Hostingin; pelirepon `deploy-accounts.ps1` julkaisee vain Firestore- ja Storage-säännöt. Pelin tilisivut ja `/api/**`-ohjaus Cloud Runiin lisätään tämän repon julkaisuun, kun tilipalvelu avataan (pelirepo: `Docs/architecture/2026-10-21-firebase-kokonaisuus.md`).

Pysyvät osoitteet `/privacy` ja `/terms` (myös `/en/…`) ohjataan `firebase.json`-tiedostossa tietosuojaselosteeseen ja käyttöehtoihin. `/delete-account` ohjataan toistaiseksi (302) poisto-ohjeeseen `/tili/`; kun tilisovellus tulee sivustolle, se ottaa polun itselleen. Pelin tilipalvelin ja Google Play viittaavat näihin osoitteisiin, joten älä poista ohjauksia.

Verkkotunnus `worldtour.exsports.fi` on liitetty sivustoon (Hosting › Custom domains; DNS: CNAME `worldtour` → `exs-worldtour.web.app`).

Automaattinen julkaisu tarvitsee repon salaisuuden `FIREBASE_SERVICE_ACCOUNT_WORLDTOUR`: Google Cloud Console (projekti `exs-worldtour`) › IAM › Service accounts › tili roolilla **Firebase Hosting Admin** (esikatselukanaville lisäksi **API Keys Viewer**) ja sen JSON-avain. Ilman salaisuutta työnkulku ajaa tarkistukset mutta ohittaa julkaisun; käsin julkaisu: `npx firebase-tools deploy --only hosting:worldtour --project exs-worldtour`.

Push `main`-haaraan julkaisee pääkanavan. Saman repon PR:t saavat 7 päivää voimassa olevan esikatseluosoitteen, jonka linkki tulee PR:n kommenttiin.

Paikallinen esikatselu Firebasen otsakkeilla: `npx firebase-tools emulators:start --only hosting` (http://127.0.0.1:5000/).

## Tietoturva

- Sivustolla ei ole eikä saa olla avaimia, joilla voi kirjoittaa tuloksia. Kaikki kirjoitus tapahtuu Cloud Runin tarkistuspalvelusta.
- CSP ja muut turvaotsakkeet asetetaan `firebase.json`-tiedostossa. Sama CSP on myös `<meta>`-tagissa. Kun Firebase-kirjautuminen lisätään, laajenna `connect-src` ja `script-src` molempiin.
- Ylläpitonäkymä ja tilin poisto toteutetaan tähän samaan Firebase Hosting -sivustoon.
- Jakolinkkien esikatselu (og-tagit suorituskohtaisesti) vaatii palvelimen: `/s/<tunnus>`-osoitteet ohjataan Cloud Runiin `firebase.json`-tiedoston `rewrites`-säännöllä, kun palvelu on pystyssä. Sääntöä ei voi lisätä etukäteen, koska julkaisu epäonnistuu, jos palvelua ei ole.
