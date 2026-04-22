# Iterator Pattern Lab (Python + Tkinter)

This project demonstrates the Iterator pattern without using `yield`.

## What is implemented

- User model with attributes: first name, last name, friends, interests.
- Mapping users to 2D points with weighted parameters:
  - first name and last name are ignored in point mapping,
  - friends define the main anchor,
  - interests add a small deviation from that anchor.
  - default priority is friends (0.70), interests (0.25), last name (0.05).
- Point model stores `x`, `y`, and `user_id`.
- Aggregate stores users/points and creates a concrete iterator for nearest users.
- Iterator returns users in order of distance to a selected base user.
- Dark themed GUI:
  - registration-style form,
  - coordinate plane with user points,
  - top-10 nearest users table,
  - step-by-step iterator demo (`has_next` / `next` / `reset`).

## Run

```bash
python main.py
```

No third-party dependencies are required.
