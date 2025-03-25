import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_konstruktori_asettaa_saldon_oikein(self):
        self.assertEqual(self.maksukortti.saldo, 1000)
    
    def test_rahan_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(500)
        self.assertEqual(self.maksukortti.saldo, 1500)
    
    def test_rahan_ottaminen_vahentaa_saldoa_oikein_jos_rahaa_on_tarpeeksi(self):
        tulos = self.maksukortti.ota_rahaa(500)
        self.assertEqual(self.maksukortti.saldo, 500)
        self.assertTrue(tulos)
    
    def test_saldo_ei_muutu_jos_rahaa_ei_ole_tarpeeksi(self):
        tulos = self.maksukortti.ota_rahaa(1500)
        self.assertEqual(self.maksukortti.saldo, 1000)
        self.assertFalse(tulos)
    
    def test_ota_rahaa_palauttaa_true_jos_rahat_riittivat(self):
        tulos = self.maksukortti.ota_rahaa(500)
        self.assertTrue(tulos)
    
    def test_ota_rahaa_palauttaa_false_jos_rahat_eivat_riittaneet(self):
        tulos = self.maksukortti.ota_rahaa(1500)
        self.assertFalse(tulos)