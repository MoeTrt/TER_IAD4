import re

def parse_func_apx(file_path):
    arguments = []
    attacks = []
    votes = {}
    voter_count = 1

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()

            # Arguments
            match_arg = re.match(r"arg\((\w+)\)\.", line)
            if match_arg:
                arguments.append(match_arg.group(1).lower())
                continue

            # Attaques
            match_att = re.match(r"att\((\w+),(\w+)\)\.", line)
            if match_att:
                attacks.append([match_att.group(1).lower(), match_att.group(2).lower()])
                continue

            # Votes
            match_vote = re.match(r"vote\(([-\d,\s]+)\)\.", line)
            if match_vote:
                values = list(map(int, match_vote.group(1).split(',')))
                votes[f"v{voter_count}"] = dict(zip(arguments, values))
                voter_count += 1

    return arguments, attacks, votes