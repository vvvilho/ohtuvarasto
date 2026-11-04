"""Automaattiset testit Varasto-luokalle."""
import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    """Testiluokka Varasto-luokalle."""
    def setUp(self):
        self.varasto = Varasto(10)

    def test_konstruktori_luo_tyhjan_varaston(self):
        """Luodaan varasto, jonka saldo on 0."""
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        """Testataan uuden varaston tilavuus."""
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_lisays_lisaa_saldoa(self):
        """Testataan lisäys."""
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        """Testataan että lisäys pienentää vapaata tilaa."""
        self.varasto.lisaa_varastoon(8)

        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        """Testataan että ottaminen palauttaa oikean määrän."""
        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        """Testataan että ottaminen lisää tilaa varastossa."""
        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)

    def test_lisaa_liikaa_tavaraa(self):
        """Testataan että lisättäessä liikaa tavaraa, varastoon mahtuu vain maksimimäärä."""
        self.varasto.lisaa_varastoon(12)

        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 0)

    def test_lisaa_negatiivinen_maara(self):
        """Testataan että lisättäessä negatiivinen määrä, varastoon ei lisätä mitään."""
        self.varasto.lisaa_varastoon(-2)

        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 10)

    def test_ota_liikaa_tavaraa(self):
        """Testataan että otettaessa liikaa tavaraa, varastosta otetaan vain se mitä on."""
        self.varasto.lisaa_varastoon(6)

        saatu = self.varasto.ota_varastosta(8)
        self.assertAlmostEqual(saatu, 6)

    def test_ota_negatiivinen_maara(self):
        """Testataan että otettaessa negatiivinen määrä, varastosta ei oteta mitään."""
        self.varasto.lisaa_varastoon(6)

        saatu = self.varasto.ota_varastosta(-2)
        self.assertAlmostEqual(saatu, 0)

    def test_negatiivinen_tilavuus(self):
        """Testataan että tilavuus ei mene negatiiviseksi."""
        varasto = Varasto(-2)
        self.assertAlmostEqual(varasto.tilavuus, 0)

    def test_negatiivinen_alkusaldo(self):
        """Testataan että alkusaldo ei mene negatiiviseksi."""
        varasto = Varasto(10, -2)
        self.assertAlmostEqual(varasto.saldo, 0)

    def test_string_esitys(self):
        """Testataan string-esitys."""
        self.varasto.lisaa_varastoon(6)

        self.assertAlmostEqual((str(self.varasto)), "saldo = 6, vielä tilaa 4")
 
