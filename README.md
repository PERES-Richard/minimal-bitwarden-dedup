This is a minimal script to remove exact duplicates from a BitWarden vault, intended to be easy to review.
No dependencies except the JSON standard library.

# Usage

## 0. Review `bitwarden_dedup.py` code

Check that I'm not stealing all your passwords 🙃.


## 1. Save other work and close programs

Because you'll restart your computer at the end.

## 2. Make and mount a RAM disk

Don't save your unencrypted vault to persistent storage (HDD/SSD), as you'd need to securely erase 
it, which is not as easy as some might expect.

### Linux

Makes a 10MB RAM disk.
```
$ sudo mkdir /mnt/ramdisk
$ sudo mount --types tmpfs --options rw,size=10M tmpfs /mnt/ramdisk
```

## 3. Export vault in JSON

[Export your vault](https://vault.bitwarden.com/#/tools/export) (unencrypted JSON) and save it to previously mounted RAM disk.

## 4. Dedupe

Replace the path values `VAULT_WITH_DUPS_PATH` and `VAULT_DEDUPED_OUTPUT_PATH` in `bitwarden_dedup.py` 
with the appropriate ones for your RAM disk and exported vault, then do:

```
python3 bitwarden_dedup.py
```

Which writes to the file at `VAULT_DEDUPED_OUTPUT_PATH`.

In the current script, 'duplicate' means same JSON entry outside of creationDate, revisionDate, id, folderId and first match uri.  
Feel free to edit `bitwarden_dedup.py` if you want to change it's behavior, excluded fields for comparison or logs detail.

## 5. Purge your BitWarden vault, then import deduped JSON

_Optional: Checks if the deduped json export is valid by importing it before purge (see below)._  

[Purge your Vault](https://vault.bitwarden.com/#/settings/account) and  [import new deduped Vault](https://vault.bitwarden.com/#/tools/import) (select  `Bitwarden (json)` as file format and import generated `VAULT_DEDUPED_OUTPUT_PATH` file).

## 6. Power cycle your computer

We could overwrite your secrets on the RAM disk, but I can't do anything foolproof in python about the temporary memory that the script uses, which also contained your unencrypted secrets, so turn off and then on your computer now to clear your RAM.

## 7. Enjoy your brand new Vault without any duplicates!

# Test script

```
python3 run_tests.py
```
