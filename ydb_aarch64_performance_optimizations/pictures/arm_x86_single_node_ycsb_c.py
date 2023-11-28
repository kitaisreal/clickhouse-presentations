import matplotlib.pyplot as plt
import numpy as np

ARM_RESULTS = (107534.1, 116204.9, 126052.7, 139089.5, 145600.5)
X86_RESULTS = (82784.3, 89273.4, 93282.7, 101510.74, 106120.8)
THREADS = (512, 1024, 2048, 4096, 8192)

ARM_RESULTS = tuple(result / 1000.0 for result in ARM_RESULTS)
X86_RESULTS = tuple(result / 1000.0 for result in X86_RESULTS)

max_result = max(max(ARM_RESULTS), max(X86_RESULTS))

values = {
    'YDB ARM': ARM_RESULTS,
    'YDB x86-64': X86_RESULTS,
}

x = np.arange(len(THREADS))  # the label locations
width = 0.3  # the width of the bars
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
ax.set_xlabel('Threads')
ax.set_ylabel('Throughput (Kops/sec)')
ax.set_title('YCSB Workload C')
ax.set_xticks(x + 0.5 * width, THREADS)
ax.legend(loc='upper left', ncols=2)
ax.set_ylim(0, max_result * 1.25)

fig.savefig("arm_x86_single_node_ycsb_c.png", transparent=True)

# plt.show()
