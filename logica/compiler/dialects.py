#!/usr/bin/python
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""SQL dialects."""

import copy

if '.' not in __package__:
  from compiler.dialect_libraries import bq_library
  from compiler.dialect_libraries import psql_library
  from compiler.dialect_libraries import sqlite_library
  from compiler.dialect_libraries import trino_library
  from compiler.dialect_libraries import presto_library
  from compiler.dialect_libraries import snowflake_library
  from compiler.dialect_libraries import dremio_library
else:
  from ..compiler.dialect_libraries import bq_library
  from ..compiler.dialect_libraries import psql_library
  from ..compiler.dialect_libraries import sqlite_library
  from ..compiler.dialect_libraries import trino_library
  from ..compiler.dialect_libraries import presto_library
  from ..compiler.dialect_libraries import snowflake_library
  from ..compiler.dialect_libraries import dremio_library


def Get(engine):
  return DIALECTS[engine]()


class Dialect(object):
  pass


class BigQueryDialect(Dialect):
  """BigQuery SQL dialect."""

  def Name(self):
    return 'BigQuery'

  def BuiltInFunctions(self):
    return {}

  def InfixOperators(self):
    return {
        '++': 'CONCAT(%s, %s)',
    }

  def Subscript(self, record, subscript):
    return '%s.%s' % (record, subscript)

  def LibraryProgram(self):
    return bq_library.library

  def UnnestPhrase(self):
    return 'UNNEST({0}) as {1}'

  def ArrayPhrase(self):
    return 'ARRAY[%s]'

  def GroupBySpecBy(self):
    return 'name'

  def DecorateCombineRule(self, rule, var):
    return rule

class SqLiteDialect(Dialect):
  """SqLite SQL dialect."""

  def Name(self):
    return 'SqLite'

  def BuiltInFunctions(self):
    return {
        'Set': 'DistinctListAgg({0})',
        'Element': "JSON_EXTRACT({0}, '$[' || {1} || ']')",
        'Range': ('(select json_group_array(n) from (with recursive t as'
                  '(select 0 as n union all '
                  'select n + 1 as n from t where n + 1 < {0}) '
                  'select n from t) where n < {0})'),
        'ValueOfUnnested': '{0}.value',
        'List': 'JSON_GROUP_ARRAY({0})',
        'Size': 'JSON_ARRAY_LENGTH({0})',
        'Join': 'JOIN_STRINGS({0}, {1})',
        'Count': 'COUNT(DISTINCT {0})',
        'StringAgg': 'GROUP_CONCAT(%s)',
        'Sort': 'SortList({0})',
        'MagicalEntangle': 'MagicalEntangle({0}, {1})',
        'Format': 'Printf(%s)',
        'Least': 'MIN(%s)',
        'Greatest': 'MAX(%s)',
        'ToString': 'CAST(%s AS TEXT)',
        'JsonExtract': 'JSON_EXTRACT({0}, {1})',
        'JsonExtractScalar': 'CAST(JSON_EXTRACT({0}, {1}) AS TEXT)',
    }

  def DecorateCombineRule(self, rule, var):
    """Resolving ambiguity of aggregation scope."""
    # Entangling result of aggregation with a variable that comes from a list
    # unnested inside a combine expression, to make it clear that aggregation
    # must be done in the combine.
    rule = copy.deepcopy(rule)

    rule['head']['record']['field_value'][0]['value'][
      'aggregation']['expression']['call'][
      'record']['field_value'][0]['value'] = (
      {
        'expression': {
          'call': {
            'predicate_name': 'MagicalEntangle',
            'record': {
              'field_value': [
                {
                  'field': 0,
                  'value': rule['head']['record']['field_value'][0]['value'][
                    'aggregation']['expression']['call'][
                      'record']['field_value'][0]['value']
                },
                {
                  'field': 1,
                  'value': {
                    'expression': {
                      'variable': {
                        'var_name': var
                      }
                    }
                  }
                }
              ]
            }
          }
        }
      }
    )

    if 'body' not in rule:
      rule['body'] = {'conjunction': {'conjunct': []}}
    rule['body']['conjunction']['conjunct'].append(
      {
        "inclusion": {
          "list": {
            "literal": {
              "the_list": {
                "element": [
                  {
                    "literal": {
                      "the_number": {
                        "number": "0"
                      }
                    }
                  }
                ]
              }
            }
          },
          "element": {
            "variable": {
              "var_name": var
            }
          }
        }
      }
    )
    return rule


  def InfixOperators(self):
    return {
        '++': '(%s) || (%s)',
        '%' : '(%s) %% (%s)',
        'in': 'IN_LIST(%s, %s)'
    }

  def Subscript(self, record, subscript):
    return '%s.%s' % (record, subscript)

  def LibraryProgram(self):
    return sqlite_library.library

  def UnnestPhrase(self):
    return 'JSON_EACH({0}) as {1}'

  def ArrayPhrase(self):
    return 'JSON_ARRAY(%s)'

  def GroupBySpecBy(self):
    return 'expr'

class PostgreSQL(Dialect):
  """PostgreSQL SQL dialect."""

  def Name(self):
    return 'PostgreSQL'

  def BuiltInFunctions(self):
    return {
        'Range': '(SELECT ARRAY_AGG(x) FROM GENERATE_SERIES(0, {0} - 1) as x)',
        'ToString': 'CAST(%s AS TEXT)',
        'Element': '({0})[{1} + 1]',
        'Size': 'ARRAY_LENGTH(%s, 1)',
        'Count': 'COUNT(DISTINCT {0})'
      }

  def InfixOperators(self):
    return {
        '++': 'CONCAT(%s, %s)',
    }

  def Subscript(self, record, subscript):
    return '(%s).%s' % (record, subscript)

  def LibraryProgram(self):
    return psql_library.library

  def UnnestPhrase(self):
    return 'UNNEST({0}) as {1}'

  def ArrayPhrase(self):
    return 'ARRAY[%s]'

  def GroupBySpecBy(self):
    return 'name'

  def DecorateCombineRule(self, rule, var):
    return rule


class Trino(Dialect):
  """Trino analytic engine dialect."""

  def Name(self):
    return 'Trino'

  def BuiltInFunctions(self):
    return {
        'Range': 'SEQUENCE(0, %s - 1)',
        'ToString': 'CAST(%s AS VARCHAR)',
        'ToInt64': 'CAST(%s AS BIGINT)',
        'ToFloat64': 'CAST(%s AS DOUBLE)',
        'AnyValue': 'ARBITRARY(%s)',
        'ArrayConcat': '{0} || {1}',
        'Count': 'APPROX_DISTINCT(%s)'
    }

  def InfixOperators(self):
    return {
        '++': 'CONCAT(%s, %s)',
    }

  def Subscript(self, record, subscript):
    return '%s.%s' % (record, subscript)

  def LibraryProgram(self):
    return trino_library.library

  def UnnestPhrase(self):
    return 'UNNEST({0}) as pushkin({1})'

  def ArrayPhrase(self):
    return 'ARRAY[%s]'

  def GroupBySpecBy(self):
    return 'index'

  def DecorateCombineRule(self, rule, var):
    return rule


class Presto(Dialect):

  def Name(self):
    return 'Presto'

  def BuiltInFunctions(self):
    return {
        'Range': 'SEQUENCE(0, %s - 1)',
        'ToString': 'CAST(%s AS VARCHAR)',
        'ToInt64': 'CAST(%s AS BIGINT)',
        'ToFloat64': 'CAST(%s AS DOUBLE)',
        'AnyValue': 'ARBITRARY(%s)'
    }

  def InfixOperators(self):
    return {
        '++': 'CONCAT(%s, %s)',
    }

  def Subscript(self, record, subscript):
    return '%s.%s' % (record, subscript)

  def LibraryProgram(self):
    return presto_library.library

  def UnnestPhrase(self):
    return 'UNNEST({0}) as pushkin({1})'

  def ArrayPhrase(self):
    return 'ARRAY[%s]'

  def GroupBySpecBy(self):
    return 'index'

  def DecorateCombineRule(self, rule, var):
    return rule


class Snowflake(Dialect):
    """Snowflake dialect"""
    def Name(self):
        return 'Snowflake'

    def BuiltInFunctions(self):
        return {
            'Range': '(SELECT array_agg(seq4()) FROM TABLE(generator(rowcount => %s)))',
            'ToString': 'CAST(%s AS VARCHAR)',
            'ToInt64': 'CAST(%s AS BIGINT)',
            'ToFloat64': 'CAST(%s AS DOUBLE)',
            'AnyValue': 'ANY_VALUE(%s)',
            'ArrayConcat': 'ARRAY_CAT({0}, {1})',
            'JsonExtractScalar': '{0}:"{1}"',
            'Length': 'ARRAY_SIZE(%s)',
            'DateDiff': 'DATEDIFF({0}, {1}, {2})'
        }

    def InfixOperators(self):
        return {
            '++': 'CONCAT(%s, %s)',
        }

    def Subscript(self, record, subscript):
        # I don't know how reliable this is; probably not at all
        splitter = ':' if '.' in record else '.'
        return f"{record}{splitter}{subscript}"

    def LibraryProgram(self):
        return snowflake_library.library

    def UnnestPhrase(self):
        return 'LATERAL FLATTEN(INPUT => {0}) AS pushkin(seq,key,path,index,{1})'

    def ArrayPhrase(self):
        return 'ARRAY_CONSTRUCT(%s)'

    def GroupBySpecBy(self):
        return 'index'

    def DecorateCombineRule(self, rule, var):
        return rule


class Dremio(Dialect):
    """Dremio dialect"""

    def Name(self):
        return 'Dremio'

    def BuiltInFunctions(self):
        return {
            #'Range': '(SELECT array_agg(seq4()) FROM TABLE(generator(rowcount => %s)))',
            'ToString': 'CAST(%s AS VARCHAR)',
            'ToInt64': 'CAST(%s AS BIGINT)',
            'ToFloat64': 'CAST(%s AS DOUBLE)',
            'AnyValue': 'ANY_VALUE(%s)',
            #'ArrayConcat': 'ARRAY_CAT({0}, {1})',
            #'JsonExtractScalar': 'CONVERT_FROM({0}.{1}, \'JSON\')'
            'JsonExtractScalar': '{0}.{1}',
            'IsNull': 'ISNULL(%s)'
        }

    def InfixOperators(self):
        return {
            '++': 'CONCAT(%s, %s)',
        }

    def Subscript(self, record, subscript):
        return '%s.%s' % (record, subscript)

    def LibraryProgram(self):
        return dremio_library.library

    def UnnestPhrase(self):
        return 'FLATTEN({0}) AS pushkin({1})'

    # def ArrayPhrase(self):
    #     return 'ARRAY_CONSTRUCT(%s)'

    def GroupBySpecBy(self):
        return 'index'

    def DecorateCombineRule(self, rule, var):
        return rule


DIALECTS = {
    'bigquery': BigQueryDialect,
    'sqlite': SqLiteDialect,
    'psql': PostgreSQL,
    'presto': Presto,
    'trino': Trino,
    'snowflake': Snowflake,
    'dremio': Dremio
}

