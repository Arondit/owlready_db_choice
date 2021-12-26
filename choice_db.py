from typing import Dict, Iterable, List, Union
from owlready2 import onto_path, get_ontology
from os import getcwd


CURRENT_DIRECTORY = getcwd()
onto_path.append(CURRENT_DIRECTORY)


DBMSDictType = Dict[str, Union[str, List[str], int]]


def get_dict_for_dbms(dbms) -> DBMSDictType:
    characteristics_descriptions = [
        characteristic.comment[0] if characteristic.comment else '' 
        for characteristic in dbms.implements
    ]
    return {
            'name': str(dbms).split('.')[-1], 
            'characteristics': characteristics_descriptions,
            'popularity': dbms.popularity or 0,
            'description': dbms.comment[0] if dbms.comment else '',
    }


def get_dbms(requirements: Iterable[str], dbms_count: int = 3) -> List[DBMSDictType]:
    """
    На основе списка требований получает упорядоченный список баз данных
    
    :param requirements: список строк, которым должны соответсвовать требования из онтологии
    :param dbms_count: количество СУБД, которые нужно вернуть. По умолчанию 3
    :return: список словарей, где хранится информация о базе данных
    """
    ontology = get_ontology(f'{CURRENT_DIRECTORY}/db_choice.owl')
    ontology.load()

    onto_requirements = [ontology.search_one(iri=f'*{requirement}') for requirement in requirements]

    dbms_class = ontology.search_one(iri='*DBMS')
    
    all_dbms = ontology.search(is_a=dbms_class)[1:]
    sorted_dbms = sorted(
        all_dbms, 
        reverse=True, 
        key=lambda dbms: len(set(dbms.satisfies) & set(onto_requirements)),
    )
    chosen_dbms = sorted_dbms[:dbms_count]

    return [get_dict_for_dbms(dbms) for dbms in chosen_dbms]
