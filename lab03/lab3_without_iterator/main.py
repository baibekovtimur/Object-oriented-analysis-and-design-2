from social_lab_no_iterator.gui import SocialLabAppNoIterator
from social_lab_no_iterator.point_space import create_seeded_space


def main() -> None:
    space = create_seeded_space()
    app = SocialLabAppNoIterator(space)
    app.mainloop()


if __name__ == "__main__":
    main()
