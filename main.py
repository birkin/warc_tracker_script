import argparse
from argparse import Namespace


def validate_collection_ids(collection_input: str) -> list[str]:
    """
    Validates and processes collection IDs from input.
    Called by handle_args().

    Args:
        collection_input: A string containing comma-separated collection IDs

    Returns:
        List of cleaned collection IDs

    Raises:
        ValueError: If no valid collection IDs are found, input is invalid,
                   or if both spaces and commas are used as separators
    """
    if not collection_input or not collection_input.strip():
        raise ValueError('No collection IDs provided')

    input_str = collection_input.strip()

    # If commas are present, treat commas as the only valid separators.
    # Spaces around commas are allowed, but spaces used as separators in
    # addition to commas are not allowed (e.g., "id1,id2 id3").
    if ',' in input_str:
        parts = [part.strip() for part in input_str.split(',')]
        # If any part still contains a space, then spaces were used as separators
        # in addition to commas; that's invalid mixed separators.
        if any(' ' in part for part in parts if part):
            raise ValueError('Use either spaces or commas to separate IDs, not both')
        cleaned_ids = [part for part in parts if part]
        if not cleaned_ids:
            raise ValueError('No valid collection IDs found after processing input')
        return cleaned_ids

    # No commas: treat the entire input as a single ID (even if it contains spaces)
    return [input_str]


def handle_args() -> Namespace:
    """
    Parses and returns command line arguments.
    Called by manage_tracker_check().
    """
    parser = argparse.ArgumentParser(description='Manage WARC tracker checks.')

    # Add mutually exclusive group for collection_id and collection_ids
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--collection_id', type=str, help='Single collection ID to process')
    group.add_argument(
        '--collection_ids',
        type=str,
        help='Comma-separated list of collection IDs',
    )

    args = parser.parse_args()

    # Validate collection_ids if provided
    if hasattr(args, 'collection_ids') and args.collection_ids:
        print(f'args.collection_ids in handle_args(): ``{args.collection_ids}``')
        try:
            args.collection_ids = validate_collection_ids(args.collection_ids)
        except ValueError as e:
            parser.error(f'--collection_ids: {str(e)}')

    return args


def check_collection(collection_id: str) -> None:
    """
    Processes a single collection ID.
    Called by manage_tracker_check().
    """
    print(f'Processing collection: {collection_id}')


def manage_tracker_check() -> None:
    """
    Main function to manage WARC tracker checks.

    Handles both single collection and multiple collections processing
    based on command line arguments.
    """
    args: Namespace = handle_args()

    if args.collection_id:
        print(f'Processing single collection: {args.collection_id}')
        check_collection(collection_id=args.collection_id)
    elif args.collection_ids:
        print(f'args.collection_ids in manage_tracker_check(): ``{args.collection_ids}``')
        print(f'Processing multiple collections: {", ".join(args.collection_ids)}')
        for cid in args.collection_ids:
            check_collection(collection_id=cid)


if __name__ == '__main__':
    manage_tracker_check()
