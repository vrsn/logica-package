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

RMatch(s, p) = SqlExpr(
  "REGEXP_LIKE({s}, {p})",
  {s: s, p: p});
  
RExtract(s, p, g) = SqlExpr(
  "REGEXP_SUBSTR({s}, {p}, {g})",
  {s: s, p: p, g: g});

Array(a) = SqlExpr(
  "ARRAY_AGG({value}) WITHIN GROUP (order by {arg})",
  {arg: a.arg, value: a.value});

ArraySize(array) = SqlExpr(
  "ARRAY_SIZE({array})", {array:});

ArrayContains(array) = SqlExpr(
  "ARRAY_CONTAINS({array})", {array:});

Array_min(array) = SqlExpr(
  "SELECT min(pushkin.value) FROM LATERAL FLATTEN(INPUT => {array}}) pushkin", 
  {array:});

ElementAt(array, index) = SqlExpr(
  "GET({array}, {index})", {array:, index:});

ArrayGet(array, index) = SqlExpr(
  "{array}[{index}]", 
  {array:, index:});
  
ArrayGetAsVarchar(array, index) = SqlExpr(
  "{array}[{index}]", 
  {array:, index:});

ArrayJoin(array, delimiter) = SqlExpr(
  "ARRAY_TO_STRING({array}, {delimiter})",
  {array:, delimiter:}); 

JsonArrayContains(arr, item) = SqlExpr(
  "ARRAY_CONTAINS({item}::variant, PARSE_JSON({arr}))", 
  {arr:, item:});
  
JsonArrayGet(arr, index) = SqlExpr(
  "GET(PARSE_JSON({arr}), {index})", 
  {arr:, index:});

JsonFormat(json) = SqlExpr(
  "TO_JSON({json})", 
  {json:}); 

ToJsonArray(col) = SqlExpr(
  "{col}::VARIANT", {col:});

ToJson(col) = SqlExpr(
  "TO_JSON({col})", 
  {col:});

JsonParse(json) = SqlExpr(
  "PARSE_JSON({json})", 
  {json:});
  
GetField(obj, field) =  SqlExpr(
  "JSON_EXTRACT_PATH_TEXT({obj}, {field})", {obj:, field:});
  
Now() = SqlExpr(
  "CURRENT_TIMESTAMP()", {});
  
DaysDiff(start_date:, end_date:) = DateDiff("day", start_date, end_date);

ParseStrTimestamp(date_string) = SqlExpr(
  "TRY_TO_TIMESTAMP({date_string})",
  {date_string:});
  
From_Unixtime(string) = SqlExpr(
  "TO_TIMESTAMP_TZ ({string})", {string:});
"""
