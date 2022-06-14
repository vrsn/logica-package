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

library = """
->(left:, right:) = {arg: left, value: right};

ArgMin(a) = SqlExpr("(ARRAY_AGG({arg} order by {value}))[1]",
                    {arg: a.arg, value: a.value});

ArgMax(a) = SqlExpr(
  "(ARRAY_AGG({arg} order by {value} desc))[1]",
  {arg: a.arg, value: a.value});

ArgMaxK(a, l) = SqlExpr(
  "SLICE(ARRAY_AGG({arg} order by {value} desc), 1, {lim})",
  {arg: a.arg, value: a.value, lim: l});

ArgMinK(a, l) = SqlExpr(
  "SLICE(ARRAY_AGG({arg} order by {value}), 1, {lim})",
  {arg: a.arg, value: a.value, lim: l});

Array(a) = SqlExpr(
  "ARRAY_AGG({value} order by {arg})",
  {arg: a.arg, value: a.value});

ArraySize(array) = SqlExpr(
  "CARDINALITY({array})", {array:});

ArrayJoin(array, delimiter) = SqlExpr(
  "ARRAY_JOIN({array}, {delimiter})", {array:, delimiter:});

ElementAt(array, index) = SqlExpr(
  "ELEMENT_AT({array}, {index})", {array:, index:});

RMatch(s, p) = SqlExpr(
  "REGEXP_LIKE({s}, {p})",
  {s: s, p: p});

RExtract(s, p, g) = SqlExpr(
  "REGEXP_EXTRACT({s}, {p}, {g})",
  {s: s, p: p, g: g});

JsonArrayContains(json_value, value) = SqlExpr(
  "JSON_ARRAY_CONTAINS({json_value}, {value})", {json_value:, value:});
  
ToJsonArray(col) = SqlExpr(
  "CAST({col} AS ARRAY<JSON>)", {col:});

ToJson(col) = SqlExpr(
  "CAST({col} AS JSON)", {col:});

JsonParse(string) = SqlExpr(
  "JSON_PARSE({string})", {string:});

GetField(obj, field) =  SqlExpr(
  "JSON_EXTRACT_SCALAR({obj}, {field})", {obj:, field:});

Now() = SqlExpr(
  "Now()", {});

DaysDiff(start_date:, end_date:) = DateDiff("day", start_date, end_date);

From_Unixtime(string) = SqlExpr(
  "FROM_ISO8601_TIMESTAMP_NANOS({string})", {string:});
"""
