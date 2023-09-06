import matplotlib.pyplot as plt
import numpy as np

report = """+----+-------------------------------+---------------------------+-------------------------------------------------------------------------------------------------+
| No | Profile 1 (ydb_non_optimized) | Profile 2 (ydb_optimized) | Query                                                                                           |
|    |         Run Time (ms)         |       Run Time (ms)       |                                                                                                 |
+----+-------------------------------+---------------------------+-------------------------------------------------------------------------------------------------+
| 1  |            1884.946           |          958.959          | SELECT COUNT(*) FROM hits;                                                                      |
+----+-------------------------------+---------------------------+-------------------------------------------------------------------------------------------------+
| 2  |            1905.021           |          962.545          | SELECT COUNT(*) FROM hits WHERE AdvEngineID <> 0;                                               |
+----+-------------------------------+---------------------------+-------------------------------------------------------------------------------------------------+
| 3  |            3219.502           |          994.070          | SELECT SUM(AdvEngineID), COUNT(*), AVG(ResolutionWidth) FROM hits;                              |
+----+-------------------------------+---------------------------+-------------------------------------------------------------------------------------------------+
| 4  |            2093.819           |          1001.208         | SELECT AVG(UserID) FROM hits;                                                                   |
+----+-------------------------------+---------------------------+-------------------------------------------------------------------------------------------------+
| 5  |            2666.008           |          1088.440         | SELECT COUNT(DISTINCT UserID) FROM hits;                                                        |
+----+-------------------------------+---------------------------+-------------------------------------------------------------------------------------------------+
| 6  |            1855.979           |          907.353          | SELECT MIN(EventDate), MAX(EventDate) FROM hits;                                                |
+----+-------------------------------+---------------------------+-------------------------------------------------------------------------------------------------+
| 7  |            1866.890           |          912.255          | SELECT AdvEngineID, COUNT(*) AS count FROM hits WHERE AdvEngineID <> 0 GROUP BY AdvEngineID     |
|    |                               |                           | ORDER BY count DESC;                                                                            |
+----+-------------------------------+---------------------------+-------------------------------------------------------------------------------------------------+
| 8  |            3330.905           |          1129.566         | SELECT RegionID, COUNT(DISTINCT UserID) AS u FROM hits GROUP BY RegionID ORDER BY u DESC LIMIT  |
|    |                               |                           | 10;                                                                                             |
+----+-------------------------------+---------------------------+-------------------------------------------------------------------------------------------------+
| 9  |            5012.379           |          2169.912         | SELECT RegionID, SUM(AdvEngineID), COUNT(*) AS c, AVG(ResolutionWidth), COUNT(DISTINCT UserID)  |
|    |                               |                           | FROM hits GROUP BY RegionID ORDER BY c DESC LIMIT 10;                                           |
+----+-------------------------------+---------------------------+-------------------------------------------------------------------------------------------------+
| 10 |            2058.721           |          989.472          | SELECT MobilePhoneModel, COUNT(DISTINCT UserID) AS u FROM hits WHERE MobilePhoneModel <> ''     |
|    |                               |                           |         GROUP BY MobilePhoneModel ORDER BY u DESC LIMIT 10;                                     |
+----+-------------------------------+---------------------------+-------------------------------------------------------------------------------------------------+
| 11 |            2223.908           |          1046.129         | SELECT MobilePhone, MobilePhoneModel, COUNT(DISTINCT UserID) AS u FROM hits WHERE               |
|    |                               |                           | MobilePhoneModel <> '' GROUP BY MobilePhone, MobilePhoneModel ORDER BY u DESC LIMIT 10;         |
+----+-------------------------------+---------------------------+-------------------------------------------------------------------------------------------------+
| 12 |            2267.086           |          1030.290         | SELECT SearchPhrase, COUNT(*) AS c FROM hits WHERE SearchPhrase <> '' GROUP BY SearchPhrase     |
|    |                               |                           | ORDER BY c DESC LIMIT 10;                                                                       |
+----+-------------------------------+---------------------------+-------------------------------------------------------------------------------------------------+
| 13 |            3062.555           |          1294.268         | SELECT SearchPhrase, COUNT(DISTINCT UserID) AS u FROM hits WHERE SearchPhrase <> '' GROUP BY    |
|    |                               |                           | SearchPhrase ORDER BY u DESC LIMIT 10;                                                          |
+----+-------------------------------+---------------------------+-------------------------------------------------------------------------------------------------+
| 14 |            2577.492           |          1012.803         | SELECT SearchEngineID, SearchPhrase, COUNT(*) AS c FROM hits WHERE SearchPhrase <> '' GROUP BY  |
|    |                               |                           | SearchEngineID, SearchPhrase ORDER BY c DESC LIMIT 10;                                          |
+----+-------------------------------+---------------------------+-------------------------------------------------------------------------------------------------+
| 15 |            2937.697           |          1183.064         | SELECT UserID, COUNT(*) AS c FROM hits GROUP BY UserID ORDER BY c DESC LIMIT 10;                |
+----+-------------------------------+---------------------------+-------------------------------------------------------------------------------------------------+
| 16 |            1801.034           |          895.254          | SELECT UserID FROM hits WHERE UserID = 435090932899640449;                                      |
+----+-------------------------------+---------------------------+-------------------------------------------------------------------------------------------------+
| 17 |            2087.778           |          947.524          | SELECT SearchPhrase, MIN(URL), COUNT(*) AS c FROM hits                                          |
|    |                               |                           |         WHERE URL LIKE '%google%' AND SearchPhrase <> '' GROUP BY SearchPhrase ORDER BY c DESC  |
|    |                               |                           | LIMIT 10;                                                                                       |
+----+-------------------------------+---------------------------+-------------------------------------------------------------------------------------------------+
| 18 |            4142.717           |          1908.525         | SELECT SearchPhrase, MIN(URL), MIN(Title), COUNT(*) AS c, COUNT(DISTINCT UserID) FROM hits      |
|    |                               |                           |         WHERE Title LIKE '%Google%' AND URL NOT LIKE '%.google.%' AND SearchPhrase <> '' GROUP  |
|    |                               |                           | BY SearchPhrase ORDER BY c DESC LIMIT 10;                                                       |
+----+-------------------------------+---------------------------+-------------------------------------------------------------------------------------------------+
| 19 |            1884.752           |          846.203          | SELECT SearchPhrase FROM hits WHERE SearchPhrase <> '' ORDER BY SearchPhrase LIMIT 10;          |
+----+-------------------------------+---------------------------+-------------------------------------------------------------------------------------------------+
| 20 |            2005.179           |          821.821          | SELECT SearchPhrase, EventTime FROM hits WHERE SearchPhrase <> '' ORDER BY EventTime,           |
|    |                               |                           | SearchPhrase LIMIT 10;                                                                          |
+----+-------------------------------+---------------------------+-------------------------------------------------------------------------------------------------+
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

values = {"YDB (with JIT)": list(), "YDB (without JIT)": list()}

for lhs_query_time, rhs_query_time in queries_results:
    values["YDB (without JIT)"].append(lhs_query_time)
    values["YDB (with JIT)"].append(rhs_query_time)

print(f"Values {values}")

values["YDB (with JIT)"] = tuple(e for e in values["YDB (with JIT)"])
values["YDB (without JIT)"] = tuple(e for e in values["YDB (without JIT)"])

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
ax.set_ylim(0, 6000)

fig.savefig("x86_64_hits_full_jit.png")

# plt.show()
