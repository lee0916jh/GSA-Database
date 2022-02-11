import factory
import datetime

from grdb.database.models import Experiment
from .common import test_db
from . import AuthorFactory

LIST_SIZES = [1, 2, 3]


class ExperimentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Experiment
        sqlalchemy_session = test_db.Session
        sqlalchemy_session_persistence = "commit"

    recipe_id = factory.LazyAttribute(lambda obj: obj.recipe.id)
    environment_conditions_id = factory.Faker('pyint')
    substrate_id = factory.Faker('pyint')
    furnace_id = factory.Faker('pyint')
    primary_sem_file_id = None
    # The user/author that submitted this experiment
    submitted_by = factory.LazyAttribute(lambda obj: AuthorFactory().id)
    # The date the experiment was conducted
    experiment_date = factory.Faker('date_between_dates',
                                    date_start=datetime.date(2020, 1, 1),
                                    date_end=datetime.date(2020, 5, 31),
                                    )
    # The material grown
    material_name = 'Graphene'
    # Status of experiment valdation
    validated = False
    # The authors that conducted the experiment
    # authors = factory.SubFactory(
    #     "test.database.factories.AuthorFactory"
    # )
    properties = factory.RelatedFactoryList(
        "database.factories.PropertiesFactory", "experiment", size=3
    )
    # # MANY-TO-ONE: experiments->recipe
    recipe = factory.SubFactory(
        "database.factories.RecipeFactory", experiments=[]
    )

    # # MANY-TO-ONE: experiments->environment_conditions
    environment_conditions = factory.SubFactory(
        "database.factories.EnvironmentConditionsFactory", experiments=[]
    )

    # # MANY-TO-ONE: experiments->substrate
    substrate = factory.SubFactory(
        "database.factories.SubstrateFactory", experiments=[]
    )

    # # MANY-TO-ONE: experiments->furnace
    furnace = factory.SubFactory(
        "database.factories.FurnaceFactory", experiments=[]
    )

    # # ONE-TO-MANY: experiment -> raman_files
    raman_files = factory.RelatedFactoryList(
        "database.factories.RamanFileFactory", "experiment", size=3
    )

    # The following lines are a source of bug for "maximum recursion depth exceeded while calling a Python object"
    # # # ONE-TO-MANY: experiment -> sem_files
    # sem_files = factory.RelatedFactoryList(
    #     "test.database.factories.SemFileFactory", "experiment", size=3
    # )

    # The following gives "Incompatible collection type: None is not list-like"
    # primary_sem_file = factory.RelatedFactory(
    #     "test.database.factories.SemFileFactory"
    # )
