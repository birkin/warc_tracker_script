import argparse
from argparse import Namespace


def handle_args() -> Namespace:
    """
    Parse and return command line arguments.

    Returns:
        Parsed command line arguments with validated collection IDs
        
    Raises:
        ValueError: If collection_ids is provided but empty after splitting on comma
    """
    parser = argparse.ArgumentParser(description='Manage WARC tracker checks.')

    # Add mutually exclusive group for collection_id and collection_ids
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--collection_id', type=str, help='Single collection ID to process')
    group.add_argument('--collection_ids', type=str, nargs='+', help='Comma-separated list of collection IDs to process')

    args = parser.parse_args()
    
    # Validate collection_ids if provided
    if hasattr(args, 'collection_ids') and args.collection_ids:
        # Flatten the list in case of multiple arguments and split each on comma
        split_ids = []
        for id_string in args.collection_ids:
            split_ids.extend(id_string.split(','))
        
        # Remove any empty strings that might result from trailing/leading commas
        split_ids = [id_str.strip() for id_str in split_ids if id_str.strip()]
        
        if not split_ids:
            raise ValueError('At least one valid collection ID must be provided with --collection_ids')
            
        args.collection_ids = split_ids
    
    return args


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
