from bread.tests.helper import generic_bread_testcase

from basxconnect.core import models


class PersonTest(generic_bread_testcase(models.Person)):
    pass


class NaturalPersonTest(generic_bread_testcase(models.NaturalPerson)):
    pass


class LegalPersonTest(generic_bread_testcase(models.LegalPerson)):
    pass


class PersonAssociationTest(generic_bread_testcase(models.PersonAssociation)):
    pass