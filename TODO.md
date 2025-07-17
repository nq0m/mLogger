# TODO for mLogger Suite

## Highest Priority
- [x] Save/load logs (ADIF export complete; CSV not yet implemented)
- [ ] Add help/about dialogs
- [~] UI polish and color scheme (partially complete)
- [ ] Document development process in README.md

## Next Steps
- [x] Set up shared utility functions (date/time, band lookup, file handling, etc.)
- [x] FLRig: Read frequency/mode from radio (implemented, pending testing)
- [ ] WSJT-X: Accept log messages

## Future/Enhancements
- [ ] Add error/status feedback for FLRig integration (e.g., show 'FLRig: ERROR' or warning if unreachable)
- [ ] Consider implementing a custom animated toggle switch widget for better UI polish (current QCheckBox toggle is not animated)
- [ ] Integrate additional radio control/logging features
- [ ] Consider using defusedxml for XML-RPC security if connecting to untrusted FLRig instances
