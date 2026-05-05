# Deadline Track

Deadline Track crawls official conference websites for real-time paper submission
deadlines and falls back to predictions from recent historical deadlines when a
current deadline is not available.

The initial catalog focuses on top A*/A venues relevant to Computer Vision, IoT,
and Drone/Robotics research:

- Computer Vision: CVPR, ICCV, ECCV
- IoT / sensor systems / networking: SIGCOMM, SenSys, IPSN
- Drone / robotics: ICRA, IROS

## Install

```bash
python -m pip install -e .
```

The package uses only the Python standard library.

## Usage

Show all tracked conferences:

```bash
deadline-track --offline
```

Crawl official websites and show live or predicted deadlines:

```bash
deadline-track
```

Filter by research area:

```bash
deadline-track --field "Computer Vision"
deadline-track --field IoT --field Drone
```

Emit JSON for automation:

```bash
deadline-track --json
```

## How deadline selection works

1. Each conference has official pages to crawl and keywords describing the
   deadline language used by the venue.
2. The crawler extracts visible text from those pages and looks for dates near
   submission-related keywords.
3. If a future live deadline is found, the result is marked `live`.
4. If live crawling fails or the page has no future deadline, the tracker
   predicts the next deadline by shifting the latest historical deadline forward
   according to the conference cadence.

Predicted deadlines are intentionally labelled as predictions and should be
verified before planning a submission.
