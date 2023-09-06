import matplotlib.pyplot as plt
import numpy as np

# queries_results = [
#     (5521.406, 4266.966),
#     (8195.721, 5210.221),
#     (8884.686, 8959.685),
#     (6794.099, 6712.357),
#     (27349.641, 11614.922),
#     (6580.580, 5348.385),
#     (8488.438, 5893.008),
#     (37667.174, 13879.840),
#     (44625.756, 27102.311),
#     (47690.004, 11524.233),
#     (44553.326, 9661.362)
# ]

report = """+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| No | Profile 1 (postgres_cli) | Profile 2 (ydb_cli) | Query                                                                                           |
|    |      Run Time (ms)       |    Run Time (ms)    |                                                                                                 |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 1  |         5521.406         |       4266.966      | SELECT COUNT(*) FROM hits;                                                                      |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 2  |         8195.721         |       5210.221      | SELECT COUNT(*) FROM hits WHERE AdvEngineID <> 0;                                               |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 3  |         8884.686         |       8959.685      | SELECT SUM(AdvEngineID), COUNT(*), AVG(ResolutionWidth) FROM hits;                              |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 4  |         6794.099         |       6712.357      | SELECT AVG(UserID) FROM hits;                                                                   |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 5  |        27349.641         |      11614.922      | SELECT COUNT(DISTINCT UserID) FROM hits;                                                        |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 6  |         6580.580         |       5348.385      | SELECT MIN(EventDate), MAX(EventDate) FROM hits;                                                |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 7  |         8488.438         |       5893.008      | SELECT AdvEngineID, COUNT(*) AS count FROM hits WHERE AdvEngineID <> 0 GROUP BY AdvEngineID     |
|    |                          |                     | ORDER BY count DESC;                                                                            |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 8  |        37667.174         |      13879.840      | SELECT RegionID, COUNT(DISTINCT UserID) AS u FROM hits GROUP BY RegionID ORDER BY u DESC LIMIT  |
|    |                          |                     | 10;                                                                                             |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 9  |        44625.756         |      27102.311      | SELECT RegionID, SUM(AdvEngineID), COUNT(*) AS c, AVG(ResolutionWidth), COUNT(DISTINCT UserID)  |
|    |                          |                     | FROM hits GROUP BY RegionID ORDER BY c DESC LIMIT 10;                                           |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 10 |        11271.269         |       7136.817      | SELECT MobilePhoneModel, COUNT(DISTINCT UserID) AS u FROM hits WHERE MobilePhoneModel <> ''     |
|    |                          |                     |         GROUP BY MobilePhoneModel ORDER BY u DESC LIMIT 10;                                     |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 11 |        11851.973         |       7577.397      | SELECT MobilePhone, MobilePhoneModel, COUNT(DISTINCT UserID) AS u FROM hits WHERE               |
|    |                          |                     | MobilePhoneModel <> '' GROUP BY MobilePhone, MobilePhoneModel ORDER BY u DESC LIMIT 10;         |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 12 |        44134.083         |       8668.142      | SELECT SearchPhrase, COUNT(*) AS c FROM hits WHERE SearchPhrase <> '' GROUP BY SearchPhrase     |
|    |                          |                     | ORDER BY c DESC LIMIT 10;                                                                       |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 13 |        47690.004         |      11524.233      | SELECT SearchPhrase, COUNT(DISTINCT UserID) AS u FROM hits WHERE SearchPhrase <> '' GROUP BY    |
|    |                          |                     | SearchPhrase ORDER BY u DESC LIMIT 10;                                                          |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 14 |        44553.326         |       9661.362      | SELECT SearchEngineID, SearchPhrase, COUNT(*) AS c FROM hits WHERE SearchPhrase <> '' GROUP BY  |
|    |                          |                     | SearchEngineID, SearchPhrase ORDER BY c DESC LIMIT 10;                                          |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 15 |        42004.802         |      13021.114      | SELECT UserID, COUNT(*) AS c FROM hits GROUP BY UserID ORDER BY c DESC LIMIT 10;                |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 16 |         6700.821         |       4917.704      | SELECT UserID FROM hits WHERE UserID = 435090932899640449;                                      |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 17 |        11431.779         |       7157.851      | SELECT SearchPhrase, MIN(URL), COUNT(*) AS c FROM hits                                          |
|    |                          |                     |         WHERE URL LIKE '%google%' AND SearchPhrase <> '' GROUP BY SearchPhrase ORDER BY c DESC  |
|    |                          |                     | LIMIT 10;                                                                                       |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 18 |        11603.132         |      16429.797      | SELECT SearchPhrase, MIN(URL), MIN(Title), COUNT(*) AS c, COUNT(DISTINCT UserID) FROM hits      |
|    |                          |                     |         WHERE Title LIKE '%Google%' AND URL NOT LIKE '%.google.%' AND SearchPhrase <> '' GROUP  |
|    |                          |                     | BY SearchPhrase ORDER BY c DESC LIMIT 10;                                                       |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 19 |         9743.819         |       5207.604      | SELECT SearchPhrase FROM hits WHERE SearchPhrase <> '' ORDER BY SearchPhrase LIMIT 10;          |
+----+--------------------------+---------------------+-------------------------------------------------------------------------------------------------+
| 20 |         9458.868         |       5534.120      | SELECT SearchPhrase, EventTime FROM hits WHERE SearchPhrase <> '' ORDER BY EventTime,           |
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

values = {"YDB": list(), "PostgreSQL": list()}

for postgres_query_time, ydb_query_time in queries_results:
    values["PostgreSQL"].append(postgres_query_time)
    values["YDB"].append(ydb_query_time)

print(f"Values {values}")

values["YDB"] = tuple(e for e in values["YDB"])
values["PostgreSQL"] = tuple(e for e in values["PostgreSQL"])

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
ax.set_ylim(0, 50000)

fig.savefig("aarch64_hits_full_postgres_ydb.png")

# plt.show()
