import matplotlib.pyplot as plt
import numpy as np

report = """+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| No | Profile 1 (ARM  ydb_cli) | Profile 2 (ydb_cli) | Query                                                                                           |
|    |      Run Time (ms)       |    Run Time (ms)    |                                                                                                 |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 1  |         2575.988         |       5006.797      | SELECT COUNT(*) FROM hits;                                                                      |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 2  |         3531.923         |       5588.360      | SELECT COUNT(*) FROM hits WHERE AdvEngineID <> 0;                                               |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 3  |         4672.073         |       9487.002      | SELECT SUM(AdvEngineID), COUNT(*), AVG(ResolutionWidth) FROM hits;                              |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 4  |         3512.258         |       7050.843      | SELECT AVG(UserID) FROM hits;                                                                   |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 5  |        4821.342          |      12440.140      | SELECT COUNT(DISTINCT UserID) FROM hits;                                                        |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 6  |         3258.782         |       5898.729      | SELECT MIN(EventDate), MAX(EventDate) FROM hits;                                                |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 7  |         3646.865         |       6113.104      | SELECT AdvEngineID, COUNT(*) AS count FROM hits WHERE AdvEngineID <> 0 GROUP BY AdvEngineID     |
|    |                          |                     | ORDER BY count DESC;                                                                            |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 8  |        5356.245          |      15960.377      | SELECT RegionID, COUNT(DISTINCT UserID) AS u FROM hits GROUP BY RegionID ORDER BY u DESC LIMIT  |
|    |                          |                     | 10;                                                                                             |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 9  |        6446.542          |      11366.310      | SELECT CounterID, AVG(length(URL)) AS l, COUNT(*) AS c FROM hits                                |
|    |                          |                     |         WHERE URL <> '' GROUP BY CounterID HAVING COUNT(*) > 100000 ORDER BY l DESC LIMIT 25;   |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 10 |        3298.365          |       7204.381      | SELECT MobilePhoneModel, COUNT(DISTINCT UserID) AS u FROM hits WHERE MobilePhoneModel <> ''     |
|    |                          |                     |         GROUP BY MobilePhoneModel ORDER BY u DESC LIMIT 10;                                     |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 11 |        3585.809          |       8342.150      | SELECT MobilePhone, MobilePhoneModel, COUNT(DISTINCT UserID) AS u FROM hits WHERE               |
|    |                          |                     | MobilePhoneModel <> '' GROUP BY MobilePhone, MobilePhoneModel ORDER BY u DESC LIMIT 10;         |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 12 |        3646.603          |       9508.784      | SELECT SearchPhrase, COUNT(*) AS c FROM hits WHERE SearchPhrase <> '' GROUP BY SearchPhrase     |
|    |                          |                     | ORDER BY c DESC LIMIT 10;                                                                       |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 13 |        4887.997          |      12781.734      | SELECT SearchPhrase, COUNT(DISTINCT UserID) AS u FROM hits WHERE SearchPhrase <> '' GROUP BY    |
|    |                          |                     | SearchPhrase ORDER BY u DESC LIMIT 10;                                                          |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 14 |        4391.186          |      10835.977      | SELECT SearchEngineID, SearchPhrase, COUNT(*) AS c FROM hits WHERE SearchPhrase <> '' GROUP BY  |
|    |                          |                     | SearchEngineID, SearchPhrase ORDER BY c DESC LIMIT 10;                                          |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 15 |        4165.953          |      14504.855      | SELECT UserID, COUNT(*) AS c FROM hits GROUP BY UserID ORDER BY c DESC LIMIT 10;                |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 16 |         2915.191         |       5636.390      | SELECT UserID FROM hits WHERE UserID = 435090932899640449;                                      |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 17 |         4216.598         |       7375.247      | SELECT SearchPhrase, MIN(URL), COUNT(*) AS c FROM hits                                          |
|    |                          |                     |         WHERE URL LIKE '%google%' AND SearchPhrase <> '' GROUP BY SearchPhrase ORDER BY c DESC  |
|    |                          |                     | LIMIT 10;                                                                                       |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 18 |         9913.324         |      15155.429      | SELECT SearchPhrase, MIN(URL), MIN(Title), COUNT(*) AS c, COUNT(DISTINCT UserID) FROM hits      |
|    |                          |                     |         WHERE Title LIKE '%Google%' AND URL NOT LIKE '%.google.%' AND SearchPhrase <> '' GROUP  |
|    |                          |                     | BY SearchPhrase ORDER BY c DESC LIMIT 10;                                                       |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 19 |         3541.45          |       6404.087      | SELECT SearchPhrase FROM hits WHERE SearchPhrase <> '' ORDER BY SearchPhrase LIMIT 10;          |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 20 |         3586.898         |       6354.371      | SELECT SearchPhrase, EventTime FROM hits WHERE SearchPhrase <> '' ORDER BY EventTime,           |
|    |                          |                     | SearchPhrase LIMIT 10;                                                                          |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
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

YDB_ARM_KEY = "YDB (ARM)"
YDB_X86_64_KEY = "YDB (X86-64)"

values = {YDB_ARM_KEY: list(), YDB_X86_64_KEY: list()}

for lhs_query_time, rhs_query_time in queries_results:
    values[YDB_ARM_KEY].append(lhs_query_time)
    values[YDB_X86_64_KEY].append(rhs_query_time)

print(f"Values {values}")

values[YDB_ARM_KEY] = tuple(e for e in values[YDB_ARM_KEY])
values[YDB_X86_64_KEY] = tuple(e for e in values[YDB_X86_64_KEY])

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
ax.set_ylim(0, 20000)

fig.savefig("arm_x86_64_hits_full.png")

# plt.show()
