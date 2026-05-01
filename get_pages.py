import sys

from usp.tree import sitemap_tree_for_homepage


def main():
    tree = sitemap_tree_for_homepage(sys.argv[1])

    for page in tree.all_pages():
        print(page.url)


if __name__ == "__main__":
    main()
