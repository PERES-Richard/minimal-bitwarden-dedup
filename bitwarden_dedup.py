import json

# Your RAM disk file paths here
VAULT_WITH_DUPS_PATH = "/mnt/ramdisk/bitwarden_export.json"
VAULT_DEDUPED_OUTPUT_PATH = "/mnt/ramdisk/bitwarden_deduped.json"

def dedup(vault_with_dups_path, vault_deduped_output_path):
    with open(vault_with_dups_path, encoding='utf-8', mode='r') as vaultfile:
        vault_json = json.load(vaultfile)

    assert not vault_json["encrypted"], """Unfortunately you need to export your vault unencrypted.
    BitWarden seems to use a login item's unique id as salt (or something like that), so there would
    be no duplicates in the encrypted file."""

    items = vault_json["items"]

    # use a set to detect duplicates.
    # two json item objects are duplicates if and only if, after their "id" keys are removed, they
    # have the same string representations (same value of json.dumps).
    item_identities = set()

    # will be the new contents of the "items" map
    deduped_items = []

    for item in items:
        # Save comparison fields before 'ignored deletion'
        item_id = item["id"]
        item_revision_date = item["revisionDate"]
        item_creation_date = item["creationDate"]
        item_folder_id = item["folderId"]

        # Ignore not exact uri match field for comparison
        hasUri = False
        try:
            item_login = item["login"]
            item_uris = item_login["uris"]
            if len(item_uris) > 0:
                hasUri = True
                item_match_uri = item_uris[0]["uri"]
        # Do nothing if no URI set
        except AttributeError:
            pass
        except KeyError:
            pass

        # Ignore fields for comparison by deleting id, revisionDate, creationDate, folderId and match uri (if any)
        # since those can be different in otherwise-exact duplicate items rather than `del` it, just set it to ""
        item["id"] = ""
        item["revisionDate"] = ""
        item["creationDate"] = ""
        item["folderId"] = ""
        if hasUri:
            item["login"]["uris"][0]["uri"] = ""

        # Compare..
        item_identity = json.dumps(item)
        if item_identity not in item_identities:
            item_identities.add(item_identity)

            # add the fields back before append current item in deduped list
            item["id"] = item_id
            item["revisionDate"] = item_revision_date
            item["creationDate"] = item_creation_date
            item["folderId"] = item_folder_id
            if hasUri:
                item["login"]["uris"][0]["uri"] = item_match_uri

            deduped_items.append(item)

    vault_json["items"] = deduped_items

    print(f"{len(items) - len(item_identities)} duplicates removed.")
    print(f"Exported file has {len(item_identities)} login/password/secret items.")

    with open(vault_deduped_output_path, encoding='utf-8', mode='w') as newvaultfile:
        # need ensure_ascii=False because bitwarden doesn't escape unicode characters 
        json.dump(vault_json, newvaultfile, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    dedup(VAULT_WITH_DUPS_PATH, VAULT_DEDUPED_OUTPUT_PATH)
