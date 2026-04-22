from social_lab.gui import SocialLabApp
from social_lab.point_space import create_seeded_space


def main() -> None:
    space = create_seeded_space()
    app = SocialLabApp(space)
    app.mainloop()


if __name__ == "__main__":
    main()
