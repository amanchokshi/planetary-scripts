from pathlib import Path
from shutil import copyfile

ims = [i.name for i in Path(".").glob("*.ims")]
xml = [i.name for i in Path(".").glob("*.xml")]

for i, f in enumerate(ims):
    Path(f"{i}").mkdir(parents=True, exist_ok=True)

    if i + 7 < len(ims):
        files = ims[i : i + 7]
        files.extend(xml[i : i + 7])
        for fi in files:
            copyfile(Path(f"{fi}"), Path(f"{i}/{fi}"))

    else:
        files = ims[i:]
        files.extend(xml[i:])
        for fi in files:
            copyfile(Path(f"{fi}"), Path(f"{i}/{fi}"))
