"""
Take snowflake dialect as a reference and implement the same set of functions for Databricks
Once done, test every function and their combinations thoroughly
"""

library = """
->(left:, right:) = {arg: left, value: right};

ArgMin(a) = SqlExpr(
  "(ARRAY_AGG({arg} order by {value}))[1]",
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

RMatch(s, p) = SqlExpr(
  "REGEXP_LIKE({s}, {p})",
  {s: s, p: p});

RExtract(s, p, g) = SqlExpr(
  "REGEXP_SUBSTR({s}, {p}, 1, 1, 'c', {g})",
  {s: s, p: p, g: g});
  
Array(a) = SqlExpr(
  "ARRAY_AGG({value} order by {arg})",
  {arg: a.arg, value: a.value});
  
  
  
  
"""