
export_content = open("export_cmd.txt", encoding="utf-8").read().split("# I\"A")[0]
main_lines = open("agentwatch/cli/main.py", encoding="utf-8").read().splitlines()
entry_idx = main_lines.index("# Entrypoint") - 2
new_main = "\n".join(main_lines[:entry_idx]) + "\n\n" + export_content + "\n\n" + "\n".join(main_lines[entry_idx:])
open("agentwatch/cli/main.py", "w", encoding="utf-8").write(new_main)

