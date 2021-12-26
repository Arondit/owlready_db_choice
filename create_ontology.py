from owlready2 import (
    onto_path, 
    get_ontology, 
    Thing, 
    ObjectProperty, 
    DataProperty,
    FunctionalProperty, 
    Imp,
)
from os import getcwd, remove

from owlready2.reasoning import sync_reasoner_pellet


current_directory = getcwd()

onto_path.append(current_directory)
ontology = get_ontology(f'{current_directory}/db_choice.owl')
ontology.load()


# Классы онтологии

class Characteristic(Thing):
    """Свойство"""
    namespace = ontology


class Requirement(Thing):
    """Требование"""
    namespace = ontology


class DBMS(Thing):
    """Система управления базами данных"""
    namespace = ontology


class DBMSType(Thing):
    """Тип системы управления базами данных"""
    namespace = ontology


class UseCase(Thing):
    """Сценарий использования СУБД"""
    namespace = ontology


# Отношения онтологии

class implements(ObjectProperty):
    """СУБД реализует свойство"""
    namespace = ontology
    domain = [DBMS]
    range = [Characteristic]


class ensures_feasibility(ObjectProperty):
    """Свойство обеспечивает выполнимость требования"""
    namespace = ontology
    domain = [Characteristic]
    range = [Requirement]


class satisfies(ObjectProperty):
    """СУБД удовлетворяет требования"""
    namespace = ontology
    domain = [DBMS]
    range = [Requirement]


class defines(ObjectProperty):
    """Сценарий использования определяет требование"""
    namespace = ontology
    domain = [UseCase]
    range = [Requirement]


class is_suitable_for(ObjectProperty):
    """СУБД подходит под сценарий использования"""
    namespace = ontology
    domain = [DBMS]
    range = [UseCase]


class refers_to(ObjectProperty):
    """СУБД относится к типу СУБД"""
    namespace = ontology
    domain = [DBMS]
    range = [DBMSType]


class needs(ObjectProperty):
    """Сценарий использования нуждается в типе СУБД"""
    namespace = ontology
    domain = [UseCase]
    range = [DBMSType]


# Свойста, связанные с классами онтологии

class popularity(DataProperty, FunctionalProperty):
    """Коэффициент популярности СУБД"""
    namespace = ontology
    domain = [DBMS]
    range = [int]


# Создание правил

Imp(name='does_dbms_satisfy_requirement', namespace=ontology).set_as_rule(
    (
        'DBMS(?d), Characteristic(?c), Requirement(?r),'
        ' ensures_feasibility(?c, ?r), implements(?d, ?c)'
        ' -> satisfies(?d, ?r)'
    ),
)


# Создание СУБД онтологии

postgresql = DBMS('PostgresQL')
postgresql.comment = 'Одна из самых популярных и проверенных временем Open Source реляционная база данных PostgreSQL'
postgresql.popularity = 608

oracle = DBMS('Oracle')
oracle.comment = 'Самая популярная реляционная и мульти-модельная база данных. Распространяется на платной основе.'
oracle.popularity = 1281

sqlite_dbms = DBMS('SQLite')
sqlite_dbms.comment = 'Самая простая в настройке реляционная база данных SQLite. Для работы не требуется даже сервер.'
sqlite_dbms.popularity = 128

redis = DBMS('Redis')
redis.comment = (
    'Популярная платформа с хранением данных в памяти. '
    'Используется для хранения кэша, обмена сообщениями. ' 
    'Может быть расположена как на своем сервере, так и на облачном.'
)
redis.popularity = 173

mongo = DBMS('MongoDB')
mongo.comment = (
    'Самая популярная документо-ориентированная база данных. '
    'Может быть расположена как на своем сервере, так и на облачном.'
)
mongo.popularity = 484

cassandra = DBMS('Cassandra')
cassandra.comment = 'Широко-столбцовое хранилище, основанное на идеях BigTable и DynamoDB'
cassandra.popularity = 119

hive = DBMS('Hive')
hive.comment = 'Распределенное хранилище данных на основе Hadoop'
hive.popularity = 81

neo4j = DBMS('Neo4j')
neo4j.comment = 'Самая популярная графовая база данных'
neo4j.popularity = 58

clickhouse = DBMS('ClickHouse')
clickhouse.comment = 'Столбцово-ориентированная СУБД, созданная Яндексом. Хорошо подходит для аналитики.'
clickhouse.popularity = 12

nebula = DBMS('NebulaGraph')
nebula.comment = 'Распределенная масштабированная графовая база данных с высокой производительностью.'
nebula.popularity = 1

elastic = DBMS('ElasticSearch')
elastic.comment = 'Самая популярная платформа для работы с полнотекстовым поиском'
elastic.popularity = 157

memcached = DBMS('Memcached')
memcached.comment = 'Хранилище ключ-значение для кэша'
memcached.popularity = 26


# Создание свойств СУБД онтологии

provides_acid = Characteristic('provide_acid')
provides_acid.comment = 'Поддерживает требования к транзакционной системе'

immediate_consistency = Characteristic('immediate_consistency')
immediate_consistency.comment = 'Данные полностью согласованы в любой момент времени'

provides_map_reduce = Characteristic('provides_map_reduce')
provides_map_reduce.comment = 'Поддерживает популярную парадигму параллельной обработки огромных данных (петабайты)'

concurrency = Characteristic('concurrency')
concurrency.comment = 'Поддерживает конкурентный доступ (параллельность/асинхронность)'

open_source = Characteristic('open_source')
open_source.comment = 'Свободная лицензия'

partial_tolerance = Characteristic('partial_tolerance')
partial_tolerance.comment = 'Поддерживает разделение в смысле Partial Tolerance из т.н теоремы CAP'

in_memory = Characteristic('in_memory')
in_memory.comment = 'Возможность хранить данные в памяти, не сохраняя их на диск'

fast_read = Characteristic('fast_read')
fast_read.comment = 'Очень быстрое чтение огромных данных: свойство СУБД, которые нужны в основном для аналитики'

fast_write = Characteristic('fast_write')
fast_write.comment = 'Быстрая запись данных в базу (в память или на диск)'

guarantees_safety = Characteristic('guarantees_safety')
guarantees_safety.comment = 'Гарантирует, что она никогда не потеряет полученные данные'

access_differentiation = Characteristic('access_differentiation')
access_differentiation.comment = (
    'Поддерживает ограничение доступов, ' 
    'например, через мульти-тенантность или через концепцию пользователей'
)

full_text_search = Characteristic('full_text_search')
full_text_search.comment = 'Поддерживает полнотекстовый поиск'

easy_settings = Characteristic('easy_settings')
easy_settings.comment = 'Не требует опыта и специальных знаний для настройки'

works_as_service = Characteristic('works_as_service')
works_as_service.comment = 'База данных как сервис. СУБД поддерживает работу в облачном сервисе.'


# Создание требований к СУБД онтологии

data_must_always_be_correct = Requirement('data_must_always_be_correct')
data_must_always_be_correct.comment = (
    'Данные всегда должны быть корректны: '
    'даже временная несогласованность данных критична'
)

cant_lose_data = Requirement('cant_lose_data')
cant_lose_data.comment = (
    'Нельзя терять данные: потеря данных может быть критична. Нужно уточнять, '
    'так как бывают сценарии использования базы данных, в которых такого требования нет. Например, кэш.'
)

high_access_differentiation = Requirement('high_access_differentiation')
high_access_differentiation.comment = (
    'Повышенные требования к разграничению доступов: '
    'в некоторых системах доставка данных не тому пользователю критична,'
    'и им нужно разделение доступов, чтобы такая ситуация стала невозможной даже теоретически.'
)

analyze_big_data = Requirement('analyze_big_data')
analyze_big_data.comment = 'Нужно анализировать огромные данные: требование, которые предъявляют аналитические системы'

analyze_huge_data = Requirement('analyze_huge_data')
analyze_huge_data.comment = (
    'Нужно анализировать настолько огромные данные, '
    'что они не помещаются на один сервер: да, такое вполне возможно'
)

fast_response = Requirement('fast_response')
fast_response.comment = 'Должна отвечать как можно быстрее: скорость отклика является критичной'

store_big_data = Requirement('store_big_data')
store_big_data.comment = 'Нужно хранить огромные данные: речь о данных, которые не помещаются на одном сервере'

geo_independency = Requirement('geo_independency')
geo_independency.comment = (
    'Должна отвечать одинаково быстро независимо от географии: '
    'если пользователи распределены по всему миру, то расположение сервера очень важно. '
    'СУБД должна быть в состоянии безболезненно разбиваться на несколько изолированных серверов'
)

must_be_free = Requirement('must_be_free')
must_be_free.comment = 'Должна быть бесплатной: не всегда возможно использовать платные решения'

working_with_texts = Requirement('working_with_texts')
working_with_texts.comment = 'Должна быстро работать с текстом: например, в поисковых системах или при анализе текста'

works_from_box = Requirement('works_from_box')
works_from_box.comment = (
    'Должна нормально работать «из коробки»: '
    'важно, когда нет возможности нанять опытного специалиста по базам данных'
)

no_needs_server = Requirement('no_needs_server')
no_needs_server.comment = 'СУБД может работать даже без сервера'


# Присваивание свойств СУБД

for characteristic in [
    provides_acid, 
    concurrency, 
    open_source, 
    immediate_consistency, 
    guarantees_safety, 
    full_text_search, 
    access_differentiation, 
    works_as_service,
]:
    postgresql.implements.append(characteristic)

for characteristic in [
    provides_acid, 
    concurrency, 
    in_memory, 
    immediate_consistency, 
    guarantees_safety, 
    full_text_search, 
    access_differentiation,
]:
    oracle.implements.append(characteristic)

for characteristic in [
    concurrency, 
    open_source, 
    partial_tolerance, 
    in_memory, 
    fast_read, 
    fast_write, 
    works_as_service,
]:
    redis.implements.append(characteristic)

for characteristic in [
    provides_map_reduce, 
    provides_acid, 
    concurrency, 
    open_source, 
    partial_tolerance, 
    in_memory, 
    access_differentiation, 
    works_as_service,
]:
    mongo.implements.append(characteristic)

for characteristic in [
    provides_map_reduce, 
    concurrency, 
    open_source, 
    partial_tolerance, 
    fast_read, 
    fast_write, 
    works_as_service,
]:
    cassandra.implements.append(characteristic)

for characteristic in [
    provides_acid, 
    concurrency, 
    open_source, 
    access_differentiation, 
    works_as_service,
]:
    neo4j.implements.append(characteristic)

for characteristic in [
    concurrency, 
    open_source, 
    partial_tolerance, 
    full_text_search,
]:
    elastic.implements.append(characteristic)

for characteristic in [
    provides_map_reduce, 
    concurrency, 
    open_source, 
    partial_tolerance, 
    access_differentiation,
]:
    hive.implements.append(characteristic)

for characteristic in [
    concurrency, 
    open_source, 
    immediate_consistency, 
    in_memory, 
    fast_read, 
    access_differentiation,
]:
    clickhouse.implements.append(characteristic)

for characteristic in [
    concurrency, 
    open_source, 
    in_memory, 
    fast_read, 
    fast_write, 
    access_differentiation, 
    easy_settings,
]:
    memcached.implements.append(characteristic)

for characteristic in [
    provides_acid, 
    concurrency, 
    open_source, 
    partial_tolerance, 
    immediate_consistency, 
    in_memory, 
    fast_read, 
    access_differentiation,
]:
    nebula.implements.append(characteristic)

for characteristic in [
    provides_acid, 
    concurrency, 
    open_source, 
    immediate_consistency, 
    in_memory, 
    guarantees_safety, 
    easy_settings,
]:
    sqlite_dbms.implements.append(characteristic)

sqlite_dbms.satisfies.append(no_needs_server)


# Присваивание свойствам требований, выполнимость которых они обеспечивают

provides_acid.ensures_feasibility.append(data_must_always_be_correct)
immediate_consistency.ensures_feasibility.append(data_must_always_be_correct)
guarantees_safety.ensures_feasibility.append(cant_lose_data)
open_source.ensures_feasibility.append(must_be_free)
easy_settings.ensures_feasibility.append(works_from_box)
works_as_service.ensures_feasibility.append(no_needs_server)
concurrency.ensures_feasibility.append(fast_response)
in_memory.ensures_feasibility.append(fast_response)
fast_write.ensures_feasibility.append(fast_response)

fast_read.ensures_feasibility.append(fast_response)
fast_read.ensures_feasibility.append(analyze_big_data)
fast_read.ensures_feasibility.append(analyze_huge_data)

provides_map_reduce.ensures_feasibility.append(analyze_huge_data)
partial_tolerance.ensures_feasibility.append(analyze_huge_data)
partial_tolerance.ensures_feasibility.append(geo_independency)
partial_tolerance.ensures_feasibility.append(store_big_data)
partial_tolerance.ensures_feasibility.append(high_access_differentiation)
access_differentiation.ensures_feasibility.append(high_access_differentiation)
