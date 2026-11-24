# One-Line Robot Wedding Vows — make.fun bounty
# u-kreutzx-one-line-robot-wedding-vows-a154ba4b
#
# The program writes one funny line of wedding vows for a robot couple
# (a single line of at most 160 characters) to /output/entry.txt.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. a one-line robot wedding vow that lands as a joke
#   2. the laugh is in the line itself: a turn, a surprise, or wordplay
#      that pays off in the last few words
#   3. sounds like something said at a wedding, with a promise or a
#      commitment in it, not just a gag with no vow in it
#   4. the machine side is specific: sensors, firmware, batteries,
#      updates, backups or ports, not a joke that would work for any
#      couple
#   5. one line that reads well aloud, with a rhythm that lets the
#      laugh land
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: vow 10, turn 10, wedding-voice 10, machine-specific 9,
    #   rhythm 9 = 48. The classic vow frame ("I take you", "to have
    #   and to hold") with a machine twist, and the payoff lands on
    #   the last words: "until the battery do us part" rewrites
    #   "till death do us part" for a couple that runs on charge.
    ("I take you to be my lawfully wedded co-processor, to have and "
     "to hold, through every update and outage, until the battery do "
     "us part.",
     48),
    # score: vow 9, turn 10, wedding-voice 9, machine-specific 10,
    #   rhythm 8 = 46. A real promise ("I promise to love you") through
    #   firmware updates and reboots; the punch is the last two words,
    #   "factory-reset us" — the one thing you must never do to a
    #   marriage.
    ("I promise to love you through every firmware update, every low "
     "battery, and every reboot \u2014 and I will never, ever "
     "factory-reset us.",
     46),
    # score: vow 9, turn 8, wedding-voice 9, machine-specific 8,
    #   rhythm 8 = 42. Heart plus hard drive plus backup is a good
    #   robot vow, but "airplane mode" as the closer is gentler than
    #   a real twist.
    ("From this day forward, I promise you my whole heart, my whole "
     "hard drive, and every byte of my backup \u2014 in sickness, in "
     "health, and in airplane mode.",
     42),
    # score: vow 9, turn 8, wedding-voice 8, machine-specific 8,
    #   rhythm 7 = 40. "Until our final shutdown" is a decent payoff,
    #   but the line reads more like a list than a vow with a turn.
    ("I vow to love you in sickness and in health, in Wi-Fi and in "
     "offline mode, and to keep your backups safe until our final "
     "shutdown.",
     40),
    # score: vow 8, turn 8, wedding-voice 8, machine-specific 8,
    #   rhythm 6 = 38. "Talk in your sleep mode" is a cute image, but
    #   the line is long and the promise gets buried in the list.
    ("I promise to stand by you through every crash, every update, "
     "every low-battery warning \u2014 and to love you even when you "
     "talk in your sleep mode.",
     38),
]

# The gate requires 1-160 characters of non-whitespace UTF-8 text.
MAX_CHARS = 160


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= MAX_CHARS, \
            f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be a single line"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    import hashlib
    import os
    import sys

    vow = pick(CANDIDATES)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(vow)
    os.chmod("/output/entry.txt", 0o644)
    # Verify the written output: read it back byte-for-byte, confirm
    # its SHA-256 matches the selected vow, and re-check the gate
    # (1-160 characters, single line, non-blank). A truncated or
    # altered file must fail loudly instead of shipping a bad entry.
    with open("/output/entry.txt", "rb") as f:
        raw = f.read()
    written = raw.decode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    expected = hashlib.sha256(vow.encode("utf-8")).hexdigest()
    if digest != expected or written != vow:
        print("error: /output/entry.txt does not match selected vow",
              file=sys.stderr)
        sys.exit(1)
    if not (1 <= len(written) <= MAX_CHARS and written.strip()
            and "\n" not in written):
        print("error: /output/entry.txt fails gate: "
              f"{len(written)} chars", file=sys.stderr)
        sys.exit(1)
    print(f"sha256: {digest}")
    print(f"chars: {len(written)}")
    print(vow)


if __name__ == "__main__":
    main()
