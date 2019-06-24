from unittest import TestCase

from spp.functions import caracteresInvalidos


class TestesCaracteresInvalidos(TestCase):
    """Testes para caracteresInvalidos."""

    def test1(self):
        """Teste Boolean True ___0"""
        self.assertTrue(caracteresInvalidos('___0'))

    def test2(self):
        """Teste Boolean True ___47"""
        self.assertTrue(caracteresInvalidos('___47'))

    def test3(self):
        """Teste Boolean True ___48"""
        self.assertTrue(caracteresInvalidos('___48'))

    def test4(self):
        """Teste Boolean False ___-1"""
        self.assertFalse(caracteresInvalidos('___-1'))

    def test5(self):
        """Teste Boolean no string"""
        self.assertFalse(caracteresInvalidos(''))
