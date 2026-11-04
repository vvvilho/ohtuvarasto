"""Varastonhallinta pitää kirjaa varaston tilavuudesta ja saldosta."""

class Varasto:
    """Varasto-luokka, joka pitää kirjaa varaston tilavuudesta ja saldosta."""

    def __init__(self, tilavuus, alku_saldo = 0):
        """Alustetaan varasto."""

        if tilavuus > 0.0:
            self.tilavuus = tilavuus
        else:
            # virheellinen, nollataan
            self.tilavuus = 0.0

        if alku_saldo < 0.0:
            # virheellinen, nollataan
            self.saldo = 0.0
        elif alku_saldo <= tilavuus:
            # mahtuu
            self.saldo = alku_saldo
        else:
            # täyteen ja ylimäärä hukkaan!
            self.saldo = tilavuus


    def paljonko_mahtuu(self):
        """Palauttaa paljonko varastoon vielä mahtuu."""

        return self.tilavuus - self.saldo


    def lisaa_varastoon(self, maara):
        """Lisää varastoon, jos mahtuu."""        

        if maara < 0:
            return
        if maara <= self.paljonko_mahtuu():
            self.saldo = self.saldo + maara
        else:
            self.saldo = self.tilavuus



    def ota_varastosta(self, maara):
        """Ottaa varastosta, jos siellä on tarpeeksi."""

        if maara < 0:
            return 0.0
        if maara > self.saldo:
            kaikki_mita_voidaan = self.saldo
            self.saldo = 0.0

            return kaikki_mita_voidaan

        self.saldo = self.saldo - maara

        return maara

    def __str__(self):
        return f"saldo = {self.saldo}, vielä tilaa {self.paljonko_mahtuu()}"
