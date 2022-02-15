library = """
->(left:, right:) = {arg: left, value: right};

ArgMin(a) = SqlExpr(
  "ARRAY_AGG({arg}) WITHIN GROUP (order by {value})[1]",
  {arg: a.arg, value: a.value});

ArgMax(a) = SqlExpr(
  "ARRAY_AGG({arg}) WITHIN GROUP (order by {value} desc)[1]",
  {arg: a.arg, value: a.value});

ArgMaxK(a, l) = SqlExpr(
  "ARRAY_SLICE(ARRAY_AGG({arg}) WITHIN GROUP (order by {value} desc), 1, {lim})",
  {arg: a.arg, value: a.value, lim: l});

ArgMinK(a, l) = SqlExpr(
  "ARRAY_SLICE(ARRAY_AGG({arg}) WITHIN GROUP (order by {value}), 1, {lim})",
  {arg: a.arg, value: a.value, lim: l});

Array(a) = SqlExpr(
  "ARRAY_AGG({value}) WITHIN GROUP (order by {arg})",
  {arg: a.arg, value: a.value});

RMatch(s, p) = SqlExpr(
  "REGEXP_LIKE({s}, {p})",
  {s: s, p: p});
  
RExtract(s, p, g) = SqlExpr(
  "REGEXP_SUBSTR({s}, {p}, {g})",
  {s: s, p: p, g: g});
  
ArrayJoin(array, delimiter) = SqlExpr(
  “ARRAY_TO_STRING({array}, {delimiter})“,
  {array:, delimiter:});
"""