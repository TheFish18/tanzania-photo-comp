import json
from pathlib import Path

def parse_single_ballot(p: Path):
    with p.open() as f:
        s = f.read()
        s = s[s.index("voter_name"): s.index("Submitted")]
        sl = s.split("\n")
        sl = [s.strip().strip(":") for s in sl if s != '']

        user = sl[1]
        ballot = sl[2:]
        if len(ballot) % 2 == 1:
            ballot.insert(ballot.index(user), "Excellent")
        ballot = {ballot[i]: ballot[i+1] for i in range(0, len(ballot), 2)}
        ballot[user] = "Excellent"
        return user, ballot

if __name__ == "__main__":
    dir = Path("ballots")
    save_dir = Path("ballots/parsed")

    for p in dir.glob("*.txt"):
        user, ballot = parse_single_ballot(p)
        save_p = save_dir.joinpath(p.name)
        with save_p.open('w') as f:
            json.dump(ballot, f, indent=True)
