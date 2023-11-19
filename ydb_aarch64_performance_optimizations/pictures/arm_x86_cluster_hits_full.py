import matplotlib.pyplot as plt
import numpy as np

report = """+----+---------------------------------+---------------------------------+-------------------------------------------------------------------------------------------------+
| No | Profile 1 (ydb_cli_cluster_arm) | Profile 2 (ydb_cli_cluster_x86) | Query                                                                                           |
|    |          Run Time (ms)          |          Run Time (ms)          |                                                                                                 |
+----+---------------------------------+---------------------------------+-------------------------------------------------------------------------------------------------+
| 1  |             1809.575            |             2123.534            | SELECT COUNT(*) FROM hits;                                                                      |
+----+---------------------------------+---------------------------------+-------------------------------------------------------------------------------------------------+
| 2  |             2136.800            |             2421.070            | SELECT COUNT(*) FROM hits WHERE AdvEngineID <> 0;                                               |
+----+---------------------------------+---------------------------------+-------------------------------------------------------------------------------------------------+
| 3  |             2300.880            |             3984.886            | SELECT SUM(AdvEngineID), COUNT(*), AVG(ResolutionWidth) FROM hits;                              |
+----+---------------------------------+---------------------------------+-------------------------------------------------------------------------------------------------+
| 4  |             1981.442            |             2603.925            | SELECT AVG(UserID) FROM hits;                                                                   |
+----+---------------------------------+---------------------------------+-------------------------------------------------------------------------------------------------+
| 5  |             2887.949            |             3215.451            | SELECT COUNT(DISTINCT UserID) FROM hits;                                                        |
+----+---------------------------------+---------------------------------+-------------------------------------------------------------------------------------------------+
| 6  |             1941.940            |             2365.955            | SELECT MIN(EventDate), MAX(EventDate) FROM hits;                                                |
+----+---------------------------------+---------------------------------+-------------------------------------------------------------------------------------------------+
| 7  |             2073.578            |             2395.410            | SELECT AdvEngineID, COUNT(*) AS count FROM hits WHERE AdvEngineID <> 0 GROUP BY AdvEngineID     |
|    |                                 |                                 | ORDER BY count DESC;                                                                            |
+----+---------------------------------+---------------------------------+-------------------------------------------------------------------------------------------------+
| 8  |             3082.409            |             4229.471            | SELECT RegionID, COUNT(DISTINCT UserID) AS u FROM hits GROUP BY RegionID ORDER BY u DESC LIMIT  |
|    |                                 |                                 | 10;                                                                                             |
+----+---------------------------------+---------------------------------+-------------------------------------------------------------------------------------------------+
| 9  |             5828.657            |             7376.907            | SELECT RegionID, SUM(AdvEngineID), COUNT(*) AS c, AVG(ResolutionWidth), COUNT(DISTINCT UserID)  |
|    |                                 |                                 | FROM hits GROUP BY RegionID ORDER BY c DESC LIMIT 10;                                           |
+----+---------------------------------+---------------------------------+-------------------------------------------------------------------------------------------------+
| 10 |             2210.366            |             2685.117            | SELECT MobilePhoneModel, COUNT(DISTINCT UserID) AS u FROM hits WHERE MobilePhoneModel <> ''     |
|    |                                 |                                 |         GROUP BY MobilePhoneModel ORDER BY u DESC LIMIT 10;                                     |
+----+---------------------------------+---------------------------------+-------------------------------------------------------------------------------------------------+
| 11 |             2449.341            |             2674.282            | SELECT MobilePhone, MobilePhoneModel, COUNT(DISTINCT UserID) AS u FROM hits WHERE               |
|    |                                 |                                 | MobilePhoneModel <> '' GROUP BY MobilePhone, MobilePhoneModel ORDER BY u DESC LIMIT 10;         |
+----+---------------------------------+---------------------------------+-------------------------------------------------------------------------------------------------+
| 12 |             2456.556            |             2905.851            | SELECT SearchPhrase, COUNT(*) AS c FROM hits WHERE SearchPhrase <> '' GROUP BY SearchPhrase     |
|    |                                 |                                 | ORDER BY c DESC LIMIT 10;                                                                       |
+----+---------------------------------+---------------------------------+-------------------------------------------------------------------------------------------------+
| 13 |             3311.023            |             3421.180            | SELECT SearchPhrase, COUNT(DISTINCT UserID) AS u FROM hits WHERE SearchPhrase <> '' GROUP BY    |
|    |                                 |                                 | SearchPhrase ORDER BY u DESC LIMIT 10;                                                          |
+----+---------------------------------+---------------------------------+-------------------------------------------------------------------------------------------------+
| 14 |             2675.136            |             3012.260            | SELECT SearchEngineID, SearchPhrase, COUNT(*) AS c FROM hits WHERE SearchPhrase <> '' GROUP BY  |
|    |                                 |                                 | SearchEngineID, SearchPhrase ORDER BY c DESC LIMIT 10;                                          |
+----+---------------------------------+---------------------------------+-------------------------------------------------------------------------------------------------+
| 15 |             3283.366            |             3776.054            | SELECT UserID, COUNT(*) AS c FROM hits GROUP BY UserID ORDER BY c DESC LIMIT 10;                |
+----+---------------------------------+---------------------------------+-------------------------------------------------------------------------------------------------+
| 16 |             1860.829            |             2603.706            | SELECT UserID FROM hits WHERE UserID = 435090932899640449;                                      |
+----+---------------------------------+---------------------------------+-------------------------------------------------------------------------------------------------+
| 17 |             2311.596            |             2583.602            | SELECT SearchPhrase, MIN(URL), COUNT(*) AS c FROM hits                                          |
|    |                                 |                                 |         WHERE URL LIKE '%google%' AND SearchPhrase <> '' GROUP BY SearchPhrase ORDER BY c DESC  |
|    |                                 |                                 | LIMIT 10;                                                                                       |
+----+---------------------------------+---------------------------------+-------------------------------------------------------------------------------------------------+
| 18 |             4780.210            |             5533.261            | SELECT SearchPhrase, MIN(URL), MIN(Title), COUNT(*) AS c, COUNT(DISTINCT UserID) FROM hits      |
|    |                                 |                                 |         WHERE Title LIKE '%Google%' AND URL NOT LIKE '%.google.%' AND SearchPhrase <> '' GROUP  |
|    |                                 |                                 | BY SearchPhrase ORDER BY c DESC LIMIT 10;                                                       |
+----+---------------------------------+---------------------------------+-------------------------------------------------------------------------------------------------+
| 19 |             2055.996            |             2436.373            | SELECT SearchPhrase FROM hits WHERE SearchPhrase <> '' ORDER BY SearchPhrase LIMIT 10;          |
+----+---------------------------------+---------------------------------+-------------------------------------------------------------------------------------------------+
| 20 |             2150.848            |             2381.626            | SELECT SearchPhrase, EventTime FROM hits WHERE SearchPhrase <> '' ORDER BY EventTime,           |
|    |                                 |                                 | SearchPhrase LIMIT 10;                                                                          |
+----+---------------------------------+---------------------------------+-------------------------------------------------------------------------------------------------+
"""

queries_results = []
report_lines = report.split('\n')
for report_line in report_lines:
    print(f"Report line {report_line}")
    report_line_parts = report_line.split('|')
    try:
        query_number = int(report_line_parts[1].strip())
        lhs_time = float(report_line_parts[2].strip())
        rhs_time = float(report_line_parts[3].strip())
        # print(f"Query number {query_number} lhs time {lhs_time} rhs time {rhs_time}")
        queries_results.append((lhs_time, rhs_time))
    except:
        continue
    # print(f"Report line parts {int(report_line_parts[1].strip())}")


queries_len = len(queries_results)
queries = tuple(f"Q{e}" for e in range(1, queries_len + 1))

values = {"YDB (ARM)": list(), "YDB (X86)": list()}

max_query_time = 0.0

for lhs_query_time, rhs_query_time in queries_results:
    max_query_time = max(max_query_time, lhs_query_time, rhs_query_time)
    values["YDB (ARM)"].append(lhs_query_time)
    values["YDB (X86)"].append(rhs_query_time)

print(f"Values {values}")

values["YDB (ARM)"] = tuple(e for e in values["YDB (ARM)"])
values["YDB (X86)"] = tuple(e for e in values["YDB (X86)"])

print(f"Values tuple {values} queries {queries}")

# # values = {
# #     'YDB': (18.35, 18.43, 14.98),
# #     'PostgresSQL': (38.79, 48.83, 47.50),
# # }

x = np.arange(len(queries))  # the label locations
width = 0.4  # the width of the bars
multiplier = 0

plt.rc("font", size=24)

fig, ax = plt.subplots(layout='constrained')

# for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
#     item.set_fontsize(20)

# ax.title.set_fontsize(40)

fig.set_size_inches(18.5, 10.5)
fig.set_dpi(100)

for attribute, measurement in values.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    # ax.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Time (ms)')
ax.set_title('Hits')
ax.set_xticks(x + width, queries)
ax.legend(loc='upper left', ncols=2)
ax.set_ylim(0, max_query_time * 1.25)

fig.savefig("arm_x86_cluster_hits_full.png")

# plt.show()
