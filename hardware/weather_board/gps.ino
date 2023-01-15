#include <SoftwareSerial.h>
#include <TinyGPS.h>
// nastavení propojovacích pinů
#define TX 6
#define RX 13
// inicializace GPS a komunikace po softwarové sériové lince
TinyGPS gps;
SoftwareSerial swSerial(RX, TX);

void setup() {
  // zahájení komunikace po sériové lince
  Serial.begin(9600);
  // zahájení komunikace s GPS modulem po softwarové sériové lince
  swSerial.begin(9600);
}

void loop() {
  // vytvoření dočasných proměnných pro načtení informací o komunikaci s GPS modulem
  bool novaData = false;
  unsigned long znaky;
  unsigned short slova, chyby;
  // po dobu jedné vteřiny budeme kontrolovat příjem dat z GPS
  for (unsigned long start = millis(); millis() - start < 1000;) {
    // kontrola aktivity softwarové komunikace
    while (swSerial.available()) {
      // vytvoření proměnné pro uložení načtených dat z GPS
      char c = swSerial.read();
      //Serial.write(c); // pro výpis přijatých dat odkomentujte tento řádek
      // dekódování přijaté zprávy s kontrolou platných dat
      if (gps.encode(c)) {
        // pokud jsou přijatá data platná, nastavíme proměnnou pro tištění dat
        novaData = true;
      }
    }
  }
  // pokud proběhl příjem nových dat, vytiskneme všechny dostupné informace
  if (novaData) {
    // vytvoření dočasných proměnných pro načtení dat z GPS modulu
    float zSirka, zDelka;
    unsigned long stariDat;
    int rok;
    byte mesic, den, hodina, minuta, sekunda, setinaSekundy;
    // načtení GPS pozice do proměnných
    gps.f_get_position(&zSirka, &zDelka, &stariDat);
    // vytištění informací po sériové lince
    Serial.println("::Dostupne GPS udaje::");
    Serial.print("Zemepisna sirka: ");
    // nejprve zkontrolujeme, jestli máme platné údaje
    // (zSirka == TinyGPS::GPS_INVALID_F_ANGLE),
    // pokud nejsou validní (platné), vytiskneme nulu,
    // v opačném případě vytiskneme obsah proměnné s přesností 6 desetinných míst,
    // podobným způsobem se pracuje i s ostatními údaji
    Serial.print(zSirka == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : zSirka, 6);
    Serial.print(" delka: ");
    Serial.print(zDelka == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : zDelka, 6);
    Serial.print(" Pocet satelitu: ");
    Serial.println(gps.satellites() == TinyGPS::GPS_INVALID_SATELLITES ? 0 : gps.satellites());
    Serial.print("Presnost: ");
    Serial.print(gps.hdop() == TinyGPS::GPS_INVALID_HDOP ? 0 : gps.hdop());
    Serial.print(" Stari dat: ");
    Serial.print(stariDat == TinyGPS::GPS_INVALID_AGE ? 0 : stariDat);
    Serial.print(" Nadmorska vyska: ");
    Serial.print(gps.f_altitude() == TinyGPS::GPS_INVALID_F_ALTITUDE ? 0 : gps.f_altitude());
    Serial.print(" Rychlost v km/h: ");
    Serial.println(gps.f_speed_kmph() == TinyGPS::GPS_INVALID_F_SPEED ? 0 : gps.f_speed_kmph());
    // načtení data a času z GPS modulu do proměnných
    gps.crack_datetime(&rok, &mesic, &den, &hodina, &minuta, &sekunda, &setinaSekundy, &stariDat);
    // kontrola platnosti dat
    if (stariDat == TinyGPS::GPS_INVALID_AGE) {
      Serial.println("Nelze nacist datum a cas.");
    } else {
      // vytvoření proměnné pro vytištění data a času
      char datumCas[32];
      Serial.print("Datum a cas: ");
      // poskládání celé zprávy do proměnné datumCas a poté její vytištění,
      // %02d znamená desetinné číslo uvedené za uvozovkami s přesností na 2 číslice
      sprintf(datumCas, "%02d/%02d/%02d %02d:%02d:%02d", mesic, den, rok, hodina, minuta, sekunda);
      Serial.println(datumCas);
    }
  }
  // načtení a vytištění informací o komunikaci s GPS modulem
  gps.stats(&znaky, &slova, &chyby);
  Serial.print("Detekovane znaky: ");
  Serial.print(znaky);
  Serial.print(", slova: ");
  Serial.print(slova);
  Serial.print(", chyby pri kontrole dat: ");
  Serial.println(chyby);
  // kontrola chyb při komunikaci skrze detekci přijatých znaků
  if (znaky == 0) {
    Serial.println("Chyba pri prijmu dat z GPS, zkontrolujte zapojeni!");
  }
  Serial.println();
}