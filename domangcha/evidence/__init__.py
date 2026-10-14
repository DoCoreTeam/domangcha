"""Evidence adapters: prove that a feature works in *your* product.

REA turns someone else's product into evidence. These adapters do the same for the
product being built: `state` forces loading/empty/error/no-permission, `trace` binds a
browser request to the server log and the stored row, and `ledger` tags every claim as
observation, derivation, inference, or unknown and diffs it against the previous run.
"""
