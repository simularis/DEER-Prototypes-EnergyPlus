with ColumnUnits as (
SELECT distinct "ColumnName", "RowName", "Units"
FROM "sim_tabular"
)
SELECT
st.filename,
cu."ColumnName" || '/' || cu."RowName" || ' (' || cu."Units" || ")" as "user_column_name",
sum(Value) as "Value"
from sim_tabular st
join ColumnUnits cu
on st."ColumnName" = cu."ColumnName"
group by st.filename, cu."ColumnName";
