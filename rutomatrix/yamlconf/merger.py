def yaml_merge(dest: dict, src: dict, src_name: str="") -> None:
    """ Merges the source dictionary into the destination dictionary. """

    # Checking if destination is None
    if dest is None:
        # We can't merge into a None
        raise ValueError(f"Could not merge {src_name or 'config'} into None. The destination cannot be None")

    # Checking if source is None or empty
    if not src:
        # If src is None or empty, there's nothing to merge
        return

    _merge(dest, src)


# ======
def _merge(dest: dict, src: dict) -> None:
    for key in src:
        if key in dest:
            if isinstance(dest[key], dict) and isinstance(src[key], dict):
                _merge(dest[key], src[key])
                continue
        dest[key] = src[key]
