from .qgaops_reference import Multivector, blade


def main() -> None:
    value = Multivector.zero() + blade("1") + blade("e1")
    other = blade("1") + blade("e2")
    print(f"(1 + e1)(1 + e2) = {value.geometric_product(other).coefficients}")


if __name__ == "__main__":
    main()
