## Version 1.0.2
- Updated documentation
- Updated `README.md`
- Added `update.sh`
- Added `SHARDC_GIT_REPO_URL` to `shardc/utils/constants/meta.py`
- Variables declared in for loops (e.g. `for var i: i32 = 0;...`) are now in a local scope
- Added `##` token to reset the line counter
- Compiler messages are colored

## Version 1.0.1
- SPP does not use Python exceptions anymore
- Added documentation about `@message`
- shardc version is defined in `shardc/utils/constants/meta.py` in `SHARDC_VERSION`
- Addef `-v/--version` flag
- Added extern function definitions
```sd
extern func f(x) -> T {}
```
- Fixed scoped types usage

## Version 1.0.0
- First release