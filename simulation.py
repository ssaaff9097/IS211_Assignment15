import argparse


def simulateOneServer():
    pass


def simulateManyServers():
    pass


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--servers", help="Number of servers", type=int, default=1)
    parser.add_argument("--file", help="File location", type=str, required=True)
    args = parser.parse_args()
    
