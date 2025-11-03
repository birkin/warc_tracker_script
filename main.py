import argparse
from argparse import Namespace


def handle_args() -> Namespace:
    """
    Parse and return command line arguments.

    Returns:
        Parsed command line arguments
    """
    parser = argparse.ArgumentParser(description='Manage WARC tracker checks.')

    # Add mutually exclusive group for collection_id and collection_ids
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--collection_id', type=str, help='Single collection ID to process')
    group.add_argument('--collection_ids', type=str, nargs='+', help='List of collection IDs to process')

    return parser.parse_args()


def check_collection(collection_id: str) -> None:
    """
    Process a single collection ID.

    Args:
        collection_id: The collection ID to process
    """
    print(f'Processing collection: {collection_id}')


def manage_tracker_check() -> None:
    """
    Main function to manage WARC tracker checks.

    Handles both single collection and multiple collections processing
    based on command line arguments.
    """
    args = handle_args()

    if args.collection_id:
        print(f'Processing single collection: {args.collection_id}')
        check_collection(collection_id=args.collection_id)
    elif args.collection_ids:
        print(f'Processing multiple collections: {", ".join(args.collection_ids)}')
        for cid in args.collection_ids:
            check_collection(collection_id=cid)


if __name__ == '__main__':
    manage_tracker_check()
