import re

def preprocess_codeowners_inlining_group_members(template, get_members):
    def replacement(match):
        group_name = match.group(1)
        members = get_members(group_name)
        if members is None:
            return match.group(0)  # leave as-is
        return " ".join(members)
    return re.sub(r'(?<=\s)@(\S+)', replacement, template)
