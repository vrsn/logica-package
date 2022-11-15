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

ArrayContains(array, element) = SqlExpr(
  "ARRAY_CONTAINS({array}, {element})", {array:, element:});

Array_min(array) = SqlExpr(
  "SELECT min(pushkin.value) FROM LATERAL FLATTEN(INPUT => {array}) pushkin",
  {array:});

ElementAt(array, index) = SqlExpr(
  "GET({array}, {index}-1)", {array:, index:});

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
  "ARRAY_CONTAINS({item}::variant, PARSE_JSON({arr}::varchar))",
  {arr:, item:});

JsonArrayLength(arr) = SqlExpr(
  "ARRAY_SIZE({arr})", {arr:});

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

Now() = SqlExpr(
  "CURRENT_TIMESTAMP()", {});

ParseStrTimestamp(date_string) = SqlExpr(
  "TO_TIMESTAMP_TZ({date_string}::VARCHAR)",
  {date_string:});

From_ISO8601_TIMESTAMP_NANOS(string) = SqlExpr(
  "TO_TIMESTAMP_TZ({string})", {string:});

From_Unixtime(int) = SqlExpr(
  "TO_TIMESTAMP_LTZ({int})", {int:});

ToVarchar(val) = SqlExpr(
  "TO_VARCHAR({val})", {val:});

GetField(obj, field) =  JsonExtractAsString(obj, field);

JsonExtractAsString(json, path) = ToVarchar(JsonExtractScalar(json, path));
"""
