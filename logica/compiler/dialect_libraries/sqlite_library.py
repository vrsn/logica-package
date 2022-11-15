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

Arrow(left, right) = arrow :-
  left == arrow.arg,
  right == arrow.value;

PrintToConsole(message) :- 1 == SqlExpr("PrintToConsole({message})", {message:});

ArgMin(arr) = Element(
    SqlExpr("ArgMin({a}, {v}, 1)", {a:, v:}), 0) :- Arrow(a, v) == arr;

ArgMax(arr) = Element(
    SqlExpr("ArgMax({a}, {v}, 1)", {a:, v:}), 0) :- Arrow(a, v) == arr;

ArgMinK(arr, k) = 
    SqlExpr("ArgMin({a}, {v}, {k})", {a:, v:, k:}) :-
  Arrow(a, v) == arr;

ArgMaxK(arr, k) =
    SqlExpr("ArgMax({a}, {v}, {k})", {a:, v:, k:}) :- Arrow(a, v) == arr;

Array(arr) =
    SqlExpr("ArgMin({v}, {a}, null)", {a:, v:}) :- Arrow(a, v) == arr; 

ArraySize(array) = SqlExpr(
  "json_array_length({array})", 
  {array:});

ReadFile(filename) = SqlExpr("ReadFile({filename})", {filename:});

ReadJson(filename) = ReadFile(filename);

WriteFile(filename, content:) = SqlExpr("WriteFile({filename}, {content})",
                                        {filename:, content:});

Fingerprint(s) = SqlExpr("Fingerprint({s})", {s:}); 

ElementAt(array, index) = SqlExpr(
  "ELEMENT_AT({array}, {index})", {array:, index:});

JsonArrayContains(json_value, value) =
  SqlExpr("CASE WHEN {json_value} = 'null' OR {json_value} IS NULL THEN NULL ELSE CASE WHEN EXISTS (SELECT 1 FROM json_each({json_value}) WHERE json_each.value LIKE {value}) THEN TRUE ELSE FALSE END END", {json_value:, value:});

JsonArrayLength(arr) = SqlExpr(
  "JSON_ARRAY_LENGTH({arr})", {arr:});

ToJsonArray(col) = SqlExpr("{col}", {col:});

ToJson(col) = SqlExpr("{col}", {col:});

JsonParse(col) = SqlExpr(
  "JSON({col})", 
  {col:});

GetField(obj, field) =  (SqlExpr("JSON_EXTRACT({obj}, {field})", {obj:, field:}));
"""
